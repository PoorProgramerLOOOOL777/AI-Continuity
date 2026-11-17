
---
name: ai-continuity
description: Preserve project state and prepare a reliable handoff to another AI model when the current provider is unavailable, rate-limited, or out of quota.
---

# AI Continuity

## Purpose
Keep software and creative projects resumable across different AI models. Never claim that you can inspect hidden provider quotas or switch the current Claude session automatically unless an external supervisor actually reports that event.

## When to use
- The user says the current model is out of tokens, rate-limited, unavailable, or wants to continue with another model.
- Before a long task, checkpoint meaningful progress.
- At the end of a work session or before changing providers.

## Required workflow
1. Inspect the current repository and identify the actual project state.
2. Read:
   - `memory/project_context.md`
   - `memory/decisions.md`
   - `memory/completed_tasks.md`
   - `memory/pending_tasks.md`
3. Update these files with verified facts. Separate confirmed facts from assumptions.
4. Create a handoff using:
   `python -m continuity.cli handoff --summary "Resumen breve de la sesión"`
5. The handoff must include:
   - Project goal and current architecture.
   - Files changed and why.
   - Commands/tests run and their results.
   - Decisions and constraints.
   - Current blocker, if any.
   - Exact next action.
   - Relevant paths, but never secrets or API keys.
6. When continuing from another model, read `handoff/latest_handoff.md`, inspect the repository again, verify the status, and continue from the next action. Do not blindly trust stale notes.

## Provider fallback
The skill can prepare context for a fallback model. Actual provider switching is handled by an external router/supervisor, not by this markdown file. For an OpenAI-compatible gateway, configure `.env` and `config/models.json`, then use:
`python -m continuity.cli chat --prompt "Continúa con la siguiente tarea"`

If the gateway reports quota/rate-limit/server errors, the router tries the next enabled model. Authentication, permission, invalid-model, and malformed-request errors should be fixed rather than endlessly retried.

## Optional companion workflows
- Superpowers: use its planning, test-first, and review workflows where installed; record plans and outcomes in the project memory.
- I Have ADHD: present one immediate next action at a time, with short checkpoints, if the user has installed and enabled that workflow.
- Caveman: keep status updates concise when requested; do not omit critical technical details from handoffs.
- Headroom: use its context-compaction workflow if installed; preserve the full project facts and decisions in the handoff.

Do not invent companion commands, APIs, or capabilities. Detect whether each companion is installed and follow its own documentation.

## Safety
- Never expose or copy `.env`, credentials, access tokens, private keys, or personal data into a handoff.
- Ask before destructive operations, deployments, purchases, or changes to external accounts.
- Verify tests and file changes instead of claiming success without evidence.
