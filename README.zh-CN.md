# NoBillShock

**Because AI doesn't pay your cloud bills.**

防止 AI 编写的 Serverless 代码引发意外高额云账单。

[English README](README.md) | [Skill 正文](skills/no-billshock/SKILL.md) | [许可证](LICENSE)

一个面向 **Claude Code、Codex、Cursor、Google Antigravity** 等 AI Coding Agents 的精准触发 Skill，防止 Cloudflare Workers / Durable Objects、AWS Lambda 以及其他 Serverless 平台因为死循环、重复调度、队列重试、公开接口滥用等原因产生意外高额账单。

> **重要：** Skill 是开发和审查指南，不是云平台的实际费用硬上限。它不会在安装后自动配置 AWS/Cloudflare 账户，也不能保证账单归零。

## 设计目标

这个 Skill 只在变更或审查 **存在按量计费放大风险的执行路径** 时才应该被加载，例如：

- Durable Object `alarm()` 不断 `setAlarm()` 自我唤醒。
- Lambda 写入 S3 之后又触发自己，或者 SQS 消费失败后反复入队。
- TTL / checkpoint 过期窗口在上线 20 多天之后才触发异常。
- Cloudflare Worker 将公开请求转发至计费的 Lambda Function URL，而 AWS 原始入口仍能被直接调用。
- 大量 fan-out、无上限分页/扫描、反复调用付费 AI/API 服务。

**不应触发：** 普通 CSS/UI 工作、文档修改、单次有明确边界的 API 调用、一般云计算概念问答，或只因为仓库里出现了 `aws` / `cloudflare` 关键字。

Agent 在选择 Skill 前通常仅看到 `name` / `description`，选中后才读取 `SKILL.md`。AWS 和 Cloudflare 的详细参考文件也按需加载，而不是每次读完全部内容。

## Agent 负责什么？哪些事需要人做？

此版本坚持 **Automation first，优先自动实施**：

1. 先检查完整调用链，辨别是否存在无界的重试、定时、自触发和收费操作。
2. 在代码中自动增加执行上限、持久化终止状态、幂等防重、时间边界校验、自动化测试等适用保护。
3. 有授权时优先通过项目现有的 Terraform/CDK/CloudFormation、云 API 或 CLI 实施控制和告警。
4. **生产环境、账户费用/配额、权限、可用性等高影响变更，必须遵守用户授权和批准要求。** 不允许偷偷部署或为了通过检查而提高并发配额。
5. 无法操作时，以 `NOT CONFIGURED` 标明，并在提交/部署前清楚列出人工配置步骤、剩余风险和阻断状态。
6. 不允许把“已经写在 README 里的配置办法”谎称成“云平台已经配置并验证”。

最终报告区分 **AUTO-IMPLEMENTED**、**APPLIED AND VERIFIED IN CLOUD**、**USER ACTION REQUIRED**，并给出 `BLOCKED` / `NEEDS VERIFICATION` / `READY FOR REVIEW`。最后一种也不代表保证不会花钱。

## 目录结构

```text
no-billshock/
├── README.md                      # 英文完整说明
├── README.zh-CN.md                # 中文说明
├── LICENSE
├── CONTRIBUTING.md
├── .github/workflows/validate.yml
├── examples/                      # 触发测试与报告范例
├── scripts/validate.py             # 静态校验工具
└── skills/
    └── no-billshock/
        ├── SKILL.md
        └── references/
            ├── cloudflare.md
            └── aws-lambda.md
```

安装时必须复制 **整个** `skills/no-billshock/` 文件夹，包括 `references/`。

## 安装路径（已针对各平台核对）

| Agent | 项目级（项目根目录下） | 全局（当前用户） |
| --- | --- | --- |
| Claude Code | `.claude/skills/no-billshock/` | `~/.claude/skills/no-billshock/` |
| Codex | `.agents/skills/no-billshock/` | `~/.agents/skills/no-billshock/` |
| Cursor | `.agents/skills/` 或 `.cursor/skills/` 后接 Skill 名 | `~/.cursor/skills/` 或 `~/.agents/skills/` 后接 Skill 名 |
| Antigravity IDE / 2.0 | `.agents/skills/` 后接 Skill 名 | `~/.gemini/config/skills/` 后接 Skill 名 |
| Antigravity CLI | `.agents/skills/` 后接 Skill 名 | `~/.gemini/antigravity-cli/skills/` 后接 Skill 名 |

**项目级**：适合交给团队共同使用，可将 Skill 与源代码一同提交 Git。

**全局**：适合自己所有本地项目使用。全局安装只是“可被发现”，并不代表每次编程都自动加载全文。

### 下载仓库

发布 GitHub 后，将 `YOUR_GITHUB_USERNAME` 替换成自己的 GitHub 用户或组织名称：

```bash
OWNER=YOUR_GITHUB_USERNAME
git clone "https://github.com/${OWNER}/no-billshock.git"
cd no-billshock
```

也可以选择 GitHub 上的 **Code -> Download ZIP**，解压后进入仓库根目录。以下命令默认在**本 Skill 仓库根目录**执行。

### 项目级安装：同时用于 Codex / Cursor / Antigravity

macOS / Linux：

```bash
TARGET="$HOME/path/to/my-app"  # 修改成实际应用项目绝对路径
mkdir -p "$TARGET/.agents/skills"
cp -R skills/no-billshock "$TARGET/.agents/skills/"
```

额外给 Claude Code 创建符号链接，保证四种 Agent 只维护一份：

```bash
mkdir -p "$TARGET/.claude/skills"
ln -s ../../.agents/skills/no-billshock \
  "$TARGET/.claude/skills/no-billshock"
```

这条相对符号链接仅适用于上述目录结构。若目标文件夹已存在，不要直接覆盖。Windows 或不能使用符号链接时，可以另外复制一份：

```bash
mkdir -p "$TARGET/.claude/skills"
cp -R skills/no-billshock "$TARGET/.claude/skills/"
```

### 全局安装：macOS / Linux

从本 Skill 仓库根目录，按照使用的 Agent 选择执行：

```bash
# Claude Code
mkdir -p "$HOME/.claude/skills"
cp -R skills/no-billshock "$HOME/.claude/skills/"

# Codex
mkdir -p "$HOME/.agents/skills"
cp -R skills/no-billshock "$HOME/.agents/skills/"

# Cursor（若需要同步到 Cursor Cloud Agents，建议用此位置）
mkdir -p "$HOME/.cursor/skills"
cp -R skills/no-billshock "$HOME/.cursor/skills/"

# Antigravity IDE / 2.0
mkdir -p "$HOME/.gemini/config/skills"
cp -R skills/no-billshock "$HOME/.gemini/config/skills/"

# Antigravity CLI
mkdir -p "$HOME/.gemini/antigravity-cli/skills"
cp -R skills/no-billshock "$HOME/.gemini/antigravity-cli/skills/"
```

Codex 与 Cursor 本地模式可共用 `~/.agents/skills/`。但 Cursor 要将个人 Skill 同步到 Cloud Agent 时，一般需要放进 `~/.cursor/skills/`，并在 Settings -> Agents 中启用相关同步选项。Antigravity IDE 和 Antigravity CLI 的全局目录**不同**。

### Windows PowerShell 安装

在 Skill 仓库根目录运行：

```powershell
# 项目级：Codex / Cursor / Antigravity
$target = 'C:\path\to\my-app'  # 修改路径
New-Item -ItemType Directory -Force -Path "$target\.agents\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$target\.agents\skills\"

# 项目级：Claude Code
New-Item -ItemType Directory -Force -Path "$target\.claude\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$target\.claude\skills\"

# 全局示例：Claude Code
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force '.\skills\no-billshock' "$HOME\.claude\skills\"
```

其他全局目录依次是 `$HOME\.agents\skills` (Codex)、`$HOME\.cursor\skills` (Cursor)、`$HOME\.gemini\config\skills` (Antigravity IDE) 和 `$HOME\.gemini\antigravity-cli\skills` (Antigravity CLI)。将上述全局示例中的目录替换即可。目标文件夹已存在时先明确是更新还是覆盖，避免多套重复安装。

## 如何使用

安装后最好重新启动 Agent 会话，让它发现 Skill。

**自动触发示例：**

```text
Please change our Durable Object checkpoint refresh logic so that
expired checkpoints are refreshed safely. Write fake-clock tests.
```

**明确要求使用：**

```text
Use the no-billshock skill to audit the Lambda/SQS
retry path. Implement code guardrails and tests, but do not deploy or
modify production infrastructure. Report missing cloud controls.
```

Claude Code 和 Antigravity 可通过 `/no-billshock` 手动调用可见 Skill。Cursor 通常可从 Agent 的 Skills 或 `/` 菜单选择。Codex 可以在对话中直接引用 Skill 名称，具体快捷方式依版本变化。

**验证不会乱触发：**

```text
Please update the button background color in this React component.
```

普通 CSS 改动不应该加载这个 Skill。更多正反测试例子见 [examples/activation-tests.md](examples/activation-tests.md)。

### 可选：要求关键任务必须运行

频繁涉及 Serverless 的项目，可在 `AGENTS.md`（适用 Codex 等）或 `CLAUDE.md`（Claude Code）只加入下面的短规则：

```text
Before editing or deploying self-scheduling/retrying serverless workloads,
metered event-feedback paths, or publicly exposed routes to paid backends,
invoke no-billshock. Skip unrelated and bounded one-shot work.
```

不要把整个 `SKILL.md` 复制到全局常驻的 `AGENTS.md` 或 `CLAUDE.md`，那会违背精准加载的设计。完整示例见 [examples/optional-repo-instructions.md](examples/optional-repo-instructions.md)。

## 从旧名称升级

如果之前安装了使用旧名称的版本，请删除旧 Skill 文件夹，并移除 `AGENTS.md` / `CLAUDE.md` 中指向旧名称的可选触发规则，再安装 `no-billshock/`。不要保留两个名称的副本，否则可能重复触发或使用不同版本。

## 更新、卸载和验证

更新：重新复制最新的 `skills/no-billshock/` 文件夹。建议先备份并删除旧副本，避免遗留失效文件。

卸载：只删除对应 Agent 安装位置下的 `no-billshock` 文件夹或其符号链接，不要删除其他 Skills。再删除额外加入的可选项目路由指令。

本仓库提供静态验证，无需云平台密钥：

```bash
python3 scripts/validate.py
```

CI 也运行同样的检查。它只验证 Skill 文件和仓库结构，不能证明实际 AWS/Cloudflare 账户已经安全。

## 注意事项

- 不使用 Cloudflare Durable Objects，也可能因为公开代理转发、Lambda 递归触发或下游按量收费 API 而产生风险。
- AWS Lambda Reserved Concurrency 只限制同时执行的数量，不限制每月调用次数或账单金额。
- Cloudflare / AWS 的预算邮件有延迟，不能当成实时熔断。
- 修改生产配额、权限、停机、部署前必须遵守授权流程。Agent 不能假装自己完成了无权限执行的操作。
- 该 Skill 无后台守护进程，不会主动登录云平台或为你监控账单。

## 官方文档

- [Agent Skills 规范](https://agentskills.io/specification)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Cursor Skills](https://cursor.com/docs/skills)
- [Antigravity Skills](https://www.antigravity.google/docs/skills)

欢迎通过 Issue / PR 改进。开源许可证为 [MIT](LICENSE)。
