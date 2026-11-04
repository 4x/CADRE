# CFA source brief for curators (attach to every CFA dispatch)

You are curating finance formulas guided by the owner's CFA materials. This brief complements your kit `AGENTS.md`; where they conflict on sources, this brief wins for source handling only. Everything else in `AGENTS.md` (session contract, atomicity, interface rules, checks, return format) applies unchanged.

## What you receive instead of full PDFs

You may receive an **excerpt packet**: the owner's minimal transcriptions (formula + exact locator + scope note) from purchased PDFs you cannot access directly. Rules:

- Treat each excerpt as a **discovery lead**, not as inspected evidence. You did not inspect the PDF.
- For every completed record, **independently corroborate the formula against a directly inspected accessible source** (public textbook, official documentation, agency/standards page) and record that source with edition, URL, section/equation, and access date. The excerpt gets you to the right formula fast; the accessible source is what makes the record verifiable.
- If no accessible corroboration exists after reasonable searching, keep the record honest: cite the owner excerpt precisely (packet ID, formula key, owner-stated locator) in addition to whatever partial evidence you found, mark the interpretation risk in `unresolved` or limitations, and let review decide. Never present the excerpt as a source you inspected.

## Citing the owner excerpts

Cite each excerpt as a `project-derivation` source (it is owner-supplied, not a publication you opened):

- `title`: owner excerpt packet ID, e.g. `Owner excerpt packet cfa-lane-4 (CFA Level II equity, 2026-11-04)`
- `url`: `null` (no accessible URL)
- `version`: the owner-stated book/edition from the packet, e.g. `Prep provider X, CFA Level II Equity, 2025 ed.`
- `locator`: the exact owner-stated locator, e.g. `Vol. 3, printed p. 214 (PDF p. 228), Reading 28, Gordon growth model`
- `evidence`: one original sentence stating what the excerpt asserts (formula role and scope), e.g. `Owner excerpt asserts the constant-growth dividend discount form with required return above growth.`
- `license`: `Purchased owner copy; personal-use terms assumed; no redistribution`
- `redistribution`: `No redistribution; minimal owner-supplied formula transcription with locator only; full PDF never transmitted or stored in returns`

For the corroborating public source, follow the normal `AGENTS.md` rules (actual URL inspected, terms page recorded or unknown, no invented clearance).

## What never goes in a return

- Full PDFs, PDF pages, screenshots, or long verbatim passages — from the excerpts or anywhere else.
- Bulk transcription of a book chapter. Transcribe single formulas with your own formalization, symbols mapping, and translation notes.
- Claims of access you do not have (“verified in CFA curriculum” when you only saw the excerpt).

## Finance-specific rules

- **Canonical base units.** The engine converts inputs to base units before evaluating, so never inline a conversion factor the unit scales already encode (percent↔decimal, annual↔monthly, currency minor units). Conversion records project as identities over registry scales; document factors in `constants`/translation notes, never in the expression.
- **Periods are dimensionless counts.** Financial years/periods never convert to physical seconds; durations in physical time use `duration`, never period counts.
- **No implicit currency conversion.** Amounts in different currencies never mix without an explicit rate model; currency basis (nominal/real, currency unit) is part of the context.
- **Name registry constants; never inline them.** `pi` and the other registry names in your vocabulary snapshot are used by name. Case-specific fitted coefficients stay attributed inputs/constants, not free variables.
- **Guard the math the source requires.** Positive rates/principal where the formula needs them; growth-below-rate for Gordon-type forms; nonzero denominators; stated timing (beginning/end of period) and compounding frequency. Timing and frequency are part of the record, not footnotes.
- **Already covered — do not resubmit as new:** `lump-sum-future-value-discrete`, `ordinary-annuity-future-value`, `annuity-due-future-value`, `annuity-due-present-value`, `growing-annuity-present-value`, `effective-annual-rate-nominal`, `periodic-rate-from-nominal`, `effective-discount-rate`, `level-loan-periodic-payment`, `loan-payment-interest-portion`, `loan-payment-principal-portion`, `arithmetic-gradient-annual-equivalent`, `constant-growth-stock-present-value`, `fisher-real-rate` (all under `engineering-finance--`). Genuinely distinct variants need their own sources and overlap notes naming the nearest existing ID.
- **Out of engine reach? Defer, don't fake.** Iterative solvers (IRR/YTM by iteration), normal-CDF forms (Black-Scholes), and anything needing operators outside your snapshot go to `deferred` with exact sources and the missing capability. `log`, `log10`, `exp`, `sqrt`, `sum`, `prod`, `len` and index families are available forward-only — use them where they genuinely fit.
- **No advice.** Records are mathematical formalizations with scope and provenance, never investment advice, forecasts, or recommendations.
