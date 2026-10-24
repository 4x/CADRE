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
