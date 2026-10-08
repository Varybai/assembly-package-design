"""Validate this repository's knowledge-only Skill and all installed local references."""

from pathlib import Path
import re
import sys


EXPECTED = {
    "SKILL.md",
    "references/charter.md",
    "references/object-contract.md",
    "references/execution-evidence.md",
    "references/domain-adapters.md",
    "references/pi-package.md",
    "references/conformance.md",
    "references/implementation-map.md",
    "assets/PACKAGE-DESIGN.template.md",
    "assets/DECISION.template.md",
    "assets/DOMAIN-EXAMPLES.md",
}


def validate(root):
    root = root.resolve()
    files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if files != EXPECTED:
        raise ValueError(f"Unexpected Skill payload: missing={EXPECTED - files}, extra={files - EXPECTED}")
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    # This Skill deliberately uses only two single-line scalar fields.
    fields = {}
    for line in match[1].splitlines():
        key, value = line.split(":", 1)
        if key in fields:
            raise ValueError(f"Duplicate frontmatter field: {key}")
        fields[key] = value.strip()
    if set(fields) != {"name", "description"}:
        raise ValueError("Unexpected frontmatter fields")
    if fields["name"] != "assembly-package-design" or root.name != fields["name"]:
        raise ValueError("Skill name and directory must agree")
    if not 1 <= len(fields["description"]) <= 1024:
        raise ValueError("Invalid description length")
    links = 0
    for relative in sorted(files):
        file = root / relative
        if file.is_symlink():
            raise ValueError(f"Skill payload must contain actual files: {file}")
        body = file.read_text(encoding="utf-8")
        if re.search(r"/Users/[^/\s]+/|[A-Z]:\\Users\\", body):
            raise ValueError(f"Personal machine path in {relative}")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (file.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise ValueError(f"Broken or escaping reference: {relative} -> {target}")
            links += 1
    print(f"PASS: one standard Skill, {len(files)} Markdown files, {links} local links, no executable payload")


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "skills/assembly-package-design"
    validate(root)
