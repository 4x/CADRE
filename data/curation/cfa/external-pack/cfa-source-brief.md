# CFA source brief for curators (read with your assignment)

You are curating finance formulas from a CFA PDF you can read directly under `sources/`. This brief complements the kit `AGENTS.md`; where they conflict on sources, this brief wins for source handling only. Everything else in the kit protocol (session contract, atomicity, interface rules, checks, return format) applies unchanged.

## Your PDF

- The owner names the PDF in the dispatch message (for example `sources/CFA-Level-1-book1.pdf`). Work only that PDF unless told otherwise.
- Before the first batch, manifest it: filename, SHA-256, CFA level, book, publisher, title, edition/year, page count if your tools report it. Record the manifest in `SESSION.json` (and keep a `source-manifest.json` beside it). Never rename the PDF.
- The PDF is owner-purchased material. You may read it for this task. You must not redistribute it, copy it into returns, attach pages or screenshots, or paste long verbatim passages anywhere outside your working notes.

## Citing the PDF

Cite the PDF as a `project-derivation` source: you read it directly, but reviewers cannot open it, so it is owner-supplied provenance, not independently verifiable evidence. (The validator requires every `primary` source to carry a public URL, which a purchased PDF has not — never cite the PDF as `primary`.)

- `title`: book title, e.g. `CFA Level I Quantitative Methods`
- `url`: `null` (purchased copy, no accessible URL)
- `version`: publisher and edition/year, e.g. `Prep provider X, 2025 ed.`
- `locator`: exact position, e.g. `Reading 6, printed p. 214 (PDF p. 228), Eq. 3 / Exhibit 12`
- `evidence`: one original sentence stating what the passage asserts (formula role and scope), e.g. `Passage presents the constant-growth dividend discount form with required return above growth.`
- `license`: `Purchased owner copy; personal-use terms assumed; no redistribution`
- `redistribution`: `No redistribution; single-formula transcription with locator only; full PDF never transmitted or stored in returns`

## Corroboration carries the record

Every completed record ALSO needs a directly inspected accessible `primary` source (public textbook, official documentation, agency/standards page) confirming the same formula, recorded per the normal kit rules: actual URL inspected, edition, section/equation, access date, terms page or unknown. Point the relationship's `source_id` at this accessible source, not at the PDF.

If no accessible corroboration exists after reasonable searching, use the fallback instead of forcing one: keep the PDF cited as `project-derivation` with `url: null` (never `primary` — `primary` means publicly checkable, and the validator enforces a URL for it), point the relationship's `source_id` at the PDF citation, and add an `unresolved` entry such as `No accessible corroboration found after <searches tried>; formula verified only against the owner PDF, which reviewers cannot open.` A fallback record has no `primary` source at all: that is acceptable, it validates, and this brief overrides the kit's primary-source discipline on this point. Submit it; review decides (expect deferral unless the owner corroborates from their copy). Never present the PDF citation as independently verifiable.

## What never goes in a return

- The PDF itself, PDF pages, screenshots, or long verbatim passages.
- Bulk transcription of a chapter. Transcribe single formulas with your own formalization, symbol mapping, and translation notes.
- Claims beyond your access ("verified in CFA curriculum" when you mean one prep book).

## Finance-specific rules

- **Canonical base units.** The engine converts inputs to base units before evaluating, so never inline a conversion factor the unit scales already encode (percent↔decimal, annual↔monthly, currency minor units). Conversion records project as identities over registry scales; document factors in `constants`/translation notes, never in the expression.
- **Periods are dimensionless counts.** Financial years/periods never convert to physical seconds; durations in physical time use `duration`, never period counts.
- **No implicit currency conversion.** Amounts in different currencies never mix without an explicit rate model; currency basis (nominal/real, currency unit) is part of the context.
- **Name registry constants; never inline them.** `pi` and the other registry names in your vocabulary snapshot are used by name. Case-specific fitted coefficients stay attributed inputs/constants, not free variables.
- **Guard the math the source requires.** Positive rates/principal where the formula needs them; growth-below-rate for Gordon-type forms; nonzero denominators; stated timing (beginning/end of period) and compounding frequency. Timing and frequency are part of the record, not footnotes.
- **Already covered — do not resubmit as new:** `lump-sum-future-value-discrete`, `ordinary-annuity-future-value`, `annuity-due-future-value`, `annuity-due-present-value`, `growing-annuity-present-value`, `effective-annual-rate-nominal`, `periodic-rate-from-nominal`, `effective-discount-rate`, `level-loan-periodic-payment`, `loan-payment-interest-portion`, `loan-payment-principal-portion`, `arithmetic-gradient-annual-equivalent`, `constant-growth-stock-present-value`, `fisher-real-rate` (all under `engineering-finance--`). Genuinely distinct variants need their own sources and overlap notes naming the nearest existing ID.
- **Out of engine reach? Defer, don't fake.** Iterative solvers (IRR/YTM by iteration), normal-CDF forms (Black-Scholes), and anything needing operators outside your snapshot go to `deferred` with exact sources and the missing capability. `log`, `log10`, `exp`, `sqrt`, `sum`, `prod`, `len` and index families are available forward-only — use them where they genuinely fit.
- **No advice.** Records are mathematical formalizations with scope and provenance, never investment advice, forecasts, or recommendations.
