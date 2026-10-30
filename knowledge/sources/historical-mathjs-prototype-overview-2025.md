---
id: source-historical-mathjs-prototype-overview-2025
type: source
title: "Historical Math.js Prototype Overview \u2014 2025"
summary: "Preserved account of the 2025 React/Math.js/Supabase prototype and nested DuPont composition; documentation only, not retained application source."
status: archived
created: '2026-10-29'
updated: '2026-10-29'
topics:
  - architecture
  - runtime
  - lifecycle
confidence: null
relations:
  - type: relates-to
    target: investigation-prototype-2025-mathjs-supabase
  - type: relates-to
    target: concept-unified-computational-graph
  - type: relates-to
    target: decision-retire-standalone-mathjs-implementation
---

# Historical Math.js Prototype Overview — 2025

## Provenance and interpretation

Historical project documentation, not outsider advice. The year 2025 comes from the original filename and existing corpus. This is an account of a prototype, NOT a current source tree or independently reproduced runtime experiment. Read current decisions before reusing its stack or social-feature design.

- Imported on 2026-10-29 from `Legacy/Simple mathJS implementation attempt [2025].md`.
- Created/updated metadata dates describe this source record, not the original document.
- Original payload SHA-256 (including original line endings): `328f057915dcc60299b9f3182772709057cf39df042ea6015b14b427799b844a`.
- The original payload follows unchanged after the marker; line references to the original are relative to that payload.

## Original document (verbatim)

<!-- ORIGINAL DOCUMENT:BEGIN -->

This was a **mathematical modeling and knowledge-sharing platform** that enables users to **create, execute, compose, discover, and share mathematical equations and computational models**. Users can build simple equations, combine them into larger computational graphs, execute models with user-provided inputs, and publish or share their work with others.
A key architectural feature is the **unified graph system**, where both standalone equations and complex multi-step models are stored as `computational_graph` objects. Simple equations are treated as **atomic graphs**, while larger models are built by connecting multiple equations and nested graphs together.
The example provided demonstrates a **hierarchical DuPont financial model**, where reusable sub-models such as *Profit Margin* and *Asset Turnover* are combined to calculate ROI.

---

### What the Platform Does

Key capabilities include:

#### Equation Builder

- Create mathematical formulas using both LaTeX and executable expressions.
- Define variables, units, inputs, outputs, and metadata.

#### Computational Graph Builder

- Connect equations into larger workflows.
- Reuse existing equations and models as building blocks.
- Support nested graphs and dependency chains.

#### Model Execution Engine

- Accept user inputs.
- Compile execution plans.
- Calculate intermediate and final results.

#### Knowledge Management

- Store variables, units, constants, citations, and mathematical definitions.
- Create a searchable library of reusable models.

#### Social Features

- User authentication.
- Public/private models.
- Star, fork, view, and share equations and graphs.

---

### Technologies Used

##### Math.js

- Expression parsing and mathematical evaluation.

#### Frontend

##### React (TypeScript)

- Component-based UI framework.

##### Vite

- Fast build tooling and development server.

##### React Router

- Client-side routing.

##### React Context API

- Global authentication and application state.

##### Tailwind CSS

- Utility-first styling framework.

##### KaTeX / react-katex

- Rendering mathematical expressions from LaTeX.

---

#### Backend

- Backend-as-a-Service platform.

##### PostgreSQL

- Primary data store.

##### Supabase Auth

- User registration, login, and session management.

##### PostgreSQL Functions & RPCs

- Graph compilation and execution support.

##### Row-Level Security (RLS)

- Fine-grained access control.
