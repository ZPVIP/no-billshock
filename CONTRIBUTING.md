# Contributing

Contributions are welcome, especially corrections to provider semantics, platform-specific installation paths, false-positive trigger wording and cases where an agent claimed a protection was active without verifying it.

## Before opening a PR

1. Keep the activation boundary narrow. Adding a provider's name alone should **not** cause unrelated changes to trigger this skill.
2. Put provider details in `skills/no-billshock/references/`, not in the frontmatter description or an always-loaded policy.
3. Back provider-specific claims with an up-to-date **official documentation URL**. Don't hardcode price numbers without effective dates, region and plan assumptions.
4. Keep code changes as the preferred agent outcome. If a task requires operator action, mark it unconfigured and explain how it affects production readiness.
5. Don't introduce automated cloud calls, required credentials, mandatory production load tests or scripts that change accounts.
6. Update English and Chinese READMEs when changing install paths, commands or scope.
7. Add or update entries in `examples/activation-tests.md` if trigger semantics change.
8. Run `python3 scripts/validate.py` and include the result in the PR.

## Scope of issues

Please include the affected agent/version, provider and plan, a minimal **sanitized** reproduction, expected and observed behavior, and an official reference where applicable.

**Never post:** AWS access keys, Cloudflare tokens, account identifiers, private Function URLs, customer data, proprietary source code or bills containing personal details. For sensitive security findings, privately contact repository maintainers through their GitHub profile or a repository security advisory if enabled.

## Release / compatibility

The project follows the portable Agent Skills format. Avoid platform-exclusive metadata in the main `SKILL.md`. Test across agent vendors where possible. `metadata.version` is informational; it does not make clients automatically update installed copies.

## Licensing

By contributing you agree to publish your contribution under the repository's MIT License.
