# Optional repo-level routing instructions

**Default:** install the Skill; don't add any of these lines unless your team wants stronger selection guarantees for risky changes.

The following are **short routing hints**, not a duplicate copy of the Skill. Keep them conditional so unrelated work remains lightweight.

## In a repository's `CLAUDE.md` (Claude Code)

```text
When creating, modifying, reviewing, or deploying a self-scheduling or retrying
serverless path, a metered event-feedback path, or a newly public paid origin,
use no-billshock before deployment. Skip unrelated edits.
```

## In a repository's `AGENTS.md` (Codex and tools that read this file)

```text
For changes to metered serverless alarms, cron, queues, retries, paid fan-out,
or publicly accessible billable endpoints, invoke no-billshock.
Do not invoke it for unrelated or bounded one-shot work.
```

## In Cursor / Antigravity

The skill's frontmatter should be sufficient for normal discovery. If a particular workspace has a consistent selection failure, add a single conditional hint to that agent's **existing** workspace rules, rather than creating a broad always-on instruction to read the entire skill. Rules/settings vary by agent version.

## What not to add

```text
Always read no-billshock/SKILL.md at the start of every task.
```

This unconditional rule defeats progressive disclosure and should be avoided.
