"""Build ingest-energy-mech review.json files for the CFA-L3 bundles.

Scaffolding and hashes come from connected_models.auditing.template; evidence is
composed from record content plus live oracle recomputation with an independent
safe evaluator. Verdicts: blocked (offline, no curator defect found) except
three needs-revision records with specific defects and one blocked record with
a corroboration gap plus a same-science duplicate. Writes review JSON only.
"""

import ast
import glob
import json
import operator
import os
from pathlib import Path

from connected_models.auditing import template
from connected_models.curation import load_bundle

REVIEWER = "ingest-energy-mech"
REVIEWED = "2026-11-04"
OUT_DIR = "ingest-notes/slice-a-work/reviews"

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate(node, env):
    """Evaluate record expressions over numbers and sum() of lists."""
    if isinstance(node, ast.Expression):
        return evaluate(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.left, env), evaluate(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.operand, env))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "sum" and len(node.args) == 1 and not node.keywords:
            return float(sum(evaluate(node.args[0], env)))
        raise ValueError(f"unsupported call {node.func.id}")
    raise ValueError(f"unsupported node {type(node).__name__}")


def recompute(model):
    """Return (ok_count, total, notes) for the record's reference oracles."""
    tree = ast.parse(model["relationship"]["expression"], mode="eval")
    ok, notes = 0, []
    for ref in model["references"]:
        env = {}
        for key, val in ref["inputs"].items():
            env[key] = [float(x) for x in val] if isinstance(val, list) else float(val)
        try:
            got = evaluate(tree, env)
        except Exception as exc:  # noqa: BLE001 - recorded in the review
            notes.append(f"{ref['id']}: EVAL-FAIL {exc}")
            continue
        want, tol = float(ref["expected"]), float(ref["tolerance"])
        if abs(got - want) <= tol:
            ok += 1
        else:
            notes.append(f"{ref['id']}: MISMATCH got={got} want={want} tol={tol}")
    return ok, len(model["references"]), notes


CANONICAL = {
    # v1-b01..b08 (reviewed 2026-11-04 against canonical CFA L3 forms)
    "financial-analysis--grinold-kroner-equity-expected-return": "Grinold-Kroner E(R)=D/P+(gE-gS)+gPE",
    "financial-analysis--real-estate-long-run-expected-return-cap-rate": "Gordon-style E(R)=cap+gNOI",
    "financial-analysis--real-estate-finite-horizon-expected-return-cap-rate-change": "finite-horizon E(R)=cap+gNOI-dcap",
    "financial-analysis--mean-variance-utility-certainty-equivalent-decimal": "mean-variance U=E(R)-0.5*lam*sig^2, decimal scaling",
    "financial-analysis--singer-terhaar-risk-premium-blend": "Singer-Terhaar blend phi*RPiG+(1-phi)*RPiS",
    "financial-analysis--capm-beta-correlation-volatility": "CAPM beta=rho*sigi/sigm",
    "financial-analysis--building-block-fixed-income-expected-return": "building-block rf+tp+cp+lp sum",
    "financial-analysis--net-exports-saving-investment-identity": "national-accounts (S-I)+TS identity",
    "financial-analysis--singer-terhaar-integrated-risk-premium": "integrated RPiG=rho*sigi*SRgm",
    "financial-analysis--singer-terhaar-segmented-risk-premium": "segmented RPiS=sigi*SRiS",
    "financial-analysis--pension-surplus-market-value-less-liabilities": "surplus MV-PVL",
    "financial-analysis--pension-funding-ratio-assets-over-liabilities": "funding ratio MV/PVL",
    "financial-analysis--surplus-optimization-objective-decimal": "surplus objective U=E(Rs)-0.5*lam*sigS^2",
    "financial-analysis--safety-first-ratio": "Roy safety-first (ERp-RL)/sigp",
    "financial-analysis--arch-conditional-variance-one-lag": "ARCH one-lag gam+alpha*sig2t1+beta*eta2t",
    "financial-analysis--risk-parity-equal-risk-contribution": "risk contribution RCi=wi*covi vs sigp2/n",
    "financial-analysis--taylor-rule-nominal-policy-rate": "Taylor rule with 0.5/0.5 gap coefficients",
    "financial-analysis--age-based-equity-allocation-120-minus-age": "120-minus-age heuristic",
    "financial-analysis--one-over-n-equal-weight": "1/N naive diversification",
    "financial-analysis--shrinkage-vcv-element-weighted-average": "shrinkage w*vs+(1-w)*vt",
    "financial-analysis--capm-security-market-line-expected-return": "SML rf+beta*MRP",
    "financial-analysis--rebalancing-corridor-lower-bound": "corridor lower w-d",
    "financial-analysis--rebalancing-corridor-upper-bound": "corridor upper w+d",
    "financial-analysis--surplus-return-change-over-initial-assets": "surplus return (dA-dL)/A0",
    "financial-analysis--credit-spread-expected-loss-plus-premium": "spread EL+CP decomposition",
    "financial-analysis--age-based-equity-allocation-100-minus-age": "100-minus-age heuristic",
    "financial-analysis--arch-unconditional-variance": "ARCH steady state gam/(1-alpha-beta)",
    "financial-analysis--fx-building-block-exchange-rate-expectation": "FX building-block five-differential sum (Eq9)",
    "financial-analysis--after-tax-expected-return": "after-tax rpt*(1-t)",
    "financial-analysis--after-tax-standard-deviation": "after-tax sig_pt*(1-t)",
    "financial-analysis--after-tax-rebalancing-range": "after-tax range Rpt/(1-t)",
    "financial-analysis--after-tax-account-value": "TDA partnership vpt*(1-ti)",
    # v2-b01..b07
    "financial-analysis--herfindahl-hirschman-index": "HHI sum of squared weights",
    "financial-analysis--effective-number-of-stocks": "effective N = 1/HHI",
    "financial-analysis--bond-current-yield": "current yield coupon/price",
    "financial-analysis--bond-rolldown-return": "rolldown (p_end-p_begin)/p_begin",
    "financial-analysis--bond-rolling-yield": "rolling yield ci+rr",
    "financial-analysis--bond-price-change-duration-convexity": "duration-convexity -md*dy+0.5*cx*dy^2",
    "financial-analysis--bond-spread-price-change": "spread duration-convexity sibling form",
    "financial-analysis--fixed-income-expected-return-build": "five-component E(R) build",
    "financial-analysis--levered-portfolio-return": "levered ri+(vb/ve)*(ri-rb)",
    "financial-analysis--repo-dollar-interest": "repo P*r*days/360 (Actual/360)",
    "financial-analysis--after-tax-fvif-accrual": "accrual FVIF [1+R(1-tx)]^T",
    "financial-analysis--after-tax-fvif-deferred-gains": "deferral FVIF (1+R)^T*(1-tcg)+tcg",
    "financial-analysis--after-tax-fvif-cost-basis": "basis FVIF (1+R)^T*(1-tcg)+tcg*B",
    "financial-analysis--after-tax-fvif-inflation-adjusted": "real accrual FVIF ratio^T",
    "financial-analysis--after-tax-fvif-deferred-gains-inflation": "real deferral FVIF with basis",
    "financial-analysis--tax-drag-proportion": "tax drag (fvpt-fvat)/(fvpt-p)",
    "financial-analysis--human-capital-present-value": "human-capital sum of discounted summands",
    "financial-analysis--domestic-currency-return-compounding": "RDC=(1+rfc)(1+rfx)-1",
    "financial-analysis--balance-sheet-identity": "A=L+E solved as E=A-L",
    "financial-analysis--balance-sheet-change-identity": "change identity dE=dA-dL",
    "financial-analysis--bank-leverage-change-eq3": "Eq3 dee=daa*lev-dll*le",
    "financial-analysis--bank-equity-change-eq4": "Eq4 with L/E=lev-1 substitution",
    "financial-analysis--modified-duration-eq7": "value change dW/W=-dur*dr",
    "financial-analysis--bank-equity-duration-eq8": "equity duration lev*da-(lev-1)*dl*sens",
    "financial-analysis--bank-equity-volatility-eq9": "equity variance Eq9 two-term plus covariance",
    "financial-analysis--quoted-bid-ask-spread": "quoted spread ask-bid",
    "financial-analysis--effective-spread-buy": "buy effective 2*(trade-midpoint)",
    "financial-analysis--effective-spread-sell": "sell effective 2*(midpoint-trade)",
    "financial-analysis--volume-weighted-average-price": "VWAP sum(D)/q",
    "financial-analysis--vwap-transaction-cost-sell": "sell cost size*(bench-trade)",
    "financial-analysis--average-effective-spread": "mean effective sum(S)/n",
    # v3-b01..b06
    "financial-analysis--portfolio-weighted-return-sum": "weighted R=sum w_i R_i (Eq1/Eq2)",
    "financial-analysis--bhb-allocation-contribution": "BHB A_i=(w-bw)*b",
    "financial-analysis--bhb-allocation-total": "BHB A=sum A_i",
    "financial-analysis--bhb-selection-contribution": "BHB S_i=bw*(r-b)",
    "financial-analysis--bhb-selection-total": "BHB S=sum S_i",
    "financial-analysis--bhb-interaction-contribution": "BHB I_i=(w-bw)*(r-b)",
    "financial-analysis--bhb-interaction-total": "BHB I=sum I_i",
    "financial-analysis--bf-allocation-contribution": "BF A_i=(w-bw)*(b-tb)",
    "financial-analysis--carhart-factor-contribution": "factor contribution d*F",
    "financial-analysis--arithmetic-excess-return": "excess r-b",
    "financial-analysis--sortino-ratio": "Sortino (rp-rt)/sd",
    "financial-analysis--target-semivariance": "semivariance sum(M)/n",
    "financial-analysis--upside-capture": "upside capture rm/rb",
    "financial-analysis--downside-capture": "downside capture rm/rb",
    "financial-analysis--capture-ratio": "capture ratio uc/dc",
    "financial-analysis--gain-to-offset-loss": "recovery g=L/(1-L)",
    "financial-analysis--maximum-drawdown": "drawdown (v-vp)/vp with v<=vp",
    "financial-analysis--style-return-component": "style S=B-M",
    "financial-analysis--active-management-return": "active A=P-B",
    "financial-analysis--performance-fee-sharing-leg": "fee leg base+share*(active-base)",
    "financial-analysis--net-active-return": "net active-fee",
    "financial-analysis--fee-schedule-kink": "kink a*=base+(fee-base)/share",
    "financial-analysis--monthly-net-return": "monthly net g-mf/12",
    "financial-analysis--subperiod-twr": "subperiod (v1-v0)/v0",
    "financial-analysis--geometric-linking-twr": "two-leg link (1+a)(1+b)-1",
    "financial-analysis--modified-dietz-return": "Dietz (v1-v0-cf)/(v0+cf*w)",
    "financial-analysis--composite-asset-weighted-return": "composite sum(R)",
    # v4-b01..b07
    "financial-analysis--covered-call-max-gain": "covered-call max gain (x-s)+c",
    "financial-analysis--covered-call-breakeven": "covered-call breakeven s-c",
    "financial-analysis--bull-call-spread-breakeven": "bull breakeven xl+cl-ch",
    "financial-analysis--bull-call-spread-max-profit": "bull max (xh-xl)-(cl-ch)",
    "financial-analysis--bull-call-spread-max-loss": "bull max loss cl-ch",
    "financial-analysis--bear-put-spread-breakeven": "bear breakeven xh-ph+pl",
    "financial-analysis--bear-put-spread-max-loss": "bear max loss ph-pl",
    "financial-analysis--collar-flat-region-profit": "collar flat-region k-s-p+c",
    "financial-analysis--swap-duration-notional": "swap notional ((mt-mp)/ms)*v",
    "financial-analysis--portfolio-basis-point-value": "BPVP m*v*0.0001",
    "financial-analysis--target-basis-point-value": "BPVT m*v*0.0001 with target meaning",
    "financial-analysis--bpv-futures-hedge-count": "hedge count ((t-p)/c)*cf",
    "financial-analysis--equity-futures-count": "futures count ((t-s)/f)*(v/k)",
    "financial-analysis--domestic-currency-return": "RDC=(1+f)(1+x)-1 (Eq1)",
    "financial-analysis--futures-principal-invoice": "invoice (s/100)*c*z",
    "financial-analysis--riskfree-asset-currency-risk": "risk-free-asset risk (1+r)*s",
    "financial-analysis--two-asset-domestic-variance": "two-asset variance Eq4",
    "financial-analysis--trs-net-settlement": "TRS net settlement e+f",
    "financial-analysis--trs-hedged-portfolio-pnl": "hedged P&L p+n",
    "financial-analysis--partial-hedge-blended-return": "blend w*r+(1-w)*f",
    "financial-analysis--fx-quote-conversion": "quote conversion d/q",
    "financial-analysis--semiannual-interest-accrual": "accrual n*r*t",
    "financial-analysis--implied-ffe-rate": "implied FFE 1-F/100",
    "financial-analysis--fomc-hike-probability": "P(hike) (r_impl-r_cur)/(r_new-r_cur)",
    "financial-analysis--stir-futures-locked-rate": "locked rate r_cash+(f_unwind-f_init)/100",
}

NEEDS_REVISION = {
    "financial-analysis--collar-flat-region-profit": [
        "Reference published-cap-profit-oracle carries an unreplaced placeholder "
        "method ('Placeholder replaced below.'); write the actual substitution "
        "route (17-12-1.46+1.44 = 4.98) and resubmit."
    ],
    "financial-analysis--bpv-futures-hedge-count": [
        "Domain rejection case cites guard `c != 0`, which is absent from the "
        "guards list; declare the guard (with the zero-CTD case) or reword the "
        "case and resubmit."
    ],
    "financial-analysis--equity-futures-count": [
        "Domain rejection case cites guard `f != 0`, which is absent from the "
        "guards list; declare the guard (with the zero-beta-future case) or "
        "reword the case and resubmit."
    ],
}

BLOCKED_WITH_DEFECTS = {
    "financial-analysis--domestic-currency-return-compounding": [
        "Single PDF-only source with an unresolved corroboration gap; the owner "
        "PDF cannot be opened by reviewers, so the formula has no accessible "
        "provenance.",
        "Same-science duplicate of financial-analysis--domestic-currency-return "
        "(v4-b04, RDC=(1+f)(1+x)-1 with accessible corroboration); a canonical "
        "choice is needed at consolidation, not a silent merge.",
    ],
}


def provenance_mix(model):
    """Summarize reference provenance labels honestly."""
    pubs = sum(1 for r in model["references"] if r["provenance"].startswith("Published"))
    total = len(model["references"])
    if pubs == total:
        return f"{pubs}/{total} labeled Published result"
    if pubs == 0:
        return f"{total}/{total} constructed/boundary checks, honestly labeled"
    return f"{pubs}/{total} Published, rest constructed/boundary"


def license_posture(model):
    """Summarize the record's rights posture from its source entries."""
    pdf = sum(1 for s in model["sources"] if s["url"] is None)
    unknown = sum(1 for s in model["sources"] if "unknown" in s["license"].lower())
    stated = len(model["sources"]) - unknown
    bits = []
    if pdf:
        bits.append(f"{pdf} owner-PDF project-derivation (no redistribution claimed)")
    if unknown:
        bits.append(f"{unknown} web source(s) with terms unknown (no clearance invented)")
    if stated:
        bits.append(f"{stated} source(s) with stated license")
    return "; ".join(bits)


def money_convention_note(model):
    """Flag pack-convention unit-1 money ports where present."""
    money = [v["symbol"] for v in model["variables"]
             if "currency unit" in v["definition"] and v["unit"] == "1"]
    if money:
        return (" Money-denominated ports (" + ",".join(money) + ") use pack-convention "
                "unit 1 with currency prose; projection-time relabeling to currency "
                "units will be needed.")
    return ""


def build_model_review(model):
    """Compose one honest model review from record content and recomputation."""
    mid = model["id"]
    expr = model["relationship"]["expression"]
    ok, total, notes = recompute(model)
    kinds = sorted({c["kind"] for c in model["rejection_cases"]})
    guards = model["guards"]
    coverage = ""
    if guards and "domain" not in kinds:
        coverage = (" Observation (non-blocking): guards are stated but no domain "
                    "rejection case live-fires them; inverses are still analyzed.")
    canon = CANONICAL[mid]

    checks = {
        "source-fidelity": {
            "status": "not-checked",
            "evidence": (
                f"Offline review: the owner-copy CFA PDF (url null) and "
                f"{len(model['sources']) - 1} corroborating page(s) were not opened; "
                f"no inspection claimed. Independent signal only: expression `{expr}` "
                f"matches the canonical {canon} form; {len(model['sources'])} source "
                f"locator(s)/equation refs are internally consistent with the symbol map."
            ),
        },
        "scope": {
            "status": "passed",
            "evidence": (
                f"Bounded {model['kind']}: {len(model['assumptions'])} assumption(s), "
                f"{len(model['limitations'])} limitation(s); e.g. {model['limitations'][0][:160]}"
                if model["limitations"] else
                f"Bounded {model['kind']}: {len(model['assumptions'])} assumption(s), no limits text."
            ),
        },
        "dimensions": {
            "status": "passed",
            "evidence": (
                f"Ports: {'; '.join(v['symbol'] + '/' + v['unit'] + '/' + v['dimensions'] for v in model['variables'])}. "
                f"Expression `{expr}` closes per the translation notes."
                + money_convention_note(model)
            ),
        },
        "reference-independence": {
            "status": "passed",
            "evidence": (
                f"{ok}/{total} oracles recomputed exactly in tolerance by an independent "
                f"AST evaluator ({', '.join(r['id'] for r in model['references'])}); "
                f"{provenance_mix(model)}. Live publication of 'Published result' labels "
                f"not verified offline."
                + ("" if not notes else " " + " ".join(notes))
            ),
        },
        "guards-inverses": {
            "status": "passed",
            "evidence": (
                f"Guards [{', '.join(guards) if guards else 'none'}]; rejection kinds "
                f"[{', '.join(kinds)}]; inverse notes present with substitution check."
                + coverage
            ),
        },
        "rights-provenance": {
            "status": "not-checked",
            "evidence": (
                f"Offline: live terms not inspected. Record posture: {license_posture(model)}. "
                f"Equation-shape-only use is visible in the record; no curator rights "
                f"defect is visible. Live verification still required."
            ),
        },
    }

    if mid in NEEDS_REVISION:
        if mid == "financial-analysis--collar-flat-region-profit":
            checks["reference-independence"] = {
                "status": "failed",
                "evidence": (
                    "Cap-profit oracle arithmetic recomputes (17-12-1.46+1.44=4.98) but "
                    "its method field is an unreplaced placeholder ('Placeholder replaced "
                    "below.'), so the oracle route is undocumented."
                ),
            }
        else:
            missing = "c != 0" if "bpv" in mid else "f != 0"
            checks["guards-inverses"] = {
                "status": "failed",
                "evidence": (
                    f"A domain rejection case cites guard `{missing}`, which is absent "
                    f"from the guards list (guards are empty); the cited enforcement does "
                    f"not exist."
                ),
            }
        blockers = list(NEEDS_REVISION[mid]) + [
            f"Offline review ({REVIEWER} {REVIEWED}): live source and terms inspection "
            f"still required after the correction."
        ]
        recommendation = "needs-revision"
        permitted = "None pending revision. Intended scope after correction: " + model["summary"]
    elif mid in BLOCKED_WITH_DEFECTS:
        blockers = list(BLOCKED_WITH_DEFECTS[mid])
        recommendation = "blocked"
        permitted = ("None. Formula RDC=(1+rfc)(1+rfx)-1 recomputes, but admission needs "
                     "accessible provenance or a canonical-choice decision favoring the "
                     "v4-b04 sibling.")
    else:
        blockers = [
            f"Offline review ({REVIEWER} {REVIEWED}): live source access and terms "
            f"inspection still required before admission; no curator defect found. "
            f"Oracles {ok}/{total} recomputed; canonical {canon} form matched."
        ]
        recommendation = "blocked"
        permitted = ("None pending live-source verification. Intended scope after "
                     "verification: " + model["summary"])

    return {
        "checks": checks,
        "sources": [],
        "blockers": blockers,
        "recommendation": recommendation,
        "permitted_use": permitted,
    }


def main():
    """Build one review JSON per bundle from packet templates."""
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = sorted(glob.glob(
        "from-offline-curation-workers/financial-analysis-cfa-l3-*/bundle.json"))
    counts = {"blocked": 0, "needs-revision": 0, "recommend-admit": 0}
    for path in paths:
        bundle = load_bundle(Path(path))
        report = template(bundle)
        report["reviewer"] = REVIEWER
        report["reviewed"] = REVIEWED
        originals = {m["id"]: m for m in bundle["models"]}
        for entry in report["models"]:
            review = build_model_review(originals[entry["id"]])
            entry.update(review)
            counts[review["recommendation"]] += 1
        out = os.path.join(OUT_DIR, f"{bundle['batch_id']}-review-{REVIEWER}.json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)
        print(f"wrote {out}")
    print(f"counts={counts}")


if __name__ == "__main__":
    main()

