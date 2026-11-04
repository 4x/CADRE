# Correction brief: focal-length context alignment for lens-maker → imaging (brief 9)

To: waves-and-optics curator (batches codex-b01, codex-b02)
From: dev intake (compat audit), 2026-11-03
Status: needs-revision (mechanical, not scientific — both reviews stand as recommend-admit)

## What happened

`waves-and-optics--thin-lens-maker` and
`waves-and-optics--gaussian-finite-conjugate-imaging` both passed
scientific review (recommend-admit) and are admitted, but the
lens-maker → imaging → magnification chain cannot execute: chaining
requires exact `(meaning, context)` equality on the linked ports
(units already match at `m`), and the two `focal_length` ports carry
different contexts.

Maker output `f` context (registry
`waves-and-optics--thin-lens-maker@r1.runtime1`):

> Same paraxial homogeneous thin lens, ordered incident and exit surfaces, common homogeneous exterior medium on both sides, wavelength and material state. Real-is-positive focal convention: positive converging, negative diverging. Positive signed surface curvature has its center on the outgoing side; first biconvex curvature positive and second negative.

Imaging input `f` context (registry
`waves-and-optics--gaussian-finite-conjugate-imaging@r1.runtime1`):

> Same paraxial thin lens (center reference, same exterior medium on both sides) or spherical mirror (vertex reference), optical axis, real object and wavelength/medium conditions. Real-is-positive convention: d_o>0, d_i>0 for real images and d_i<0 for virtual images; f>0 converging lens/concave mirror, f<0 diverging lens/convex mirror.

This is the documented near-miss shape (same meaning, different
contexts), which wants a context-alignment revision. No evidence was
questioned and nothing was modified.

## Fix: move the imaging side (1 record, 1 variable, contexts only)

`waves-and-optics--gaussian-finite-conjugate-imaging` (codex-b01, r1 → r2):

- Input `f` variable: context → the maker output context above,
  byte-identical. Keep its symbol, source symbol, role, meaning
  (`focal_length`), definition, dimensions, domain, and unit (`m`)
  byte-identical.
- `d_o` and `d_i` keep the imaging-instance context byte-identical
  (they describe the conjugate pair, which is correct where it is).
- Append one sentence to `translation_notes` stating the `f` input
  now names the supplying thin-lens element description so
  lens-maker focal lengths bind; nothing else in the notes changes.
- Keep expression, output symbol, guards, references, rejection
  cases, assumptions, limitations, sources, and evidence
  byte-identical.

Why the imaging side moves: the shared string must truthfully
describe the linked value on both sides. The maker context describes
exactly that value — one thin lens's focal length, center plane,
common exterior medium, real-is-positive — and the imaging lens
branch already assumes all of it (same exterior medium both sides,
center reference, supplied `f` for its index and wavelength). The
imaging context additionally asserts a mirror alternative and a real
object, which are false of the maker's pure element property, so the
maker side cannot adopt it without misdescribing itself. Mixed
contexts within one record are precedented (130 of 232 registry
models), and no working edge is lost: no producer emits the old
imaging `f` context today, while imaging → magnification already
matches on `image_distance` and is untouched — so after admission the
full lens-maker → imaging → magnification chain executes.

Out of scope: mirror-branch supply stays unbound (fail-closed, as it
is today); aligning `spherical-mirror-focal-radius` output with an
imaging `f` input would be a separate mirror-side revision.

## References: no changes needed

A context string is not arithmetic input. Every `inputs`,
`expected`, `tolerance`, and `method` stays byte-identical and replays
exactly as in r1 (0.125 m real image, −0.100 m virtual image,
−0.15 m ray-construction check).

## Resubmission

Submit the r2 record as a small correction batch (bundle + return as
usual) for re-review per protocol since record text changes.
