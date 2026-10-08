# Example agent handoff (illustrative, not a real deployment result)

Suppose an agent reviews a changed Cloudflare Worker proxy to AWS Lambda. The Worker runs in a free plan; Lambda uses a public Function URL, and the agent cannot access the AWS account.

```text
Serverless cost-safety: NEEDS VERIFICATION

Changed paid path(s): public Worker route -> Lambda Function URL -> metered DB read

Worst-case work:
  Code caps requests to the known allowed paths and methods.
  Direct-origin AWS invocations: UNKNOWN (public Function URL still accessible)
  Maximum daily DB reads: UNKNOWN until origin authorization is verified.

AUTO-IMPLEMENTED:
  - Added route/method allowlist (src/proxy.ts)
  - Added early input validation (src/proxy.ts)
  - Added direct-origin threat-model tests (test/proxy.test.ts)
  - 12 local unit tests passed (illustrative example only)

APPLIED AND VERIFIED IN CLOUD:
  - NONE VERIFIED. No production credentials were available.

USER ACTION REQUIRED:
  - NOT CONFIGURED: set Lambda Function URL AuthType to AWS_IAM and
    implement SigV4 signing from Worker if compatible with architecture.
  - NOT VERIFIED: origin invocation permissions and usage alarms.
  - Owner must approve changes to production availability and permissions.

Kill switch and direct-origin exposure:
  Disable the public origin or revoke invoke permission after approval.
  No kill-switch action was performed.

Deployment decision:
  Do not mark protection operational or deploy automatically.
  Approval and cloud verification required.
```

The agent should not claim this report applies to your project without inspecting and running your code. The skill reports observed state and unknowns rather than inventing safeguards or costs.
