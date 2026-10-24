This project is a mathematical modeling platform that allows users to discover, create, and share mathematical equations and computational graphs. It's built with a React frontend, styled with Tailwind CSS, and uses Supabase for its backend (database, authentication, and server-side logic).

Here's a comprehensive walkthrough of the project's architecture and its components:

## **Project Structure Overview**

The project is organized into several key directories:

- **`public/`**: Contains static assets like the `vite.svg` icon.
- **`db/`**: Holds conceptual database schema definitions (`schema1.sql`).
- **`supabase/migrations/`**: Stores SQL scripts for Supabase database schema changes.
- **`src/`**: The main directory for the React frontend application.
  - **`components/`**: Reusable UI components, further categorized by their domain (e.g., `equation`, `graphs`, `layout`, `math`, `ui`).
  - **`contexts/`**: React Contexts for global state management.
  - **`lib/`**: Utility functions and Supabase client initialization.
  - **`pages/`**: Top-level components representing different views or pages of the application.
  - **`App.tsx`**: The root React component, handling routing and global error boundaries.
  - **`main.tsx`**: The entry point for the React application.
  - **`index.css`**: The main CSS file, importing Tailwind CSS.
- **Configuration Files**: `package.json`, `vite.config.ts`, `tailwind.config.js`, `postcss.config.js`, `eslint.config.js`, and `tsconfig.*.json` files manage project dependencies, build processes, styling, linting, and TypeScript compilation.

## **Detailed Component Descriptions**

### **Core Configuration and Build System**

1. **`package.json`**:
   
   - **Purpose**: Defines project metadata, scripts for common tasks (like `dev`, `build`, `lint`), and lists all project dependencies (runtime libraries like React, Supabase JS, Math.js, and development tools like Vite, Tailwind CSS, ESLint).
   - **Interactions**: Essential for setting up the development environment and managing the project's software ecosystem.

2. **`vite.config.ts`**:
   
   - **Purpose**: Configures Vite, the fast build tool used for development and production builds.
   - **Key Functionality**: Specifies plugins (e.g., `@vitejs/plugin-react` for React support) and optimization settings for dependencies.
   - **Interactions**: Vite uses this file to bundle, transpile, and serve the application.

3. **`tailwind.config.js`**:
   
   - **Purpose**: Configures Tailwind CSS.
   - **Key Functionality**: Defines `content` paths for Tailwind to scan for classes, allowing it to generate only the necessary CSS. It can also extend Tailwind's default theme.
   - **Interactions**: Works in conjunction with PostCSS to process CSS files.

4. **`postcss.config.js`**:
   
   - **Purpose**: Configures PostCSS, a tool for transforming CSS with JavaScript plugins.
   - **Key Functionality**: Includes `tailwindcss` (to process Tailwind directives) and `autoprefixer` (to automatically add vendor prefixes for browser compatibility).
   - **Interactions**: Processes CSS files during the build step, ensuring styles are correctly applied and optimized.

5. **`eslint.config.js`**:
   
   - **Purpose**: Configures ESLint, a static code analysis tool for identifying problematic patterns found in JavaScript/TypeScript code.
   - **Key Functionality**: Defines linting rules, specifies files to ignore, and integrates plugins for React hooks and React Fast Refresh.
   - **Interactions**: Helps maintain code quality and consistency across the project.

6. **`tsconfig.*.json`**:
   
   - **Purpose**: TypeScript compiler configuration files.
   - **Key Functionality**: `tsconfig.app.json` configures TypeScript for the client-side React application, while `tsconfig.node.json` is for Node.js-specific files (like `vite.config.ts`). They define compiler options such as target ECMAScript version, module resolution, and JSX support.
   - **Interactions**: Used by the TypeScript compiler to type-check the code and by Vite during the bundling process.

### **Application Entry Points and Core Structure**

7. **`index.html`**:
   
   - **Purpose**: The main HTML file that serves as the entry point for the web browser.
   - **Key Functionality**: Contains the `<div id="root">` where the React application is mounted and links to `src/main.tsx` as the JavaScript entry point.
   - **Interactions**: The initial document loaded by the browser.

8. **`src/main.tsx`**:
   
   - **Purpose**: The primary JavaScript/TypeScript entry point for the React application.
   - **Key Functionality**: Uses `createRoot` from `react-dom/client` to render the `App` component into the `root` element. It wraps the `App` in `StrictMode` for development-time checks and includes a basic error fallback.
   - **Interactions**: Initializes and renders the entire React application.

9. **`src/index.css`**:
   
   - **Purpose**: The main CSS file for the application.
   - **Key Functionality**: Imports Tailwind CSS directives (`@tailwind base`, `@tailwind components`, `@tailwind utilities`), which are then processed by PostCSS to generate the final stylesheet.
   - **Interactions**: Defines the global styles and integrates the Tailwind CSS framework.

10. **`src/App.tsx`**:
    
    - **Purpose**: The root component of the React application, responsible for setting up routing, global contexts, and top-level error handling.
    - **Key Functionality**:
    - **`ErrorBoundary`**: A React class component that catches JavaScript errors in its child tree, preventing the entire application from crashing and displaying a user-friendly fallback.
    - **`AuthProvider`**: Wraps the entire application, making authentication state and functions available to all components via React Context.
    - **`BrowserRouter as Router`**: Configures client-side routing using React Router DOM.
    - **`Routes` and `Route`**: Define the application's navigation paths and map them to specific page components.
    - **`Navbar` and `Footer`**: Layout components that appear on most pages.
    - **Interactions**: Acts as the central orchestrator, managing the overall structure, navigation, and global state of the frontend.

### **Utility and Global Contexts**

11. **`src/lib/utils.ts`**:
    
    - **Purpose**: Provides general utility functions.
    - **Key Functionality**: The `cn` function (short for "class names") is a helper that uses `clsx` for conditional class joining and `tailwind-merge` to intelligently merge conflicting Tailwind CSS classes, ensuring correct styling.
    - **Interactions**: Used by various UI components to construct dynamic and clean CSS class strings.

12. **`src/lib/supabase.ts`**:
    
    - **Purpose**: Initializes the Supabase client and provides helper functions for interacting with the Supabase backend.
    - **Key Functionality**:
    - **`supabase` client**: Created using `createClient` with environment variables for the Supabase URL and anonymous key, configured for session persistence and auto-refresh.
    - **`compileGraph(graphId)`**: An asynchronous function that calls a Supabase Remote Procedure Call (RPC) named `rpc_compile_graph` to trigger server-side compilation of a computational graph.
    - **`checkGraphCompilation(graphId)`**: An asynchronous function that queries the database to determine if a computational graph needs recompilation by comparing `compiled_at` and `updated_at` timestamps of the graph and its components, also considering if the graph is `frozen`.
    - **Interactions**: This file is the primary interface for all data persistence, authentication, and server-side logic interactions with Supabase from the frontend.

13. **`src/contexts/AuthContext.tsx`**:
    
    - **Purpose**: Manages user authentication state and provides authentication-related functions to the entire React application using the Context API.
    - **Key Functionality**:
    - **`AuthContext`**: The React Context object that holds the authentication state (`user`, `session`, `loading`) and functions (`signIn`, `signUp`, `signOut`).
    - **`useAuth` hook**: A custom React hook that allows any component to easily access the authentication context.
    - **`AuthProvider` component**: Responsible for:
    - Initializing the Supabase authentication listener (`onAuthStateChange`).
    - Updating the `user`, `session`, and `loading` states based on authentication events.
    - Providing `signIn`, `signUp`, and `signOut` methods that interact with `supabase.auth`.
    - Handling the creation of a corresponding user record in the `public.user` table upon successful sign-up.
    - **Interactions**: `App.tsx` uses `AuthProvider` to wrap the application, and components like `Navbar`, `SignInPage`, and `SignUpPage` consume the context via `useAuth` to manage user sessions.

### **Database Schema and Migrations**

14. **`db/schema1.sql`**:
    
    - **Purpose**: Provides a conceptual overview of the database schema. It's a static representation for understanding the data model, not meant to be executed directly.
    - **Key Functionality**: Defines various tables such as `citation`, `comment`, `computational_graph`, `model_variable`, `unit`, `user`, `variable`, and their columns, primary keys, unique constraints, and foreign key relationships.
    - **Interactions**: Serves as a blueprint for the database structure.

15. **`supabase/migrations/*.sql`**:
    
    - **Purpose**: Contains SQL migration scripts that define the actual changes applied to the Supabase PostgreSQL database schema over time.
    - **`20250610042908_wooden_dew.sql`**: Adds a unique constraint to the `user_equation` table to ensure that a user can only have one specific relationship (e.g., 'starred', 'visited') with a given equation, enabling safe upsert operations.
    - **`20250620024514_fierce_wave.sql`**: This is a significant migration that unifies the `equation` and `computational_graph` concepts.
    - It extends the `computational_graph` table with fields like `is_atomic`, `expression_latex`, `expression_code`, `compiled_graph`, `compiled_at`, `frozen`, and `tags` to accommodate both composite graphs and atomic equations.
    - Introduces the `graph_component` table for polymorphic relationships, allowing graphs to contain either equations or other nested graphs as components.
    - Includes SQL logic to migrate existing `equation` data into the `computational_graph` table as atomic entries.
    - Defines PostgreSQL functions (`compile_graph`, `auto_compile_parent_graphs`) and an RPC function (`rpc_compile_graph`) for server-side graph compilation and automatic recompilation triggers.
    - Sets up Row Level Security (RLS) policies for the new `graph_component` table and updates existing RLS policies for `computational_graph`.
    - **`20250620025255_fragrant_river.sql`**: Updates the foreign key constraint on the `user_equation` table to reference the unified `computational_graph` table instead of the now-deprecated `equation` table, ensuring data consistency with the new schema.
    - **Interactions**: These scripts are executed by Supabase to manage the database schema, ensuring the backend data model evolves correctly with the application's features.

### **Frontend UI Components (`src/components/`)**

- **`src/components/ui/` (Generic UI Components)**:
  
  - **`Button.tsx`**: A versatile button component with customizable `variant` (e.g., default, destructive, outline) and `size` props, styled using Tailwind CSS.
  - **`Card.tsx`**: A set of components (`Card`, `CardHeader`, `CardContent`, `CardFooter`) for structuring and displaying content in a visually distinct card format.
  - **`Input.tsx`**: A standardized input field component, ensuring consistent styling and behavior across the application.
  - **`Modal.tsx`**: A reusable modal component that displays content in an overlay, featuring customizable `title`, `children`, and `size` (e.g., sm, md, lg, xl) props, along with `isOpen` and `onClose` controls.
  - **Interactions**: These are fundamental building blocks for the application's user interface, promoting consistency and reusability.

- **`src/components/layout/`**:
  
  - **`Navbar.tsx`**: The application's top navigation bar.
    - **Key Functionality**: Displays the application logo and name, a search bar, navigation links (Equations, Graphs), and dynamically shows user authentication status (e.g., "Welcome, [Display Name]" with a Sign Out button, or Sign In/Sign Up links). It fetches the user's `display_name` from the `user` table.
  - **`Footer.tsx`**: The application's bottom section.
    - **Key Functionality**: Displays copyright information and basic navigation links (About, Contact, Privacy).
  - **Interactions**: These components provide a consistent layout and navigation experience across the entire application.

- **`src/components/math/MathRenderer.tsx`**:
  
  - **Purpose**: Renders mathematical expressions using KaTeX for LaTeX syntax and displays code snippets.
  - **Key Functionality**:
    - Takes `latex` (a LaTeX string) or `code` (a code string) as props.
    - If `latex` is provided, it uses `react-katex`'s `InlineMath` or `BlockMath` components to render the mathematical expression. It includes basic cleanup for LaTeX strings and a fallback display for parsing errors.
    - If `code` is provided, it renders the string within a `<code>` block, typically for displaying programming expressions.
  - **Interactions**: Used in various pages (e.g., `EquationBuilderPage`, `EquationListPage`, `ModelDetailPage`, `KnowledgeBasePage`) to visually represent mathematical content.

- **`src/components/equation/RunEquationModal.tsx`**:
  
  - **Purpose**: A modal component that allows users to input values for an equation's variables and calculate its result.
  - **Key Functionality**:
    - Fetches `model_variable` data associated with the equation (which is now an atomic `computational_graph`).
    - Dynamically generates input fields for variables with the `role: 'input'`.
    - Uses `math.js` (via the `evaluateExpression` helper) to parse and evaluate the equation's `expression_code` with the provided input values.
    - Displays the calculated result and any validation or calculation errors.
    - Includes fallback logic to extract variable symbols directly from the `expression_code` if variable definitions are not found in the database.
  - **Interactions**: Typically opened from `EquationListPage` or `EquationBuilderPage` to allow users to test individual equations.

- **`src/components/graphs/<mark>GraphCalculator</mark>.tsx`**:
  
  - **Purpose**: A component designed for calculating the output of a computational graph. (Note: While present, the `RunGraphModal` component often handles the primary graph execution logic in this project).
  - **Key Functionality**:
    - Takes a list of `GraphComponent`s and an `onCalculationComplete` callback.
    - Identifies the necessary user inputs by filtering out variables that are connected to outputs of other components within the graph.
    - Provides input fields for these external inputs.
    - The `calculateGraph` function iterates through the components in order, builds a scope of variables, and evaluates each component's expression using `math.js`.
  - **Interactions**: Could be integrated into a graph viewing or editing page to provide an interactive calculation interface.

- **`src/components/graphs/RunGraphModal.tsx`**:
  
  - **Purpose**: A modal component for executing and displaying the results of a computational graph, handling both atomic equations and composite graphs.
  - **Key Functionality**:
    - Fetches the `computational_graph` details, including its `compiled_graph` (the pre-compiled execution plan). If the graph is not compiled or is outdated, it triggers server-side compilation via `checkGraphCompilation` and `compileGraph`.
    - Determines the `graphInputs` (external variables that require user input) by analyzing the graph's components and their connections.
    - The `executeAtomicGraph` and `executeCompiledSteps` functions recursively traverse and evaluate the graph's components based on the compiled plan, using `math.js` for expression evaluation.
    - Displays the graph's execution plan, required input fields, intermediate results for each step, and the final output.
  - **Interactions**: Opened from `ModelsPage` or `ModelDetailPage` to allow users to run and observe the execution of computational graphs.

### **Frontend Pages (`src/pages/`)**

- **`src/pages/HomePage.tsx`**:
  
  - **Purpose**: The main landing page of the application.
  - **Key Functionality**: Features a hero section, highlights key features (Equation Builder, Computational Graphs, Knowledge Base, Collaboration), displays mock statistics, and includes calls-to-action for exploring equations or getting started.
  - **Interactions**: Serves as the initial entry point for users, providing an overview of the platform's capabilities.

- **`src/pages/auth/SignInPage.tsx`**:
  
  - **Purpose**: Allows existing users to sign in to their accounts.
  - **Key Functionality**: Provides input fields for email and password, a toggle to show/hide the password, and a submit button. The `handleSubmit` function calls the `signIn` method from `AuthContext` to authenticate the user with Supabase. It handles loading states and displays error messages.
  - **Interactions**: Interacts with `AuthContext` for authentication and `react-router-dom` for navigation after successful sign-in.

- **`src/pages/auth/SignUpPage.tsx`**:
  
  - **Purpose**: Allows new users to create an account.
  - **Key Functionality**: Provides input fields for display name, email, password, and confirm password, along with password visibility toggles. The `handleSubmit` function calls the `signUp` method from `AuthContext` to register the user with Supabase. It includes client-side validation for password matching and length, handles loading states, and displays success or error messages.
  - **Interactions**: Interacts with `AuthContext` for user registration and `react-router-dom` for redirection to the sign-in page upon successful account creation.

- **`src/pages/EquationBuilderPage.tsx`**:
  
  - **Purpose**: Enables users to create new or edit existing atomic mathematical equations. These are stored as atomic `computational_graph` entries in the database.
  - **Key Functionality**:
    - Manages state for equation details (name, LaTeX expression, code expression, description, public/private status, frozen status, tags).
    - Manages a dynamic list of `Variable` objects associated with the equation, allowing users to define symbols, names, units, roles (input, output, intermediate), and descriptions.
    - **`loadEquationVariables`**: Fetches existing variables for an equation when in edit mode.
    - **`validateUnit`**: Performs basic client-side validation for unit strings.
    - **`validateVariables`**: Ensures variables meet specific criteria (e.g., exactly one output variable, unique symbols).
    - **`handleSave`**: This crucial function handles both creation and updating. It inserts or updates the `computational_graph` entry (marked as `is_atomic: true`), and then manages the associated `variable` and `model_variable` entries, reusing existing variables where possible. It also triggers server-side graph compilation.
    - **`handleRunEquation`**: Opens the `RunEquationModal` to allow users to test the equation with inputs.
  - **Interactions**: Heavily interacts with `supabase` for data persistence, uses `MathRenderer` for live preview of expressions, and `RunEquationModal` for testing. It also uses `sessionStorage` to pass data when forking or editing an equation from the `EquationListPage`.

- **`src/pages/equations/EquationListPage.tsx`**:
  
  - **Purpose**: Displays a browsable list of all available atomic equations.
  - **Key Functionality**:
    - **`fetchAtomicGraphs`**: Retrieves `computational_graph` entries where `is_atomic` is true from Supabase, along with associated user (`assembler`) and citation information. It supports searching, filtering (all, public, starred), and sorting.
    - **`handleStarEquation`**: Allows users to "star" or "unstar" an equation, updating its status in the `user_equation` table.
    - **`handleViewEquation`**: Opens a detailed modal view for a selected equation and tracks the view in the `user_equation` table.
    - **`handleForkEquation`**: Prepares the selected equation's data and navigates to `EquationBuilderPage`, allowing the user to create a new equation based on an existing one. It also tracks the "used" relationship.
    - **`handleRunEquation`**: Opens the `RunEquationModal` for a specific equation.
    - **`handleEditEquation`**: Navigates to `EquationBuilderPage` to edit an equation, but only if the current user is the original creator (`assembler`).
    - **`handleCreateEquation`**: Navigates to `EquationBuilderPage` to start building a new equation from scratch.
  - **Interactions**: Interacts extensively with `supabase` for data fetching and updates, uses `MathRenderer` for displaying equations, and `RunEquationModal` for execution.

- **`src/pages/ModelsPage.tsx`**:
  
  - **Purpose**: Displays a list of all computational graphs (both composite and atomic).
  - **Key Functionality**:
    - **`fetchComputationalGraphs`**: Fetches `computational_graph` entries from Supabase, supporting search and filtering (all, public, private, starred). It includes mock counts for equations and variables within each graph.
    - **`handleDeleteGraph`**: Handles the deletion of a computational graph. This is a complex operation that first deletes all related records (e.g., `value_set`, `model_variable`, `computational_graph_component`, `graph_component`, `user_equation`) to satisfy foreign key constraints before deleting the graph itself. It requires user ownership verification.
    - **`handleCreateGraph`**: Navigates to the `ModelBuilderPage` (or `GraphBuilderPage`) to create a new graph.
    - **`handleRunGraph`**: Opens the `RunGraphModal` for a selected graph.
    - **`handleStarGraph`**: Toggles the "starred" status for a graph (currently a client-side mock, but designed for a `user_graph` table).
    - **`handleForkGraph`**: Creates a new computational graph by duplicating an existing one and its components, allowing users to customize it.
    - **`handleEditGraph`**: Navigates to `ModelBuilderPage` to edit an existing graph.
    - **`handleViewGraph`**: Navigates to `ModelDetailPage` to view graph details.
  - **Interactions**: Interacts with `supabase` for data management (fetching, deleting) and `RunGraphModal` for graph execution.

- **`src/pages/models/ModelDetailPage.tsx`**:
  
  - **Purpose**: Displays detailed information about a specific computational graph.
  - **Key Functionality**:
    - **`fetchModelDetail`**: Retrieves the `computational_graph` data, its `computational_graph_component`s (equations and nested graphs), and aggregates all unique variables used within the graph.
    - Displays graph metadata (name, description, creator, creation date, public/private status), key statistics (number of equations, nested graphs, variables), and provides tabs for an overview, a list of components (equations and nested graphs), and a list of variables.
    - **`handleRunModel`**: Opens the `RunGraphModal` to execute the displayed graph.
  - **Interactions**: Fetches data from `supabase`, uses `MathRenderer` for displaying expressions, and `RunGraphModal` for running the graph.

- **`src/pages/models/ModelEditPage.tsx`**:
  
  - **Purpose**: Allows users to edit the high-level metadata of a computational graph (name, description, public status). It explicitly states that component-level editing (adding/removing equations or nested graphs) should be done in the Graph Builder.
  - **Key Functionality**:
    - **`loadExistingGraph`**: Fetches the graph's current details for pre-filling the form. Includes a permission check to ensure the user is the assembler (creator) of the graph.
    - **`handleSave`**: Updates the `computational_graph` table with the modified metadata.
  - **Interactions**: Interacts with `supabase` for data fetching and updates. It serves as a simplified editing interface compared to the full Graph Builder.

- **`src/pages/graphs/ModelBuilderPage.tsx` (Consolidated Graph Builder)**:
  
  - **Purpose**: This is the central page for building new computational graphs or editing existing ones by adding, removing, reordering, and connecting equations and nested graphs. This file has been consolidated to handle both `GraphBuilderPage` and `ModelBuilderPage` functionalities.
  - **Key Functionality**:
    - Manages state for graph metadata (name, description, public status) and the dynamic list of `graphComponents` (equations or nested graphs).
    - **`loadExistingGraph`**: If an `id` is provided (for editing), it fetches the existing graph and its components, reconstructing the `graphComponents` state. It attempts to infer connections for loaded equations.
    - **`fetchAvailableEquations`**: Retrieves public equations that can be added as components.
    - **`fetchAvailableGraphs`**: Retrieves public computational graphs that can be added as nested components (excluding the current graph to prevent circular references).
    - **`addEquationToGraph`, `addGraphToGraph`**: Functions to add new components. If it's not the first component, it triggers the `Connection Modal` for equations to link inputs to previous outputs.
    - **`confirmConnections`**: Finalizes adding a component after connections are established in the modal.
    - **`updateConnection`, `removeConnection`**: Functions within the `Connection Modal` to manage the links between an input variable of the new component and an output variable of a previously added component.
    - **`removeComponent`, `moveComponent`**: Allow users to remove components or change their order in the execution flow.
    - **`updateGraphInputs`**: Identifies which variables in the graph require external user input (i.e., are not connected to an output from a preceding component).
    - **`calculateGraph`**: Executes the graph logic. It iterates through the `graphComponents` in their defined order, builds a scope of variables (from user inputs and connected outputs), and evaluates each equation's expression.
    - **`saveGraph`**: Handles both creating new graphs and updating existing ones. It inserts/updates the `computational_graph` entry and then manages the `computational_graph_component` entries (deleting old ones and inserting new ones) to reflect the current graph structure.
  - **UI**: Provides forms for graph details, a visual list of components with reordering and removal options, modals for selecting new components (equations or nested graphs), and a dedicated connection modal for linking inputs and outputs. It also includes a "Graph Inputs" section for user-provided values and a "Calculate" button to test the graph.
  - **Interactions**: This is one of the most complex frontend pages, interacting heavily with `supabase` for data persistence, `MathRenderer` for equation display, and managing intricate state for graph construction and calculation.

- **`src/pages/KnowledgeBasePage.tsx`**:
  
  - **Purpose**: Displays a browsable knowledge base of mathematical constants, variables, and units.
  - **Key Functionality**: Currently uses mock data for constants (e.g., speed of light, Pi), variables (e.g., Energy, Mass), and units (e.g., Kilogram, Meter).
  - **UI**: Features a search bar, tabs for filtering by type (Constants, Variables, Units), and a grid of cards displaying details for each item, including its symbol, name, value (for constants), unit, description, and category. It uses `MathRenderer` to display mathematical symbols.
  - **Interactions**: In a production environment, this page would typically fetch data from the `constant`, `variable`, `unit`, and `dimension` tables in the Supabase database.

- **`src/pages/CollaborationPage.tsx`**:
  
  - **Purpose**: A placeholder page for future collaboration features, such as shared projects and community discussions.
  - **Key Functionality**: Currently uses mock data for "Collaborative Projects" and "Community Discussions."
  - **UI**: Provides tabs to switch between projects and discussions, a search bar, and cards displaying mock project/discussion details.
  - **Interactions**: This page is a conceptual outline; a full implementation would involve significant backend development for real-time collaboration, project management, and discussion forums.

## **Overall Architecture Summary**

The application employs a **client-server architecture** with a **React frontend** and a **Supabase backend**.

- **Frontend (React, Vite, Tailwind CSS)**:
  
  - **Component-Based UI**: Built with reusable React components for modularity and maintainability.
  - **Client-Side Routing**: Managed by `react-router-dom` for seamless navigation.
  - **State Management**: Utilizes React's `useState` for local component state and `useContext` (via `AuthContext`) for global authentication state.
  - **Styling**: Leverages Tailwind CSS for a utility-first approach to styling, enabling rapid UI development and consistency.
  - **Mathematical Rendering**: Integrates KaTeX for high-quality display of LaTeX mathematical expressions.
  - **Build Tooling**: Vite provides a highly optimized development server and efficient production builds.

- **Backend (Supabase)**:
  
  - **PostgreSQL Database**: The core data store, housing all application data. Key aspects include:
    - **Unified Graph System**: The `computational_graph` table is central, serving as a polymorphic entity for both atomic equations (`is_atomic = true`) and composite computational graphs (`is_atomic = false`).
    - **Graph Composition**: The `graph_component` table defines the structure of composite graphs by linking parent graphs to their child components (which are themselves `computational_graph` entries, enabling nesting).
    - **Mathematical Entities**: `variable`, `unit`, and `dimension` tables define the fundamental mathematical building blocks.
    - **Variable Roles**: `model_variable` links variables to specific `computational_graph` entries and defines their `role` (input, output, intermediate) within that context.
    - **Social Features**: `user`, `citation`, `comment`, `comment_vote`, and `user_equation` tables support user accounts, academic citations, commenting, and user-specific relationships with equations/graphs.
  - **Authentication**: Supabase Auth provides robust user authentication capabilities, including registration, login, and session management.
  - **Row Level Security (RLS)**: Policies are meticulously defined to enforce fine-grained access control to database rows based on user roles and data ownership, ensuring data security.
  - **Database Functions & RPC**: PostgreSQL functions (e.g., `compile_graph` for server-side graph compilation, `auto_compile_parent_graphs` for automatic recompilation triggers) and Remote Procedure Calls (RPCs) expose server-side logic to the frontend, offloading complex computations from the client.
  - **Migrations**: SQL migration scripts manage the evolution of the database schema, ensuring version control and consistency.

- **Data Flow**:
  
  - Frontend components interact with the Supabase backend primarily through the `src/lib/supabase.ts` module, making API calls to perform CRUD (Create, Read, Update, Delete) operations on the database.
  - Authentication state is managed globally by the `AuthContext`, which keeps track of the current user's session.
  - Complex computational graph execution and compilation logic is handled on the Supabase backend via database functions, which are invoked by the frontend.
  - The `RunEquationModal` and `RunGraphModal` components demonstrate the execution flow: user inputs are collected, combined with the stored mathematical expressions, and evaluated using the `math.js` library (or a simplified evaluator for demonstration purposes).

This architecture provides a scalable and maintainable foundation for a complex mathematical modeling platform, leveraging the power of React for the frontend and Supabase for a comprehensive backend solution.





```json
[
	{
		"id": 12,
		"name": "[Dupont] Profit Margin",
		"step": 1,
		"type": "graph",
		"nested_steps": [
			{
				"id": 40,
				"name": "EBIT",
				"step": 1,
				"type": "atomic",
				"expression_code": "EBIT = OI - OpEx + NOI"
			},
			{
				"id": 34,
				"name": "Profit Margin",
				"step": 2,
				"type": "atomic",
				"expression_code": "PM = EBIT / OI"
			}
		]
	},
	{
		"id": 5,
		"name": "DuPont Top (to Asset Turnover)",
		"step": 2,
		"type": "graph",
		"nested_steps": [
			{
				"id": 38,
				"name": "Current assets",
				"step": 1,
				"type": "atomic",
				"expression_code": "A_C = A_OC + Inv + AR + CE"
			},
			{
				"id": 27,
				"name": "Assets",
				"step": 2,
				"type": "atomic",
				"expression_code": "A = A_F + A_C"
			},
			{
				"id": 32,
				"name": "Asset Turnover",
				"step": 3,
				"type": "atomic",
				"expression_code": "Turnover = OI / A"
			}
		]
	},
	{
		"id": 41,
		"name": "ROI",
		"step": 3,
		"type": "atomic",
		"expression_code": "ROI = AT PM"
	}
]
```

[{"id": 12, "name": "[Dupont] Profit Margin", "step": 1, "type": "graph", "nested_steps": [{"id": 40, "name": "EBIT", "step": 1, "type": "atomic", "expression_code": "EBIT = OI - OpEx + NOI"}, {"id": 34, "name": "Profit Margin", "step": 2, "type": "atomic", "expression_code": "PM = EBIT / OI"}]}, {"id": 5, "name": "DuPont Top (to Asset Turnover)", "step": 2, "type": "graph", "nested_steps": [{"id": 38, "name": "Current assets", "step": 1, "type": "atomic", "expression_code": "A_C = A_OC + Inv + AR + CE"}, {"id": 27, "name": "Assets", "step": 2, "type": "atomic", "expression_code": "A = A_F + A_C"}, {"id": 32, "name": "Asset Turnover", "step": 3, "type": "atomic", "expression_code": "Turnover = OI / A"}]}, {"id": 41, "name": "ROI", "step": 3, "type": "atomic", "expression_code": "ROI = AT PM"}]
