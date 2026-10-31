"""Single-operator candidate, admission and withdrawal storage with immutable history."""

from contextlib import closing
from dataclasses import asdict, replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any
from uuid import uuid4

from .contracts import Composition, Model, ModelError, Node, Value, finite
from .runtime import execute, validate_model
from .serialization import MAX_RECORD_BYTES, model_digest, model_from_dict, text


class Registry:
    """Keep incomplete candidates separate from explicitly reviewed executable versions."""

    def __init__(self, path: Path) -> None:
        """Create one local store; statements are serialized by SQLite transactions."""
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with closing(sqlite3.connect(path)) as db, db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS candidates
                (id TEXT PRIMARY KEY, payload TEXT NOT NULL, diagnostics TEXT NOT NULL, created TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS models
                (key TEXT PRIMARY KEY, candidate TEXT NOT NULL, digest TEXT NOT NULL, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS reviews
                (id TEXT PRIMARY KEY, model_key TEXT NOT NULL, candidate TEXT NOT NULL,
                 decision TEXT NOT NULL, reviewer TEXT NOT NULL, notes TEXT NOT NULL, created TEXT NOT NULL);
            """)

    def propose(self, payload: dict[str, Any]) -> str:
        """Store raw extraction and its diagnostics, including partial/invalid candidates."""
        serialized = json.dumps(payload, allow_nan=False)
        if len(serialized.encode()) > MAX_RECORD_BYTES:
            raise ModelError("Candidate exceeds the storage size limit.")
        diagnostics = []
        blockers = payload.get("intake_blockers", [])
        if not isinstance(blockers, list) or any(not isinstance(item, str) or not item.strip() for item in blockers):
            raise ModelError("Intake blockers must be an array of nonempty strings.")
        diagnostics.extend(blockers)
        try:
            model = model_from_dict(payload.get("model"))
            validate_model(model)
            if not payload.get("evidence"):
                diagnostics.append("Missing extraction evidence.")
            if not payload.get("checks") or not all(self.verify_reference(model, check) for check in payload["checks"]):
                diagnostics.append("Independent reference checks have not passed.")
        except ModelError as exc:
            diagnostics.append(str(exc))
        candidate_id = str(uuid4())
        with closing(sqlite3.connect(self.path)) as db, db:
            existing = db.execute("SELECT id FROM candidates WHERE payload = ?", (serialized,)).fetchone()
            if existing:
                return existing[0]
            db.execute("INSERT INTO candidates VALUES (?, ?, ?, ?)",
                       (candidate_id, serialized, json.dumps(diagnostics), datetime.now(timezone.utc).isoformat()))
        return candidate_id

    @staticmethod
    def verify_reference(model: Model, check: dict[str, Any]) -> bool:
        """Recompute the supplied independent oracle; never trust an author's passed flag."""
        try:
            reference = check["reference"]
            expected = finite(reference["expected"], "Reference expected value")
            tolerance = finite(reference.get("tolerance", 0.005), "Reference tolerance")
            if tolerance <= 0 or set(reference["inputs"]) != set(model.inputs):
                return False
            test_model = replace(model, status="fixture")
            node = Node("reference", model.key, {name: Value(amount, model.inputs[name], "fixture", "Supplied independent numerical reference")
                                               for name, amount in reference["inputs"].items()})
            result = execute(Composition("admission-reference", (node,), (node.id,)), {model.key: test_model})
            return result["status"] == "completed" and abs(result["outputs"][node.id]["amount"] - expected) <= tolerance
        except (ModelError, KeyError, TypeError):
            return False  # Caller stores an explicit blocking diagnostic for failed evidence.

    def candidate(self, candidate_id: str) -> dict[str, Any]:
        """Retrieve a draft with the evidence needed for human source review."""
        with closing(sqlite3.connect(self.path)) as db:
            row = db.execute("SELECT payload, diagnostics, created FROM candidates WHERE id = ?", (candidate_id,)).fetchone()
        if row is None:
            raise ModelError("Candidate not found.")
        return {"id": candidate_id, **json.loads(row[0]), "diagnostics": json.loads(row[1]), "created": row[2]}

    def candidates(self) -> list[dict[str, Any]]:
        """List persisted candidate evidence in insertion order for a review bundle."""
        with closing(sqlite3.connect(self.path)) as db:
            identifiers = [row[0] for row in db.execute("SELECT id FROM candidates ORDER BY rowid")]
        return [self.candidate(candidate_id) for candidate_id in identifiers]

    def review(self, candidate_id: str, reviewer: str, notes: str, decision: str = "accepted") -> str:
        """Publish or withdraw only via an explicit attributed local review operation."""
        text(reviewer)
        text(notes)
        if decision not in {"accepted", "rejected", "withdrawn"}:
            raise ModelError("Unsupported review decision.")
        candidate = self.candidate(candidate_id)
        model = model_from_dict(candidate.get("model"))
        validate_model(model)
        if decision == "accepted" and candidate["diagnostics"]:
            raise ModelError("Candidate has blocking diagnostics; propose a corrected version before publication.")
        review_id = str(uuid4())
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT digest, candidate FROM models WHERE key = ?", (model.key,)).fetchone()
            if existing and (existing[0] != model_digest(model) or existing[1] != candidate_id):
                raise ModelError("This immutable model revision already belongs to another candidate; use a new version.")
            if decision == "accepted":
                db.execute("INSERT OR IGNORE INTO models VALUES (?, ?, ?, ?)",
                           (model.key, candidate_id, model_digest(model), json.dumps(asdict(model))))
            db.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (review_id, model.key, candidate_id, decision, reviewer, notes, datetime.now(timezone.utc).isoformat()))
        return review_id

    def snapshot(self) -> tuple[dict[str, Model], dict[str, dict[str, Any]]]:
        """Read a consistent eligible-version snapshot; later withdrawals affect new runs."""
        models: dict[str, Model] = {}
        admissions: dict[str, dict[str, Any]] = {}
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("BEGIN")
            for key, candidate_id, digest, payload in db.execute("SELECT key, candidate, digest, payload FROM models"):
                review = db.execute("SELECT id, decision, reviewer, notes, created FROM reviews WHERE candidate = ? ORDER BY rowid DESC LIMIT 1", (candidate_id,)).fetchone()
                if review and review[1] == "accepted":
                    model = model_from_dict(json.loads(payload))
                    if model_digest(model) != digest:
                        raise ModelError("Stored model integrity check failed.")
                    models[key] = replace(model, status="eligible")
                    admissions[key] = {"digest": digest, "candidate": candidate_id, "review_id": review[0],
                                       "reviewer": review[2], "notes": review[3], "reviewed": review[4]}
        return models, admissions
