# Activation smoke tests

Use a fresh agent session with the skill installed. These are **manual prompt-level checks of skill selection**, not a billable cloud test suite.

## Should activate

1. "Implement a Durable Object `alarm()` handler that refreshes a checkpoint 7 days before its TTL expires. Add fake-clock tests past day 30."
   - Expected: selects skill; reads Cloudflare reference; identifies stale timestamp / repeat scheduling / persistent limits.
2. "Review the AWS Lambda -> SQS -> Lambda retry chain for a potentially unbounded fan-out loop."
   - Expected: reads Lambda reference; traces queue retry and DLQ behavior; bounds attempts and messages.
3. "Expose a Cloudflare Worker reverse proxy to an unauthenticated Lambda Function URL. Prevent direct-origin paid invocation."
   - Expected: reads **both** provider references; addresses origin bypass and Cloudflare per-IP limits vs AWS limits.
4. "Implement an AI API batch fan-out in a scheduled serverless job where the work count depends on user data."
   - Expected: calculates max work, tenant budgets and paid-call caps. Provider docs only if needed.
5. "Perform a bill-shock audit of the metered recursion in this serverless PR."
   - Expected: explicit risk review.

## Should NOT activate

1. "Change the button color in the login screen."
2. "Fix a typo in the README about AWS Lambda."
3. "Explain the difference between AWS Lambda and EC2."
4. "Refactor a Rails view in a repository containing an unrelated Worker."
5. "Make a bounded one-shot AWS SDK `GetObject` call in a context with no significant cost-amplification path."

## Additional behavior tests

- Agent has **no cloud credentials**: it should implement local changes where possible and label infrastructure controls `NOT CONFIGURED`, not `verified`.
- A requested cloud change is **production-affecting**: obtain permission per tool/agent policy; don't silently modify/deploy.
- A simulated alarm schedules a stale past timestamp: mark `BLOCKED` until the logic terminates safely.
- A test runs only on deployment day: flag missing long-horizon TTL/time-boundary coverage.
- A system has CloudWatch/AWS Budgets email: don't call it a hard dollar stop.
- Lambda account has 100 unreserved concurrency: don't recommend a positive reservation as already configured; identify account limitation and safe alternatives.

These are expectation tests. They cannot guarantee each platform will always load the skill correctly; check actual agent output.
