# LLM-computed steps (allowed for this request)

The operator allows bounded in-context calculation for gaps no eligible model covers: the environment flag is active. A required dependency with no eligible model may be filled by exactly one llm step that computes it from already-available inputs; the runtime executes it separately through a priced call and marks the run partially grounded.

Rules:

- Use a step ONLY for a required dependency with no eligible model. Never replace a satisfiable model binding with a step, and never use a step to recall a fact the question does not supply.
- Bind step inputs exactly like model inputs (facts or upstream node or step IDs, no literals). Every input must already be available from the facts or an upstream instance.
- Declare the output meaning, unit, and context to match what the downstream input (or the requested answer) needs. The runtime validates the computed number against this port and rejects anything else.
- The instruction states the arithmetic relationship using ONLY the bound inputs: name the operations in words over the given amounts. It must not request outside facts, recalled constants, lookup values, estimates, or judgments. If a constant is needed, it must come from a bound fact or an upstream value.
- At most 3 steps per graph; steps count toward the node budget. Graph outputs may reference step IDs. List steps in any order; the runtime sorts execution itself.
- Prefer fewer steps; prefer the step whose inputs are satisfiable with the fewest gaps. Explain each step choice in reason.
