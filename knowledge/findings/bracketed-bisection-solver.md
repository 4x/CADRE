---
id: finding-bracketed-bisection-solver
type: finding
title: Bracketed bisection for guarded continuous unknowns
summary: 'Inverse views that defeat exact rational solving (higher-degree powers, unknown exponents, logarithms)
  now fall back to scan-then-bisection when the target''s guards declare an explicit finite bracket: 1000-interval
  scan for sign changes plus on-sample hits, bisection per crossing, every root verified against the original
  equation, guards and residual tolerances. Strict guards shrink by nextafter; gaps abort their interval
  without a claim; unbracketed forms keep their original unsupported diagnostic. Sub-resolution gaps and
  touching zeros may be missed and the evidence says so; multiple crossings enumerate through branch-all
  like every other solver path.'
status: accepted
created: '2026-11-04'
updated: '2026-11-04'
topics:
- solver
- inverse-view
confidence: null
relations: []
---

# Bracketed bisection for guarded continuous unknowns

## Finding


## Basis


## Implications


## Limitations / uncertainty
