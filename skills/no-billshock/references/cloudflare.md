# Cloudflare: metered feedback paths

Read this reference **only** for relevant Cloudflare changes. Confirm latest plan-specific rules from official docs before using any numbers.

## Durable Objects (DO) alarms and storage

- Inspect `alarm()`, `setAlarm`, `getAlarm`, `deleteAlarm`, constructors and any checkpoint/lease/refresh repair path. A DO alarm can run with no HTTP request.
- Passing a timestamp at or before now to `setAlarm()` causes scheduling as soon as possible. Reusing the same stale due-time is a red flag. Persist state advancement and a meaningful next time before rescheduling, accounting for failure windows.
- Automatic retries of a thrown alarm and successful application-driven rescheduling are separate. A successful run scheduling another run may continue indefinitely.
- Alarm delivery can be at least once. Include idempotency, cross-instance/cross-tenant limits, dedupe, poison-state termination, and explicit stop behavior.
- `getAlarm()` state during active execution can differ from an idle object's pending alarm state. Check official semantics instead of inferring no work from one observation.
- Count billable SQLite/DO storage **rows read/scanned/written**, not just queries or returned rows; scheduling an alarm may contribute to writes. Many DO IDs can multiply per-object ceilings.

## Workers, Queues, Cron, Workflows and public proxies

- Follow Worker -> Queue/Workflow/DO -> Worker, Cron -> Worker -> Cron, webhook -> paid API -> webhook loops, and fan-out to many objects/tenants.
- Inspect retries, DLQs, delivery and concurrency controls, self-enqueue protections, expensive scans, paid upstream subrequests and bulk fetches.
- A website's **Free** plan and the **Workers** plan are distinct. Don't presume usage is free or that overage is capped without checking the account's actual plans/products.
- If a Worker authenticates or rate-limits a downstream origin, also secure **direct access** to that origin. Confirm Workers custom domains, routes, `workers.dev`, forwarding headers, and WAF fail modes in the actual configuration.
- Restrict upstream targets/redirects and hostile headers. Protect expensive paid origins against untrusted callers independently of CDN rate limits.

## Operational proof

- Code guards: per-run and per-window work limits, persisted disable state, valid next-schedule time, terminal state.
- Tests: virtual-clock advancement past *all* refresh/TTL boundaries, no-traffic schedule ceilings, duplicate/restart scenarios, direct-origin bypass.
- Environment: inspect actual analytics and verified alarms for DO requests, execution, read/write rows and subrequests; document how to stop scheduled alarms, queue consumers and Cron, including already-enqueued items.
- Alert emails are **not** equivalent to a hard cost cap and may arrive after usage occurred.

## Primary documentation

- https://developers.cloudflare.com/durable-objects/api/alarms/
- https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/
- https://developers.cloudflare.com/durable-objects/platform/pricing/
- https://developers.cloudflare.com/workers/platform/pricing/
- https://developers.cloudflare.com/workers/platform/limits/
- https://developers.cloudflare.com/queues/platform/pricing/
- https://developers.cloudflare.com/billing/billing-policy/
