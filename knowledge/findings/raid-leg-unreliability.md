---
id: finding-raid-leg-unreliability
type: finding
title: Composer unreliable on the RAID rate-conversion leg
summary: 'Across 5 live RAID-chain runs (d2 x2, ap-raid-rate, al-dual-raid x2) the composer reached the
  full MB/s chain twice, stopped early at B/s twice, and misbound transfer_rate to byte_rate twice (one
  recovered). The final conversion leg after an inverse solve is the unreliable joint; distractor facts
  (dual-raid 0/2) make it worse. Candidate fix: prompt nudge to finish in the requested unit. Adversarial
  score 2-6-2.'
status: accepted
created: '2026-11-04'
updated: '2026-11-04'
topics:
- evaluation
- composer
confidence: null
relations: []
---

# Composer unreliable on the RAID rate-conversion leg

## Finding


## Basis


## Implications


## Limitations / uncertainty
