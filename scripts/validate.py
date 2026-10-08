#!/usr/bin/env python3
"""Dependency-free static checks for this Agent Skills repository.

No credentials, network requests, deployments, or paid API calls.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL_FOLDER = ROOT / "skills/no-billshock"
SKILL_PATH = SKILL_FOLDER / "SKILL.md"
EXPECTED = [
    SKILL_PATH,
    SKILL_FOLDER / "references/cloudflare.md",
    SKILL_FOLDER / "references/aws-lambda.md",
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "LICENSE",
    ROOT / "CONTRIBUTING.md",
    ROOT / "examples/activation-tests.md",
    ROOT / "examples/expected-report.md",
    ROOT / "examples/optional-repo-instructions.md",
]
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def verify_markdown_links(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    # Simple local Markdown links, excluding image links and raw URLs.
    for link in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", content):
        dest = link.split("#", 1)[0].strip()
        if not dest or re.match(r"^[a-z]+://", dest, re.I) or dest.startswith(("mailto:", "#")):
            continue
        target = path.parent / dest
        check(target.exists(), f"Broken local link: {path.relative_to(ROOT)} -> {dest}")


def verify_metadata() -> None:
    doc = SKILL_PATH.read_text(encoding="utf-8")
    parts = doc.split("---", 2)
    check(len(parts) == 3 and parts[0].strip() == "", "SKILL.md needs YAML frontmatter")
    if len(parts) < 3:
        return
    header = parts[1]
    name_match = re.search(r"^name:\s*(\S+)\s*$", header, re.M)
    name = name_match.group(1) if name_match else ""
    check(name == SKILL_FOLDER.name, "Skill name must match parent directory")
    check(name == "no-billshock", "Expected NoBillShock skill identity")
    check(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)) and len(name) <= 64,
          "Skill name has invalid characters or length")
    description_match = re.search(r"^description:\s*>-?\s*\n((?:^[ \t]+[^\n]*\n?)*)", header, re.M)
    description = " ".join(description_match.group(1).split()) if description_match else ""
    check(1 <= len(description) <= 1024, f"Description must be 1-1024 chars (got {len(description)})")
    for term in ("Do not", "Durable Object", "AWS Lambda", "public", "retry"):
        check(term.lower() in description.lower(), f"Description missing trigger/exclusion term: {term}")
    check("license: MIT" in header, "Expected MIT metadata")
    for guard in ("NOT CONFIGURED", "AUTO-IMPLEMENTED", "APPLIED AND VERIFIED IN CLOUD",
                  "BLOCKED", "NEEDS VERIFICATION", "READY FOR REVIEW",
                  "approval", "fake clocks", "Do not activate"):
        check(guard.lower() in doc.lower(), f"Skill missing guardrail: {guard}")
    check(len(doc.splitlines()) < 185, "Keep SKILL.md concise and delegate details to references")


def main() -> int:
    for readme in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
        check(readme.read_text(encoding="utf-8").startswith("# NoBillShock\n"),
              f"Incorrect project title in {readme.name}")
    for path in EXPECTED:
        check(path.is_file(), f"Missing required file: {path.relative_to(ROOT)}")
    if SKILL_PATH.exists():
        verify_metadata()
    for path in ROOT.rglob("*.md"):
        verify_markdown_links(path)
        text = path.read_text(encoding="utf-8")
        check(text.count("```") % 2 == 0, f"Uneven code fences in {path.relative_to(ROOT)}")
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s)")
        for item in ERRORS:
            print(f" - {item}")
        return 1
    print("PASS: Skill metadata, required files, reference links, local Markdown links, guardrails and fences")
    print("Checked:", len(EXPECTED), "required files and", len(list(ROOT.rglob('*.md'))), "Markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
