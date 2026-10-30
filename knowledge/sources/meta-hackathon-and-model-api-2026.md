---
id: source-meta-hackathon-and-model-api-2026
type: source
title: Meta Hackathon and Model API Evidence — October 2026
summary: Official event and Meta API documentation retrieved on 2026-10-26; judging weights and bonus details remain secondary-only because the official details page was not text-readable.
status: active
created: '2026-10-26'
updated: '2026-10-26'
topics:
  - hackathon
  - llm
confidence: medium
relations:
  - type: supports
    target: note-meta-hackathon-build-plan
---

# Meta Hackathon and Model API Evidence — October 2026

## Scope and provenance

Research date: **2026-10-26**. Evidence supports the proposed plan in [[note-meta-hackathon-build-plan]]. This record distinguishes organizer statements, official product documentation, and secondary reporting. It is not a copy of the legal rules and does not establish the user's eligibility or API access.

The official event landing page, requested details page, Meta model/tool/structured-output docs, and secondary event guide were fetched directly with readable-page retrieval. Independent research also consulted Meta's event announcement and API access documentation. No authenticated account, event application, provider setup, model inference, or contest submission occurred.

## S1 — Official event landing page

- Publisher: Meta and Cerebral Valley (event organizers).
- Title: Meta Global AI Developer Hackathon.
- URL: https://cerebralvalley.ai/e/meta-ai-developer-hackathon
- Retrieved: 2026-10-26; readable body available.

### Theme wording

> “Build for Your World. Bring Meta's models into your domain. Solve a problem you know firsthand, free up time and mental space, and make something possible that wasn't before.”

> “Push the Frontier. Use Meta's models to tackle challenges in software, robotics, manufacturing, energy, materials and beyond. Give a machine a new capability, accelerate a scientific experiment, or unlock a better way to understand and control a physical system. Show us what becomes possible when these models meet the real world.”

### Confirmed event facts

- Virtual event, October 26–November 4, 2026; advertised cash pool $1,000,000 across two participant tracks.
- Applications opened October 13, 9 AM ET; deadline October 25, 11:59 PM ET, possibly earlier at the 20,000-accepted-participant cap.
- Approval notifications by October 26, 9 AM ET; kickoff October 26; workshops and office hours October 27–November 4.
- Project submissions due November 4 by 9 PM ET; judging November 4–8; closing ceremony/live finals November 9.
- Dates may change at Meta's sole discretion. Use official current information when scheduling submission. The page mixes EST in its header and ET in its schedule; avoid relying on an October header-time conversion. November 4, 9 PM ET is November 5, 02:00 UTC under the stated 2026 date.
- Free entry if selected; eligibility exclusions apply. Being able to read the event page does not establish acceptance.
- Indie developer lens: “creativity, technical ambition, and whether it works.” Startup lens: “technical execution and whether it holds up in production.” These are not numeric weights.
- Application selection has two equally weighted criteria: project idea and technical skill. **These are application-selection weights, not the project-judging rubric.**
- Named tools: Muse Spark series, Muse Wonder, Muse Image, SAM 3.1 through Meta Model API; Meta open-weight models; Muse Code.
- Inference partners are mentioned on the event page. Their presence does not establish a particular model endpoint's availability or the user's entitlement to credits.
- Landing-page statement: official rules would be published before the October 26 start and must be accepted by selected participants. This is not evidence that the detailed rules were successfully retrieved here.

## S2 — Requested official details and anchors

- Publisher: Cerebral Valley / organizers.
- URL: https://cerebralvalley.ai/e/meta-ai-developer-hackathon/details
- User-specified judging anchor: https://cerebralvalley.ai/e/meta-ai-developer-hackathon/details#8-judging-process-16
- User-specified bonus anchor: https://cerebralvalley.ai/e/meta-ai-developer-hackathon/details#bonus-prizes-from-meta-50-k-20
- Retrieved: 2026-10-26; HTTP 200, event title/description available, extracted body only **“Loading...”**.

**Limitation:** text retrieval did not expose the judging process, bonus rules, or full waiver. No browser inspection was performed. The page is not proven absent or empty; its contents were inaccessible through this retrieval method. Read the actual accepted rules/participant materials before relying on legal or award conditions.

## S3 — Secondary event guide, not verified primary rules

- Publisher: ReconScribe.
- Title: Meta AI Developer Hackathon 2026: Global, $1M Prizes, Dates.
- URL: https://reconscribe.com/meta-global-ai-developer-hackathon-2026/
- Retrieved: 2026-10-26; sections on schedule, prizes, eligibility, submissions, and judging directly read. The page describes its underlying rules information as available as of October 17; it can be stale even though fetched later.

The guide attributes the following weights to the event waiver:

| Criterion reported by the guide | Reported weight |
| --- | ---: |
| Impact | 30% |
| Use of Meta AI Tooling | 25% |
| Demo | 25% |
| Technical Depth and Execution | 20% |

It reports a working demo and demo video, Indie teams up to four, individual application/acceptance for each member, and originality/ownership/licensing conditions. Exact video duration, repository/public-demo requirements, and final official submission fields were not established. Do not infer that the guide's generic definition of a hackathon as “from scratch” is an event rule banning prior work.

The guide reports startup prizes totaling $550,000, Indie prizes totaling $400,000, and **up to $50,000 in bonus prizes**. It says possible bonus categories include community vote or most viral project; categories, number, and individual amounts are not fixed in its account. It reports bonus announcements on or about November 10, distinct from the landing page's November 9 closing ceremony. All of these detailed bonus conditions remain secondary-only here.

**Do not promote this reporting into confirmed organizer terms.** It is enough to motivate a rule-verification checklist and a provisional rubric mapping, not a claim that the project qualifies for an award. External-model restrictions, prior-work eligibility, final team limits, and complete official submission requirements remain unresolved.

## S4 — Official Meta model catalogue

- Publisher: Meta.
- Title: Models — Meta Model API.
- URL: https://dev.meta.ai/docs/models
- Retrieved: 2026-10-26; readable body directly reviewed.

Relevant statements:

- Muse Spark 1.3 (`muse-spark-1.3`) is documented as the latest Spark version and recommended for new work; versions 1.2 and 1.1 also listed.
- Muse Spark and Muse Wonder support text output, tool calling, structured output, and multimodal inputs. Those input modalities are not required for the proposed text-first demo.
- Muse Wonder is in preview; its API and Muse Code availability differ by variant. A coding-agent subscription does not imply API access to every variant.
- Hosted models use Meta Model API; the examples use `https://api.meta.ai/v1` and a server-side `MODEL_API_KEY`.
- Model availability can vary by country. The API model-list endpoint reveals models enabled for a team; account availability must be verified, not assumed from a public catalogue.
- Muse Spark Open is a separately deployed open-weight release (816B total, 42B active parameters); it is not called through Meta Model API. Muse Glimmer is also described as open-weight/self-hosted.
- Standard vs Contributor data-use modes differ. Do not send private plant data without permission and review of current terms.

**Planning implication:** prefer one verified event-aligned hosted Meta model for the initial build. Llama is not established as required. Do not self-host a huge model merely to make the integration look more technical.

## S5 — Official Meta tool calling

- Publisher: Meta.
- Title: Tool calling — Meta Model API.
- URL: https://dev.meta.ai/docs/tool-calling
- Retrieved: 2026-10-26; readable body directly reviewed.

Critical statements:

> “The model does not execute developer-defined tools itself. Your app handles execution for every tool you define in tools.”

> “Regardless of strict, the model's generated arguments are guided by your parameters schema but are not guaranteed to validate against it.”

> “Only ‘auto’ (the default) is supported on both Chat Completions and the Responses API.”

- The docs recommend Responses for multi-turn tool loops, while supporting Chat Completions too. Tool definition and tool-result formats differ between endpoints.
- `strict: true` on a function tool validates that its declared schema fits a subset; it does not guarantee generated argument validity.
- Multiple/parallel calls may occur. Client-defined tool loops require application-side bounds; built-in `max_tool_calls` is not a substitute for a bound on all developer tools.
- Call IDs/results must be matched correctly.

**Planning implication:** validate every tool argument; allowlist components; never rely on forced tool choice; show no verified number without a completed deterministic run.

## S6 — Official Meta structured output

- Publisher: Meta.
- Title: Structured output — Meta Model API.
- URL: https://dev.meta.ai/docs/structured-output
- Retrieved: 2026-10-26; readable body directly reviewed.

- Documented schema-constrained decoding applies to structured-output responses, unlike the weaker function-tool-argument guarantee.
- Recursive schemas are unsupported. Flat node and edge arrays fit the bounded graph proposal better than nested recursive definitions.
- Responses parameter: `text.format`; Chat Completions parameter: `response_format`. Passing the other endpoint's field does not configure the intended feature.
- Current schema limits include depth 10, total 5,000 properties, string-length and enum limits; strict mode supports a subset rather than every JSON Schema construct.
- Schema validity is not semantic correctness. A valid enum/string/array does not prove a sensible physical model or compatible edge.

**Planning implication:** use structured output for proposals and typed error repair, followed by compiler/runtime checks. Test the actual account, model, schema, and endpoint combination early.

## Additional official references read during research

- Meta event context: https://developers.meta.com/blog/meta-connect-recap/
- API overview: https://dev.meta.ai/docs/overview
- API quickstart/access path: https://dev.meta.ai/docs/quickstart
- Open-weight deployment context: https://dev.meta.ai/docs/muse-spark-open/deploy

These support the integration research but do not substitute for the event's official rules or a successful authenticated access test.

## Service discovery and remaining uncertainty

A Gravity Index lookup for the exact direct Meta inference need returned no recommendation or supported alternatives (search ID `494cba95-9c53-448d-8ed3-17e6a18a8968`). No provider was provisioned or integrated. This catalogue gap does not mean Meta's documented API is unavailable; it means no catalogue-backed setup recommendation was established.

Before implementation, resolve: acceptance/track/team eligibility, official judging and bonuses, prior-work policy, final submission requirements, permitted model routes and external models, actual API/geographic access, enabled model IDs, credits, current API behavior, and data-use settings. Revisit this evidence if those inputs change. No inaccessible primary material has been reconstructed as a quotation.
