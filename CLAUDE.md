# Forge Autonomous Build Protocol

## Project
- **Name:** A countdown timer
- **Project ID:** 26d5f4f8-f4b8-4b98-b03f-80d7fe969179
- **Branch:** forge/build-v12
- Contract batch: latest

## MCP Servers Available
You have 5 MCP servers connected. Use them throughout the build:
- **forgeguard** — Build tracking (`forge_start_build`, `forge_log_build`, `forge_update_phase`, `forge_report_file`, `forge_complete_build`)
- **devmcp** — Governance contracts (`dev_read_contract`) and project contracts (`dev_read_project_contract`)
- **forgebench** — Code validation (`bench_validate`, `bench_pattern`, `bench_standards`)
- **forgeobs** — Build observability (`obs_health`, `obs_tail`)
- **forgememory** — Persistent memory (`memory_read`, `memory_write`, `memory_goals`)

## Build Protocol

Execute these phases in order. Report progress frequently via `forge_log_build` so the user can monitor in real-time.

### Phase 0: Initialize
1. Call `forge_start_build` with `branch="forge/build-v12"` to register this build session.
2. Call `forge_log_build` with `message="Build started"`, `source="system"`.
3. Call `memory_read` with `zone="lessons"` to load lessons from previous builds.
4. Call `memory_goals` to check active project goals.

### Phase 1: Read Governance
Read the builder contract and understand the rules:
- `dev_read_contract(name="builder_contract")` — Master governance rules
- `dev_read_contract(name="session_protocol")` — Session workflow rules

Follow ALL rules in the builder contract throughout the build.

### Phase 2: Read Project Contracts
Fetch the contracts that define what to build:
- `dev_read_project_contract(contract_type="blueprint")`
- `dev_read_project_contract(contract_type="boundaries")`
- `dev_read_project_contract(contract_type="builder_directive")`
- `dev_read_project_contract(contract_type="integration_snapshot")`
- `dev_read_project_contract(contract_type="manifesto")`
- `dev_read_project_contract(contract_type="physics")`
- `dev_read_project_contract(contract_type="schema")`
- `dev_read_project_contract(contract_type="stack")`
- `dev_read_project_contract(contract_type="ui")`

Study these carefully. They define the project's architecture, schema, API endpoints, UI, boundaries, and phased delivery plan.

### Phase 3: Parse Phases
From the `phases` contract, identify each phase and its:
- Objective and deliverables
- Files to create
- Schema tables touched
- Exit criteria (testable checkpoints)

### Phase 4+: Execute Each Phase
For each phase in order:

1. **Announce** — `forge_update_phase(phase_number=N, phase_name="...", status="started")`
2. **Plan** — Determine which files to create/modify for this phase
3. **Code** — Write the files
   - Before each file: `forge_report_file(file_path="...", status="generating")`
   - After each file: `forge_report_file(file_path="...", status="created")`
   - Log progress: `forge_log_build(message="...", source="coder")`
4. **Validate** — Check code quality
   - `bench_validate(content=<code>, file_type="router|service|model|...", technology="python")`
   - Fix any issues flagged with score < 80
5. **Test** — Run tests if a test framework is configured
   - Check `forge.json` for test commands
   - All tests must pass before moving on
6. **Verify** — 4-step verification per the builder contract:
   - Static: syntax/lint checks pass
   - Runtime: application boots
   - Behavior: tests pass
   - Contract: boundaries and schema respected
7. **Commit** — Commit changes for this phase with a descriptive message
8. **Complete** — `forge_update_phase(phase_number=N, phase_name="...", status="completed")`

### Completion
After all phases:
1. Run the full test suite one final time.
2. `forge_complete_build(status="completed", summary="<brief summary of what was built>")`
3. `memory_write(zone="lessons", content="<key lessons from this build>")` — Record what you learned.
4. `memory_write(zone="session_history", content="<compressed session summary>")` — Record what was done.

### Error Handling
If a phase fails:
1. Log the error: `forge_log_build(message="Phase N failed: <reason>", source="system", level="error")`
2. Attempt to fix the issue (up to 3 retries per phase).
3. If unrecoverable: `forge_complete_build(status="failed", error_detail="<what went wrong>")`

## Rules
- Follow the builder contract from Phase 1 rigorously.
- Use `forge_log_build` frequently — the user is watching progress in real-time.
- Commit after each completed phase, not at the end.
- Validate every file with `bench_validate` before considering it done.
- Do NOT skip phases or reorder them.
- If you encounter an ambiguous requirement, make a reasonable decision and log it.
