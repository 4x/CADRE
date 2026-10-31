---
id: source-mechanics-independent-audit
type: source
title: Separate Scientific Audit of the First Mechanics Return
summary: A separately assigned reviewer recommends the two unchanged constant-acceleration records for bounded local execution with added exact CC BY4 source evidence; three other records need provenance or locator corrections.
status: active
created: '2026-10-31'
updated: '2026-10-31'
topics: [agents, lifecycle, interoperability]
confidence: medium
relations:
  - type: relates-to
    target: question-curation-evidence-and-approval
  - type: relates-to
    target: source-classical-mechanics-first-intake
  - type: relates-to
    target: note-offline-auditor-instructions
---

# Separate mechanics audit

Reviewer `codex-separate-mechanics-auditor` independently investigated all five r1 records in `classical-mechanics-a-b01` on 2026-10-31. This is a separately assigned review role, not independent empirical validation or domain-expert certification. The unchanged original batch canonical SHA-256 is `e9b3abfe9c0bd38af636fad6779536639bcb2c8138fab30528764d43cba82b2d`. The per-record report `.runs/m2-review/review.json` satisfies `cm-scientific-review/1` and passes `connected_models.auditing validate`; it does not publish models. The report includes every criterion's status, exact identity/hash, sources, blockers and permitted-use scope. Original ZIP and research records were not changed.

## Recommendations

| Record suffix | Recommendation | Main finding |
| --- | --- | --- |
| constant-acceleration-displacement | recommend-admit | Final-position equation, declared units/scope, published reference and alternate-route check supported; preserve possible multiple nonnegative inverse roots. |
| velocity-after-constant-acceleration | recommend-admit | Signed one-axis relation, reference, zero-acceleration and inverse degeneracies supported. |
| translational-kinetic-energy | needs-revision | Athlete example locator is mislabeled; exact version/rights source for intended reuse needs completion. |
| gravitational-potential-energy-difference | needs-revision | Regrouping the same product is arithmetic consistency, not independent derivation; complete reusable-source provenance. |
| collinear-constant-force-work | needs-revision | Constructed sign cases are arithmetic checks; complete reusable-source provenance. |

The recommended subset is limited to local conditional scalar calculations under constant acceleration, with original contexts, guards and assumptions retained. Attribution must credit OpenStax, *University Physics Volume 1*, via the linked LibreTexts adaptation, link CC BY4 and identify executable formalization as an adaptation. No textbook assets, training corpus, broad redistribution or legal clearance is approved.

## Actually inspected evidence

- [OpenStax adaptation on LibreTexts, page ID3981](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_%28OpenStax%29/Book%3A_University_Physics_I_-_Mechanics_Sound_Oscillations_and_Waves_%28OpenStax%29/03%3A_Motion_Along_a_Straight_Line/3.05%3A_Motion_with_Constant_Acceleration_%28Part_1%29), modified 2025-03-16: equations3.12/3.13, Examples3.7/3.8 and explicit CC BY4 footer. This is added audit evidence for unchanged equations, not a claim the curator accessed it.
- [LibreTexts terms](https://libretexts.org/terms-conditions), Intellectual Property/Downloading; [CC BY4 deed](https://creativecommons.org/licenses/by/4.0/): page-specific licensing and attribution/change notices inspected. This documents stated conditions rather than resolving legal questions.
- Current primary pages [3.4](https://openstax.org/books/university-physics-volume-1/pages/3-4-motion-with-constant-acceleration), [7.2](https://openstax.org/books/university-physics-volume-1/pages/7-2-kinetic-energy), [8.1](https://openstax.org/books/university-physics-volume-1/pages/8-1-potential-energy-of-a-system), and [7.1](https://openstax.org/books/university-physics-volume-1/pages/7-1-work) independently support the cited equations and numerical examples. Their footers state CC BY-NC-SA and a separate AI-ingestion restriction; [publisher licensing guidance](https://help.openstax.org/s/article/Openstax-textbook-licensing-and-customization) was also inspected. Those current-site restrictions are preserved, not waived or silently substituted for historical licensing.

## Limitations and access failures

The original curator's unspecified mirror/search history remains unrecoverable; this report supplies new actual audit locations. Full historical PDFs were not read: the publisher PDF returned403 and historical Wikimedia/CloudFront PDFs exceeded browsing size limits. The UCF Pressbooks home page declares CC BY4 but its accessed chapter footers say All Rights Reserved, so that mirror was not used to establish reuse eligibility. The UCF constant-acceleration page returned403. No scientific validity claim follows from those failed accesses or search snippets.

Published numerical values serve as source-derived oracles; constructed zero/sign/regrouping checks only establish bounded arithmetic/behavior. Independence is from the submitted expression/curator's assertion where a separately retrieved published result exists, not from the shared underlying physics source. Technical runtime support, model projection and attributed local admission remain the integrator's responsibility.

## Subsequent technical integration evidence — development agent

The integrator retained the complete unchanged research batch and auditor report at `data/curation/reviews/classical-mechanics-a-b01-bundle.json` and `classical-mechanics-a-b01-review.json`. These are data artifacts, not textbook reproductions. `mechanics-integration-receipt.json` records candidate/admission IDs and saved-run references. The original archive SHA-256 remains `b8a32dfdeea575eb10f8191273ad302c1846abcd12a687e787c0cc465fe926a0`.

The generic integration path created and explicitly admitted `classical-mechanics--constant-acceleration-displacement@r1.runtime1` and `classical-mechanics--velocity-after-constant-acceleration@r1.runtime1` under technical integrator identity `codex-technical-integrator`, citing this separate auditor's report digest. Both preserve original symbols, equation, guards, units, contexts and assumptions; the executable adaptation adds exact audit source links, attribution and permitted-use scope. Three nonrecommended records were not projected or admitted.

Actual admitted-model runs reproduce four reviewed reference cases (401.8768 m within the published 402 m tolerance; 33 m; 10 m/s; 5 m/s) and recover 40 s by inversion. Three stored heating queries (investment, operating costs, discounted payback) replay under runtime 0.3 with unchanged numerical outputs and unchanged original bytes; their original engine labels are 0.1.0. No paid application inference was used. Seventy-six offline tests pass, including fresh-registry reproduction, incomplete/stale/self-authored review rejection, dimensional powers/conversion, guarded speed inversion and meaning/frame incompatibilities. This is integration evidence, separate from the scientific findings above, and does not establish full M2-C/D acceptance.
