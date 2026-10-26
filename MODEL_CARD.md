# Model / system card

## Intended use

Execute a model-proposed tool plan through an allowlisted dispatcher with strict budgets and an audit trail. Educational local experiment; no production deployment is implied.

## Data

Synthetic arrays, manually written documents or replayed JSON. No real user records. Seeds and sample inputs are recorded in app.py and sample_input.json.

## Method

Live mode requests a JSON plan from a local LLM; fixture mode replays a supplied plan. Validate a maximum of four calls, permitted tools and exact argument schemas. A calculator parses a restricted arithmetic AST; document search uses the local corpus.

## Evaluation protocol

Test unknown tools, excessive call counts and unsafe calculator expressions. Execute the sample plan and record each tool observation. This is plan-then-execute orchestration, not an autonomous open-ended agent.

## Known limits

The planner is not live-tested in this build. Tool permission checks are real, but no browser, shell, network search or filesystem-writing tool is provided.

## Verification status

Local tests and default experiment are executed during packaging. Live model generation is not exercised in the build. A successful validation result is limited to the checks implemented in code.

## Further work

Add observation-conditioned replanning, per-tool deadlines, human confirmation for side effects, budget accounting and adversarial plan evaluations.
