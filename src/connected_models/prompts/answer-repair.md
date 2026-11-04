## Repair round

Your previous proposal for this same question failed when the runtime checked or executed it. The user message carries the original question and models plus `prior_proposal` (exactly what you sent) and `machine_error` (the runtime's precise failure).

Fix the proposal: keep the parts the error does not name, change what it names. Frequent fixes: bind a fact whose unit converts to the target port instead of one that cannot; pick the eligible model whose input meanings and contexts the available facts or upstream outputs actually satisfy; correct a misspelled input name, model key, or fact reference; drop a node whose required input has no source.

Return a complete fresh proposal in the same schema (facts, issues, status, graph, reason, clarifications) — not a diff. Same grounding rules: no invented values, no in-context arithmetic, no raw literals in bindings.

If no eligible model can satisfy a required binding even in principle — for example every candidate reports a meaning/context mismatch and no alternative model exists — do not repeat a failing graph. Return status `unresolved` with a reason naming the missing bridge, or `needs-input` with plain-language clarification questions when a user-supplied value could unblock it. Binding and validation errors name models, ports, or facts: never reinterpret them as ambiguity in the question, which is unchanged since your last proposal.
