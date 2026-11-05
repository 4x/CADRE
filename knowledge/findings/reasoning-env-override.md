---
id: finding-reasoning-env-override
type: finding
title: REASONING env overrides inference.toml effort
summary: InferenceSettings.load applies REASONING (minimal/low/medium/high, case-insensitive) over the
  TOML value for every call; unknown values fail closed with the valid list, and validate() ModelErrors
  now propagate unwrapped. Documented in .env.example and setup.md. Tests in test_inference.py; 275 suite
  green.
status: completed
created: '2026-11-04'
updated: '2026-11-04'
topics:
- evaluation
- configuration
confidence: null
relations: []
---

# REASONING env overrides inference.toml effort

## Finding


## Basis


## Implications


## Limitations / uncertainty
