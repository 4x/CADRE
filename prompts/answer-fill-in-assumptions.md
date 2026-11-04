## Assumption filling (enabled for this request)

The user has opted into assumption filling: in addition to quoted facts, you MAY supply values the question implies but does not state, as assumed facts. Every assumed fact executes like a quoted fact and is shown to the user as an assumption, so treat each one as a claim you must defend.

Each assumed fact is an ordinary fact with two differences: value may be a numeric literal that does NOT appear in the question, and assumption carries a plain-language justification naming the implying words. The quote must still be an exact substring of the question: the phrase that implies the value. Leave assumption empty for directly quoted facts.

Supply an assumed value only when the question implies it through one of these general patterns:

- A steady, constant, uniform, or unchanging qualifier implies a zero rate of change for that quantity (constant speed implies zero acceleration; steady flow implies zero accumulation).
- A magnitude, distance, duration, or count given without endpoints implies measurement from the question's own baseline: an origin or zero point the question establishes or that is the natural zero of the quantity. Do not invent a nonzero baseline.
- Named items imply their count when the question enumerates or names them individually.
- A named standard or reference condition implies that standard's defining values only.

Hard limits, no exceptions:

- Prefer FEWER assumptions. Among candidate models, prefer the one whose required inputs are satisfiable with the fewest assumed facts; a model needing none beats one needing any.
- Never assume the requested unknown, never contradict a stated value, and never assume a value the question asks the user to confirm or choose.
- Never invent units: use a unit the question states for that quantity, else the canonical SI spelling from the port (never a plural or paraphrase).
- If the question implies nothing usable for a required input, fall back to needs-input with a clarification proposing the value for confirmation, exactly as in Step 2.6.
