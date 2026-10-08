---
name: no-billshock
description: >-
  Focused cost-runaway protection when creating, editing, reviewing, or deploying
  metered serverless execution paths that can repeat, self-trigger, retry,
  fan out, scan/write metered storage, or accept untrusted traffic. Trigger for
  Cloudflare Durable Object alarms, Workers cron/queues, AWS Lambda event loops,
  recursive webhooks, unbounded paid API calls, and public proxies to billable
  origins. Check persistent work limits, delayed TTL boundaries, origin bypass,
  usage alerts, kill switches, and safe deployment gates. Do not use for ordinary
  bounded one-shot requests, general AWS/Cloudflare questions, unrelated code,
  UI, documentation, or low-risk refactors.
license: MIT
metadata:
  version: "1.2.0"
---

# NoBillShock

## Scope and activation gate

This is a **narrow cost-amplification review for coding agents**, not a generic cloud review or a manual operations tutorial. Activate for changes/reviews/deployments that plausibly cause uncontrolled *metered work*:

- `alarm()` / `setAlarm()`, timers, cron, delayed TTL or checkpoint refresh, polling, queues, retries, event consumers, feedback paths, workflows or webhooks.
- Dynamic fan-out, recursive invocation, unbounded database reads/writes, pay-per-call APIs, inference/token consumption or other billable downstream effects.
- **New or changed** public endpoints, proxies or routing rules that can invoke a metered origin; check direct-origin bypass and untrusted clients.
- An explicit user request for runaway-serverless-cost auditing.

**Do not activate** merely because a repository imports an AWS/Cloudflare SDK or contains an unchanged Worker. If invoked but no plausible amplification path exists in the requested scope, say "No new cost-amplification path found" and stop.

Read `references/cloudflare.md` **only** for Cloudflare workloads. Read `references/aws-lambda.md` **only** for Lambda or its AWS triggers. Read both only for cross-provider flows. For other services use the general protocol, verifying vendor-specific limits in current primary documentation.

## 1. Trace the billable execution graph

Inspect changed code *and* its callers, event sources, side effects, retry paths, and external access. Map:

`entry/clock/event -> handler -> billable reads/writes/API -> retry/reenqueue/reschedule -> next event`

Determine whether tasks run without traffic; whether one invocation creates multiple future invocations; whether one tenant/client can multiply work; whether old/past timestamps are reused; and whether the metered origin can be called without passing through a CDN or proxy. Distinguish a platform's automatic retry cap from application-scheduled **new** work.

## 2. Implement bounded work in the actual system

Choose appropriate enforceable limits and implement them in code/configuration whenever possible:

- Explicit terminal states; maximum attempts, recursion depth, fan-out, messages, batches, scanned rows, API calls, work per tenant and per time window. Backoff or a concurrency setting by itself does **not** impose a spending ceiling.
- Persistent or externally enforced limits. In-memory counters disappear on process restart; per-instance limits do not bound an unbounded number of instances.
- Validated next-run times and time budgets. Reject past/non-finite/impossible schedules; don't repeatedly enqueue the same expired checkpoint. Ensure durable progress/atomic state transitions where supported.
- Idempotency, deduplication and bounded at-least-once retries, including overlapping consumers, crashes, partial completion and poison messages. Add dead-letter/terminal handling.
- Authentication/authorization and rate limits at the **metered origin** as well as the edge when relevant. Verify raw Function URLs, `workers.dev`, direct origin endpoints and alternate routes.
- An independent, documented emergency stop (feature flag, disabled trigger/producer, permissions, concurrency zero where available). Verify persisted alarms, backlogs and already-running work will actually stop.

Long-running recurring services may be legitimate. Bound their **work per run and per time window**, not merely the interval between runs.

## 3. Quantify exposure without inventing financial guarantees

Identify chargeable invocations, runtime/memory, read/scanned/write rows, queue operations, storage, egress/logs, AI tokens, and downstream providers. Estimate work **per accepted event and per hour/day**, including idle scheduled work, repeats and hostile traffic:

`max_work <= max_accepted_events * max_fanout * max_attempts * max_billable_ops_per_attempt`

Count autonomous scheduled events independently. Use verified, region/plan-specific prices or label them unverified. If a bound is missing, say "Unbounded/unknown". **Free-tier, reserved concurrency, budget email, WAF and rate limiting are not necessarily monetary hard stops.**

## 4. Automation-first, with explicit human approval boundaries

The agent must do the engineering work; do **not** respond with a checklist of manual tasks when implementation is possible.

1. Implement scoped safeguards and tests directly in the repository first.
2. If authorized, prefer existing IaC, provider APIs or CLI tools to configure alerts, quotas, access controls, trigger limits and stop controls. Follow repository conventions; avoid creating competing infrastructure definitions.
3. Do **not** silently change production infrastructure, spend commitments, permissions, resource availability or deployment state. Obtain approval when authorization is missing or a change is destructive, paid, production-affecting or outside the task scope.
4. Never claim that a protection is active merely because a config file, README, console instruction or alert proposal exists. Distinguish **implemented in code**, **applied in environment**, and **verified operational**.
5. When blocked by missing permissions, credentials, plan features, quota restrictions or approval: record **NOT CONFIGURED**, explain the remaining exposure and give concrete operator steps. Don't pretend the action succeeded.
6. Do not bypass safeguards, raise concurrency/account quotas, or add paid services merely to silence a check.

## 5. Test long-delayed and failure scenarios safely

Use fake clocks, mocks or test doubles. **Never launch high-volume loops or load tests on production** as a way to validate a guard.

- Test TTL/checkpoint states before, at and after each refresh/expiry boundary, including weeks after deployment; test stale and skewed timestamps.
- Simulate no-traffic autonomous execution, duplicate delivery, race/restarts, partial effects, transient/permanent errors and poison messages.
- Assert finite ceilings: `scheduled_events <= N`, `attempts <= N`, `rows_scanned <= N`, `paid_calls <= N`, and `no_schedule_after_terminal`.
- Verify unauthenticated bursts and direct-origin bypass cannot invoke expensive work unchecked.
- Test the emergency stop with mocks and bound the number of additional billable operations after activation.

If tests could not be run, describe what was **not** tested and why.

## 6. Production readiness gate and structured handoff

Before a production deployment involving a changed amplification path, classify:

- **BLOCKED**: plausible unbounded paid loop, uncontrolled paid fan-out, bypassable origin with unbounded expensive work, or no credible emergency stop. Don't auto-deploy.
- **NEEDS VERIFICATION**: implementation looks bounded, but required infrastructure, live permission, alert delivery or shutdown behavior has not been verified. Do not label it safe.
- **READY FOR REVIEW**: relevant limits, tests and required controls are implemented and verified to the extent access permits. This is not a guarantee of a dollar ceiling or authorization to deploy.

Report using this structure, concise for low-risk changes:

```text
Serverless cost-safety: BLOCKED | NEEDS VERIFICATION | READY FOR REVIEW
Changed paid path(s): ...
Worst-case work: ... (bound, assumptions, unknowns)
AUTO-IMPLEMENTED: ... (files/config and tests with actual results)
APPLIED AND VERIFIED IN CLOUD: ... (evidence, or NONE VERIFIED)
USER ACTION REQUIRED: ... (NOT CONFIGURED, exact steps and impact)
Kill switch and direct-origin exposure: ...
Deployment decision: ... (production deployment not assumed authorized)
```

## Failure pattern this skill addresses

A Durable Object checkpoint with a 30-day TTL and a 7-day refresh window can appear healthy until ~day 23. A successful `alarm()` that schedules another already-due alarm can continue indefinitely; the exception-retry cap does **not** limit newly scheduled alarms. Review delayed state transitions and repeated scheduling even when deployment-day tests pass.
