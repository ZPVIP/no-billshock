# AWS Lambda: metered feedback paths

Read this reference **only** for relevant AWS Lambda or Lambda trigger changes. Verify region/account settings and current official docs for limits and prices.

## Event sources and recursion

- Map Function URL/API Gateway/ALB -> Lambda; EventBridge schedules/rules; SQS/SNS; S3 notifications; DynamoDB Streams; Step Functions; asynchronous invocations/destinations; Lambda-to-Lambda invokes.
- Watch for Lambda writing to the same S3 prefix/bucket that triggers it, publishing a message consumed by itself, re-enqueueing failed work, or fan-out to downstream services that trigger the original function.
- AWS recursive-loop detection is useful defense-in-depth but does **not** cover every service, SDK, custom API and event-chain shape. Do not assume it is a universal stop.
- Configure per-event source retry count, maximum record age, batch behavior, DLQ/on-failure destination and visibility timeout where supported. Validate the dead-letter path does not return to the source.

## Public Lambda URLs and limits

- Function URL `AuthType=NONE` with a permissive resource policy may allow direct invocations, bypassing Cloudflare/WAF. Protect the **AWS origin**, ideally with IAM/SigV4 or another pre-invocation access control where suitable.
- An application-layer shared header checked *inside* Lambda can block expensive business work, but does not stop the anonymous request from invoking Lambda and incurring invocation overhead.
- **Reserved concurrency is not a monthly/daily request or spending cap**. It bounds simultaneously running instances. `0` can throttle new invocations if the configuration is available, but existing work and downstream queued work may still require action.
- AWS Lambda reserves at least 100 regional concurrency for unreserved functions. If unreserved is already 100, a positive reserved-concurrency allocation will be rejected until quotas/reservations permit. Never increase regional concurrency solely to make an example pass without considering exposure.
- Check whether an event source is synchronous, async or poll-based: throttling and retry/queue behavior differ; dropped/throttled calls can also cause upstream retry costs.

## Monitoring, automation and emergency stop

- Alert on Lambda `Invocations`, `Duration`, `Errors`, `Throttles`, async age, SQS backlog, DLQ count and billable downstream operations (DynamoDB, RDS, S3, AI APIs, CloudWatch Logs).
- Use IaC/provider APIs to configure where authorized. Verify resources exist in the target account, Region and environment. `AWS Budgets` and cost anomaly emails are useful but delayed; not an immediate hard billing cutoff.
- Identify at least one independently actionable stop procedure: disable event source mapping/EventBridge rule, revoke invoke permissions, stop producers, isolate a queue, or reduce reserved concurrency to zero where possible. Verify the stop for *that specific trigger type*.
- Bound events per time window, work/invocation, retries and expensive downstream actions. Function timeout and small concurrency alone do not impose a dollar ceiling.

## Primary documentation

- https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html
- https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html
- https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html
- https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html
- https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
- https://aws.amazon.com/lambda/pricing/
