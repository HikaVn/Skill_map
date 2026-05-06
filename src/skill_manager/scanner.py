from __future__ import annotations

from pathlib import Path

from .models import SkillInfo


def scan_skills(root_path: str) -> list[SkillInfo]:
    root = Path(root_path)
    if not root.exists():
        raise FileNotFoundError(f"Skill root path does not exist: {root_path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Skill root path is not a directory: {root_path}")

    skills: list[SkillInfo] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        skills.append(
            SkillInfo(
                name=child.name,
                path=str(child),
                has_skill_md=(child / "SKILL.md").is_file(),
                has_examples=(child / "examples").is_dir(),
                has_scripts=(child / "scripts").is_dir(),
                has_templates=(child / "templates").is_dir(),
                has_resources=(child / "resources").is_dir(),
                has_references=(child / "references").is_dir(),
                has_assets=(child / "assets").is_dir(),
            )
        )
    return skills
