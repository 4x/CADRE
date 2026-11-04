"""Lexical retrieval over the model catalog with audit-edge expansion.

Retrieval is a pure, deterministic function of (question, models, edges):
the same snapshot and question always retrieve the same subset in the same
order. Lexical scoring finds endpoint models from question vocabulary;
one-hop compat-audit expansion rescues vocabulary-mismatched adapters.
Misses are fatal (the composer cannot use a model it never sees), so the
defaults err toward recall: K=40 seeds plus expansion, capped at 60.
"""

import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

from .contracts import Model

RETRIEVAL_VERSION = "retrieval-v1/1"
SEED_K = 40
RETRIEVAL_CAP = 60
FALLBACK_K = 80
FALLBACK_CAP = 100

FIELD_WEIGHTS = {
    "id": 3.0,
    "output_meaning": 3.0,
    "input_meanings": 2.0,
    "contexts_units": 1.0,
    "assumptions": 0.5,
    "guards": 0.5,
}

STOPWORDS = frozenset(
    """
a an the and or of to in on for with is are was were be been being it its
this that these those as at by from into over after before between through
during each every all any both few more most other some such no nor not only
own same so than too very can will just should now what what is how many much
does do did has have had having there their then there here when where which
who whom why because until while per s t d m ll re ve don won isn aren wasn
""".split()
)

TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Split display text into indexable tokens, dropping stopwords and singles."""
    if not isinstance(text, str):
        return []
    return [
        token
        for token in TOKEN.findall(text.lower())
        if len(token) >= 2 and token not in STOPWORDS
    ]


def model_fields(key: str, model: Model) -> dict[str, set[str]]:
    """Project one model to per-field token sets; weights apply at scoring time."""
    data = asdict(model)
    fields: dict[str, set[str]] = {
        "id": set(
            tokenize(
                key.replace("--", " ")
                .replace("@", " ")
                .replace("/", " ")
                .replace(".", " ")
            )
        ),
        "output_meaning": set(tokenize(str(data["output"].get("meaning", "")))),
        "input_meanings": set(),
        "contexts_units": set(),
        "assumptions": set(),
        "guards": set(),
    }
    for port in list(data["inputs"].values()) + [data["output"]]:
        fields["contexts_units"] |= set(
            tokenize(f"{port.get('unit', '')} {port.get('context', '')}")
        )
    for name, port in data["inputs"].items():
        fields["input_meanings"] |= set(tokenize(f"{name} {port.get('meaning', '')}"))
        fields["contexts_units"] |= set(tokenize(str(name)))
    fields["assumptions"] = set(
        tokenize(" ".join(str(item) for item in data.get("assumptions", [])))
    )
    fields["guards"] = set(
        tokenize(" ".join(str(item) for item in data.get("guards", [])))
    )
    if data.get("families"):
        fields["contexts_units"] |= set(
            tokenize(
                " ".join(
                    f"{name} {family.get('meaning', '')} {family.get('unit', '')} {family.get('context', '')}"
                    for name, family in data["families"].items()
                )
            )
        )
    return fields


@dataclass(frozen=True)
class RetrievalIndex:
    """Precomputed per-model field tokens and corpus IDF weights."""

    fields: dict[str, dict[str, set[str]]]
    idf: dict[str, float]


def build_index(models: dict[str, Model]) -> RetrievalIndex:
    """Index every model once per snapshot; scoring stays a pure lookup."""
    fields = {key: model_fields(key, model) for key, model in models.items()}
    document_frequency: Counter[str] = Counter()
    for per_model in fields.values():
        document_frequency.update(
            set().union(*per_model.values()) if per_model else set()
        )
    count = len(fields)
    idf = {
        token: math.log((count + 1) / (hits + 1)) + 1.0
        for token, hits in document_frequency.items()
    }
    return RetrievalIndex(fields, idf)


def neighbors_from_audit(audit: dict[str, Any]) -> dict[str, set[str]]:
    """Reduce audit edges to undirected neighbor sets for expansion."""
    neighbors: dict[str, set[str]] = {}
    for edge in audit.get("edges", []):
        for endpoint in (edge.get("from"), edge.get("to")):
            neighbors.setdefault(endpoint, set())
        neighbors[edge["from"]].add(edge["to"])
        neighbors[edge["to"]].add(edge["from"])
    return neighbors


@dataclass(frozen=True)
class RetrievalResult:
    """An ordered subset plus the provenance a run record must log."""

    keys: tuple[str, ...]
    seeds: tuple[str, ...]
    expanded: tuple[str, ...]
    dropped: tuple[str, ...]
    version: str = RETRIEVAL_VERSION


def retrieve(
    question: str,
    index: RetrievalIndex,
    neighbors: dict[str, set[str]] | None = None,
    k: int = SEED_K,
    cap: int = RETRIEVAL_CAP,
    weights: dict[str, float] | None = None,
) -> RetrievalResult:
    """Return the top-K seeds plus one-hop neighbors, deterministically ordered.

    Seeds are never dropped by the cap; expansion yields lowest score first.
    Ties break by model key, so equal inputs always give equal outputs.
    """
    question_tokens = set(tokenize(question))
    table = weights or FIELD_WEIGHTS
    scored = []
    for key, per_model in index.fields.items():
        total = 0.0
        for field_name, weight in table.items():
            total += weight * sum(
                index.idf.get(token, 0.0)
                for token in question_tokens & per_model[field_name]
            )
        scored.append((-total, key))
    scored.sort()
    seeds = tuple(key for _, key in scored[: max(k, 0)])
    seed_set = set(seeds)
    expanded: list[str] = []
    if neighbors:
        candidates = sorted(
            {peer for key in seeds for peer in neighbors.get(key, set())} - seed_set
        )
        by_score = sorted(
            (next(score for score, candidate in scored if candidate == peer), peer)
            for peer in candidates
        )
        room = max(cap - len(seeds), 0)
        expanded = [peer for _, peer in by_score[:room]]
        dropped = tuple(peer for _, peer in by_score[room:])
    else:
        dropped = ()
    ordered = tuple(
        key
        for _, key in sorted(
            (next(score for score, candidate in scored if candidate == peer), peer)
            for peer in list(seeds) + expanded
        )
    )
    return RetrievalResult(ordered, seeds, tuple(expanded), dropped)
