# NoBillShock

**Because AI doesn't pay your cloud bills.**

[中文说明](README.zh-CN.md) | [Skill](skills/no-billshock/SKILL.md) | [Contributing](CONTRIBUTING.md) | [License](LICENSE)

A **focused, cross-agent coding skill** that helps prevent unexpected pay-as-you-go bills caused by uncontrolled Cloudflare Workers / Durable Objects, AWS Lambda, and similar serverless workflows.

The skill is deliberately **narrowly triggered**. It is intended to run when an agent creates, changes, reviews or deploys a code path with a credible cost-amplification risk. It should **not** activate for every reference to AWS, every simple HTTP request, UI changes or unrelated refactoring.

> [!IMPORTANT]
> This skill provides engineering guidance and deployment gates, **not** a financial guarantee, billing limit or automatically installed cloud firewall. A coding agent needs sufficient access and authorization to implement or verify cloud controls. A budget email is not a hard spending cutoff.

## Why this exists

A serverless function that schedules itself, retries indefinitely, re-enqueues messages or accepts unbounded requests can generate charges long after a release looks healthy.

A real-world failure pattern: a Durable Object checkpoint with a 30-day TTL and a refresh beginning 7 days before expiration can appear safe for about 23 days. Once its refresh window opens, a stale alarm timestamp can cause an autonomous loop of wakeups and metered storage operations. Initial smoke tests will not reveal this.

The guard prompts coding agents to trace and **bound** these chains, test virtual time transitions and verify kill switches before declaring a deployment ready.

## What it covers

| Risk | Examples of checks |
| --- | --- |
| Autonomous rescheduling | `alarm()`, `setAlarm()`, cron, timed jobs, checkpoint/TTL refresh |
| Feedback loops | Lambda -> S3 -> Lambda; Worker -> Queue -> Worker; recursive webhooks |
| Unbounded amplification | retries, fan-out, large scans, storage writes, downstream paid AI/API calls |
| Untrusted public traffic | Cloudflare proxy forwarding to a publicly callable Lambda Function URL |
| False sense of safety | reserved concurrency mistaken for a cost cap; budget alerts mistaken for circuit breakers |
| Delayed failures | day-23 refresh of day-30 checkpoint; leases and expired timestamps |
| Runtime containment | persistent task limits, dead-letter states, usage monitoring and independently tested stops |

Not a general-purpose cloud-security, FinOps, performance or infrastructure-design skill.

## How the agent behaves

**Automation first**:

1. Trace the affected metered execution graph, including triggers, retries and downstream services.
2. Implement practical **code-level** guardrails and tests.
3. Prefer existing IaC or authorized cloud APIs/CLI for infrastructure-side limits, origin authentication, alerts and kill switches.
4. Before modifying production resources, permissions, spending or availability, obtain required authorization. Don't silently deploy or raise quotas.
5. Verify applied protections. If access is missing, **do not claim they are enabled**. List exact user actions and remaining risk.
6. Report the deployment gate: `BLOCKED`, `NEEDS VERIFICATION` or `READY FOR REVIEW`.

**Manual steps are a fallback**, not the skill's primary output. This distinction is intentional: it is for **coding agents**, not an operator checklist.

### When it should and should not activate

| Prompt / work item | Expected |
| --- | --- |
| "Change the Durable Object alarm to refresh checkpoints before TTL expires" | Activate |
| "Implement an SQS retry loop in Lambda" | Activate |
| "Add a public Cloudflare Worker proxy to a billable Lambda URL" | Activate |
| "Review this worker for unbounded paid API calls" | Activate |
| "Update the application's login page CSS" | **Do not** activate |
| "What is AWS Lambda?" | **Do not** activate |
| "Fix a spelling mistake in Cloudflare documentation" | **Do not** activate |
| "Refactor an unrelated Rails model in a repo that also contains Lambda" | **Do not** activate |

Only the `name` and `description` are initially offered to supporting agents. When selected, the agent loads `SKILL.md`. Cloudflare and AWS references are **loaded only when relevant**. Exact automatic selection still depends on the agent's skill implementation and prompt.

## Repository layout

```text
no-billshock/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .github/workflows/validate.yml
├── examples/
│   ├── activation-tests.md
│   ├── expected-report.md
│   └── optional-repo-instructions.md
├── scripts/
│   └── validate.py
└── skills/
    └── no-billshock/
        ├── SKILL.md
        └── references/
            ├── aws-lambda.md
            └── cloudflare.md
```

The installable skill is the **whole `skills/no-billshock/` directory**. Copy it with its `references/` subdirectory; do not copy just `SKILL.md`.

## Install with your AI coding agent (recommended)

Ask Claude Code, Codex, Cursor, or Antigravity to install NoBillShock for you. An agent with terminal and filesystem access can fetch the repository, select the supported Skills directory, install the complete skill, and verify the result.

Paste the prompt below into the coding agent where you want NoBillShock installed. It uses the current project by default. Change `PROJECT` to `GLOBAL` for a user-level installation that other local projects can discover.

```text
Install the NoBillShock coding-agent skill from:
https://github.com/ZPVIP/no-billshock

Installation scope: PROJECT (the currently open repository).
# Change PROJECT to GLOBAL to install for my user account instead.

Do the installation, not just explain the steps:
1. Identify the current coding agent (Claude Code, Codex, Cursor, or
   Antigravity), operating system, and applicable skill directory.
   If the scope or target repository is unclear, ask before writing files.
2. Fetch the named GitHub repository and review the contents of
   skills/no-billshock/ before installing. Use the supported Skills CLI
   if appropriate and approved, or a temporary git clone plus a safe copy.
   Install the entire folder, including SKILL.md and references/.
3. Use this agent's actual PROJECT or GLOBAL discovery path, as documented
   in the repository README. Do not assume all agents use the same path.
4. If no-billshock is already installed, inspect the existing version and
   differences; ask before overwriting it. Do not delete unrelated skills.
5. Verify SKILL.md has name: no-billshock, required references are present,
   and the installed path is discoverable. State whether I must restart
   the agent session to refresh skill discovery.
6. Report the target agent, scope, exact installed path, installation
   method, and verification results. If you lack permissions or network
   access, report the blocker instead of claiming success.

This is an installation-only task. Do not run the skill's cloud checks,
edit my application, change AWS/Cloudflare settings, or deploy anything.
```

The agent might ask for permission to access the network, run an external package, or write to a user-level directory. Review those requests before approving them. Installing a Skill only makes it **available for future tasks**; it does not run a cloud safety review or grant access to AWS or Cloudflare.

<details>
<summary><strong>Manual installation options</strong></summary>

### Install with the Skills CLI

If Node.js and npm are available, you or your coding agent can alternatively use the community [Skills CLI](https://github.com/vercel-labs/skills). Run these commands **inside the target application repository** for project scope:

```bash
# Interactive installation: choose your coding agent when prompted.
npx skills add "ZPVIP/no-billshock" --skill no-billshock

# Example: install directly for Codex in this project.
npx skills add "ZPVIP/no-billshock" --skill no-billshock -a codex

# Example: install globally for Claude Code.
npx skills add "ZPVIP/no-billshock" --skill no-billshock -a claude-code -g
```

Supported agent selectors include `claude-code`, `codex`, `cursor`, `antigravity`, and `antigravity-cli`. Add `-g` only for user-level installation. The CLI chooses directories according to its supported-agent mapping, which may change with versions; check the actual destination and agent discovery after installation. The CLI is an external npm package, **not bundled with NoBillShock**. Review and approve external package execution before using `npx`. The manual installation instructions below do not require Node.js.

### Install by copying the skill files

#### 1. Obtain this repository

Clone the repository:

```bash
git clone "https://github.com/ZPVIP/no-billshock.git"
cd no-billshock
```

Or download and extract GitHub's **Code -> Download ZIP**, then enter the extracted repository directory. All following commands assume the shell's current directory is **this repository root**, not the target application's root.

#### 2. Choose project vs global scope

| Agent | Project-level destination (inside target repo) | User-level destination (on your machine) |
| --- | --- | --- |
| **Claude Code** | `.claude/skills/no-billshock/` | `~/.claude/skills/no-billshock/` |
| **Codex** | `.agents/skills/no-billshock/` | `~/.agents/skills/no-billshock/` |
| **Cursor** | `.agents/skills/` or `.cursor/skills/` + skill name | `~/.agents/skills/` or `~/.cursor/skills/` + skill name |
| **Antigravity IDE / 2.0** | `.agents/skills/` + skill name | `~/.gemini/config/skills/` + skill name |
| **Antigravity CLI** | `.agents/skills/` + skill name | `~/.gemini/antigravity-cli/skills/` + skill name |

**Project-level** skills can be committed with the app and shared with collaborators. **Global** skills are installed for one user and are discoverable across local projects. Installing globally does **not** force invocation for every task.

The shared `.agents/skills/` project path works for **Codex, Cursor and Antigravity**; Claude Code requires `.claude/skills/` (or another supported Claude customization mechanism).

#### 3. Project-level installation (macOS/Linux)

Set `TARGET` to the absolute path of your **application repository**, then run **from this skill repository root**:

```bash
TARGET="$HOME/path/to/my-app"  # change this
mkdir -p "$TARGET/.agents/skills"
cp -R skills/no-billshock "$TARGET/.agents/skills/"
```

That single installation covers **Codex, Cursor and Antigravity**. For **Claude Code** too, either make a symlink to the same source:

```bash
mkdir -p "$TARGET/.claude/skills"
ln -s ../../.agents/skills/no-billshock \
  "$TARGET/.claude/skills/no-billshock"
```

Or copy a separate skill folder if symlinks are unavailable:

```bash
mkdir -p "$TARGET/.claude/skills"
cp -R skills/no-billshock "$TARGET/.claude/skills/"
```

**Important:** the symlink command assumes the `TARGET/.claude/skills` and `TARGET/.agents/skills` layout shown above. Do not run it if the destination already exists. Review files before committing a third-party skill into your product repo.

#### 4. Global installation (macOS/Linux)

Run the appropriate command(s) from this skill repository root:

**Claude Code:**

```bash
mkdir -p "$HOME/.claude/skills"
cp -R skills/no-billshock "$HOME/.claude/skills/"
```

**Codex:**

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/no-billshock "$HOME/.agents/skills/"
```

**Cursor (local):**

```bash
mkdir -p "$HOME/.cursor/skills"
cp -R skills/no-billshock "$HOME/.cursor/skills/"
```

For local Cursor, you can instead use the Codex-style `~/.agents/skills/` location. **For Cursor Cloud Agent sync**, use `~/.cursor/skills/` and enable **Settings -> Agents -> Sync Skills for Cloud Agents** if supported by your plan/setup. Cursor does not automatically sync `~/.agents/skills/`.

**Antigravity IDE / 2.0:**

```bash
mkdir -p "$HOME/.gemini/config/skills"
cp -R skills/no-billshock "$HOME/.gemini/config/skills/"
```

**Antigravity CLI:**

```bash
mkdir -p "$HOME/.gemini/antigravity-cli/skills"
cp -R skills/no-billshock "$HOME/.gemini/antigravity-cli/skills/"
```

These are separate *global* discovery directories, unlike the common project path. You can replace copies with carefully checked symlinks if your agent version supports following them. Avoid duplicate skills of the same name in multiple paths visible to one agent.

#### 5. Windows (PowerShell)

From the downloaded skill repository root, use a single command block per agent or project. Windows uses different user-home path syntax, but each skill still contains `SKILL.md` and `references/`:

```powershell
# Example: project-level common install for Codex, Cursor, Antigravity
$target = 'C:\path\to\my-app'   # change this
New-Item -ItemType Directory -Force -Path "$target\.agents\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$target\.agents\skills\"

# Optional: Claude Code project-level copy (no symlink/admin privileges needed)
New-Item -ItemType Directory -Force -Path "$target\.claude\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$target\.claude\skills\"
```

For **global** installation, replace `$target` with the relevant absolute home-directory destination:

```powershell
# Example: global Claude Code
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$HOME\.claude\skills\"

# Other global destinations:
# Codex:          "$HOME\.agents\skills"
# Cursor:         "$HOME\.cursor\skills"
# Antigravity IDE "$HOME\.gemini\config\skills"
# Antigravity CLI "$HOME\.gemini\antigravity-cli\skills"
```

To use another global destination, create that directory and run the corresponding `Copy-Item` command. If you already have a skill folder with this name, remove/rename or update it intentionally before copying, rather than nesting a second folder inside it.

#### 6. Verify installation

Check the installed directory for `SKILL.md` and both reference documents. Start a **new agent session** if the agent does not immediately discover a newly installed skill.

Ask the coding agent:

```text
Review the Durable Object alarm refresh path for runaway billing risk.
Use the no-billshock skill and only local mocks/fake clocks.
Do not deploy anything.
```

It should read `SKILL.md` and the **Cloudflare** reference. Then test a non-trigger:

```text
Change the button color in this UI component.
```

The billing skill should not activate. See [activation examples](examples/activation-tests.md).

</details>

## How to use the skill

### Automatic selection

For a scoped high-risk coding task, a compatible agent can automatically choose the skill based on its `name` and `description`. You do **not** need to paste the long guidance into global instruction files.

### Explicit invocation

For an audit, say:

```text
Use no-billshock to review the changed Lambda/SQS retry path.
Find any unbounded billable work, implement tests and safe code guards,
and report what remains unconfigured in AWS. Do not alter production.
```

Claude Code and Antigravity support `/no-billshock` when the skill is installed and discoverable. Cursor exposes installed skills through Agent and may allow `/` selection. In Codex you can explicitly mention the skill by name or use the skill picker supported in your installed version. Invocation UX can vary by version; normal natural-language naming is portable.

### Stronger project enforcement (optional)

If your repository frequently modifies queues, alarms, Lambda or paid backend entry points, insert just a *short* conditional instruction into a repo-level `AGENTS.md` (Codex and other agents that read it), `CLAUDE.md` (Claude Code), or corresponding agent rules file:

```text
Before editing or deploying self-scheduling/retrying serverless workloads,
metered event-feedback paths, or publicly exposed routes to paid backends,
invoke no-billshock. Skip unrelated and bounded one-shot work.
```

Do **not** copy the entire Skill into an always-loaded system/agent instruction file. See [optional integration patterns](examples/optional-repo-instructions.md). For Claude Code, avoid relying on `AGENTS.md` alone; use `CLAUDE.md` for this instruction if needed.

### Example output / deployment semantics

See [example review report](examples/expected-report.md). There are three separate concepts:

- **AUTO-IMPLEMENTED**: code, tests or IaC changes the agent actually made.
- **APPLIED AND VERIFIED IN CLOUD**: controls it confirmed exist in a real environment, only when authorized and accessible.
- **USER ACTION REQUIRED**: missing permissions, unavailable features or required approvals with exact remaining work.

`READY FOR REVIEW` is **not** a promise of zero risk, and never implies permission for an unrequested production deployment.

## Updating or uninstalling

To **update** an installation, review upstream changes, then replace the installed skill folder with `skills/no-billshock/`. Copying on top of an existing folder can leave obsolete files behind; remove the old copy or use a verified sync operation after backing up local modifications.

To **uninstall**, remove only the exact installed `no-billshock` directory/symlink in the chosen per-agent location. Do not delete the parent `skills/` directory if it contains other skills. Remove optional `AGENTS.md` / `CLAUDE.md` references you added separately.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Agent cannot see skill | Folder name, `SKILL.md` frontmatter, correct scope, session restart, cloud/remote agent filesystem |
| Agent activates on every task | Remove unconditional global instructions, check accidental duplication, ensure current `description` is installed |
| Agent never activates | Ask explicitly by name; confirm task has a real amplification path; check supported agent version |
| Claude doesn't see `.agents/skills` | Claude Code's native project location is `.claude/skills`; copy/symlink there |
| Cursor Cloud Agent lacks global skill | Only selected user-level skills in `~/.cursor/skills` are eligible for cloud sync; repository skills work in cloned repositories |
| Cloud config was not changed | Agent may lack credentials, permission or user approval. Read `USER ACTION REQUIRED`, never assume "planned" means "applied" |
| Existing account has only 100 unreserved Lambda concurrency | Positive Reserved Concurrency may be rejected due to AWS's 100-unreserved minimum; request quota changes only after understanding increased exposure |

## Validation and CI

The package has no runtime dependencies, no credential requirements and **no automatic production API calls**. Validate it locally:

```bash
python3 scripts/validate.py
```

The GitHub Actions workflow runs the same static validation. It checks metadata, expected references, local Markdown links, packaging conventions and a few key policy invariants. It is **not** proof that your own serverless project is protected.

## Limitations

- Providers change pricing, request quotas, account features, retry semantics and agent discovery paths. Verify current official documentation for the target account/region.
- A skill is **advisory**. Agents can miss triggers, make mistakes or be denied needed permissions. Always review infrastructure changes and test kill switches independently.
- Monitoring and emailed budget alerts may lag. A CDN rate limit does not automatically protect a publicly reachable AWS origin.
- Finite concurrency is not a finite cost ceiling, and a limit in one service does not limit downstream billable calls.
- This repository contains **instructions only**, not a deployed cloud policy, provider account integration or automatic cost monitor.

## Official references

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Google Antigravity skills](https://www.antigravity.google/docs/skills)
- [Cloudflare Durable Object alarms](https://developers.cloudflare.com/durable-objects/api/alarms/)
- [AWS Lambda concurrency](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html)

## Contributions and license

Issues and pull requests are welcome, especially corrections to provider behavior and install paths. See [CONTRIBUTING.md](CONTRIBUTING.md). Released under the [MIT License](LICENSE).
