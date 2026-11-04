# About this directory

This directory preserves the **original returns from offline curation workers** exactly as received: research bundles, validation reports, session records, quantity/source reviews, and the worker-local helper scripts (`author_batch*.py`, `curation_support.py`, `numerical_review.py`, `quantity_review.py`) that produced them.

It is **evidence and provenance, not product code**:

- Nothing here is imported by the application, the test suite, or the eval batteries.
- The helper scripts run only inside their own worker kit workspaces (plus `curation_support.py` on their path); do not run them from the repo root and do not import them.
- Worker research is staged for review through `connected-models curation validate/import`, never by executing these scripts in place.

Intake status lives in `../data/curation/inventories/` and reviewed pairs in `../data/curation/reviews/`. The dispatch/review workflow is owned by the [offline curation operator guide](../knowledge/notes/offline-curation-agent-kit.md).
