from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

from .models import SkillInfo


SECTION_ALIASES = {
    "summary": {"purpose", "summary", "overview", "description"},
    "when_to_use": {"when to use"},
    "inputs": {"inputs"},
    "outputs": {"outputs"},
    "steps": {"steps"},
    "examples": {"examples"},
    "cautions": {"cautions", "warnings"},
    "troubleshooting": {"troubleshooting", "failure handling", "error handling"},
}


def parse_skill_md(skill: SkillInfo) -> SkillInfo:
    skill_path = Path(skill.path) / "SKILL.md"
    if not skill_path.is_file():
        return skill

    text = skill_path.read_text(encoding="utf-8")
    if not text.strip():
        return skill

    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            meta = {}
            if yaml is not None:
                try:
                    meta = yaml.safe_load(parts[1]) or {}
                except Exception:
                    meta = {}
            else:
                for line in parts[1].splitlines():
                    if ":" in line:
                        k,v = line.split(":",1)
                        meta[k.strip()] = v.strip()
            if isinstance(meta, dict):
                skill.title = skill.title or meta.get("name")
                skill.summary = skill.summary or meta.get("description")
            body = parts[2]

    clean = _remove_code_blocks(body)
    sections = _extract_sections(clean)

    if not skill.title:
        m = re.search(r"^#\s+(.+)$", clean, flags=re.MULTILINE)
        if m:
            skill.title = m.group(1).strip()

    if not skill.summary:
        for key in SECTION_ALIASES["summary"]:
            content = sections.get(key)
            if content:
                skill.summary = _first_nonempty_line(content)
                break

    skill.inferred_tags = sorted(
        {
            key
            for key, aliases in SECTION_ALIASES.items()
            if key != "summary" and any(alias in sections for alias in aliases)
        }
    )
    return skill


def _remove_code_blocks(text: str) -> str:
    return re.sub(r"```[\s\S]*?```", "", text)


def _extract_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        head = re.match(r"^#{2,6}\s+(.+)$", line)
        if head:
            current = head.group(1).strip().lower()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _first_nonempty_line(text: str) -> str | None:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return None
