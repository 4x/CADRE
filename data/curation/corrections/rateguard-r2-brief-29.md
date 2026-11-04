# Correction brief: rate-guard r2 (brief 29)

To: rateguard r2 curator (batch engineering-finance-rateguard-b02, 1 revised record)
From: dev, 2026-11-04
Status: prescribed (mechanical — no admitted record is revised; all reviews stand)

## What happened

Batch `engineering-finance-rateguard-b01` returned needs-revision (revBP;
review at
`.runs/review-compat-curation/reviews/engineering-finance-rateguard-b01-review.json`,
validator-accepted) on six precise blockers:

- B1 (locators): NIST locator 'PDF pp. 14-21 (printed 67-74)' is wrong
  (front matter); tables are at PDF pp. 98-106 (printed 66-74). 'PDF p. 75
  (printed 128)' for 8.6.6.1 is wrong: it is PDF p. 160 (printed 128).
  Correct to PDF p. 61 (printed 29, 3.2.2.1 Eq. 3-7), PDF pp. 98-106
  (printed 66-74, Table 5-1, 5.1.2, Tables 5-2 to 5-5), PDF p. 160
  (printed 128, 8.6.6.1).
- B2 (false stale-fragment claim): '#page=61 lands on section 8.2.3, not
  UPV material' is false. #page=61 is PDF p. 61 = printed p. 29, section
  3.2.2.1, giving the UPV definition, Eq. 3-7, and a $100/5yr/3%=$457.97
  worked example (independently recomputed 457.9707). Retract the claim;
  #page=61 is the best single locator.
- B3 (ceiling vs published scope): published FEMP scope caps the DOE real
  rate at 10% (10 CFR 436 via handbook PDF p. 67/printed p. 35; floor 3%
  binding since 2004); examples use 3% and 2.15%; UMD illustration peaks
  at 19.74%. rate<=1 permits a decade (10%-100%) with no published basis.
  Either tighten to rate<=0.1 citing the 10% ceiling (updating boundary
  ref/rejections), or keep 100% as an explicitly justified numerical
  envelope with a scope statement that guard-permitted rates above 10% are
  outside the published application scope. Either resolution keeps the
  finite bracket the implied-rate view needs.
- B4 (inversion residual): implied-rate reference claims root 0.03000345
  with 'residual 7.1e-05'; independent Newton solve gives true root
  0.0300034524, and the quoted root has forward residual 2.6e-03, not
  7.1e-05. Quote the root to >=10 decimals or correct the residual figure.
- B5 (succession/duplication): the record self-declares as the next
  research revision of uniform-present-value@source-3 yet ships under a
  new id with empty duplicate_of and no formal supersession; on admission
  this duplicates the admitted relationship. Add formal supersession
  metadata (duplicate_of/supersedes -> uniform-present-value@source-3)
  with an admission note retiring source-3, or reissue as a revision under
  the original id if the kit permits. Do not admit as a coexisting second
  record.
- B6 (evidence wording): sources[0].evidence claims 'All handbook examples
  use the 3% real DOE rate'; section 8.6.6 uses a 2.15% non-DOE real rate
  (PDF p. 160). Qualify the sentence accordingly.

## Prescription

Author the revised record in a fresh batch
`engineering-finance-rateguard-b02` (single record), resolving all six
blockers. Keep the equation, oracle values and all other ports identical
unless a resolution forces a change; say which changes each resolution
forced and why.

## Resubmission

Validate, pack, and report bundle + return-ZIP verification hashes with each
hash labeled by artifact. Intake will packet the return for independent
re-review; on admission, the live implied-rate battery entry follows.
