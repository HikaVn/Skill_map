from __future__ import annotations

import re
import shutil
from pathlib import Path


def generate_skill(skill_name: str, output_root: str, force: bool = False) -> Path:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", skill_name):
        raise ValueError("Skill name contains unsafe characters.")
    if ".." in skill_name or "/" in skill_name or "\\" in skill_name:
        raise ValueError("Path traversal is not allowed.")

    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = (root / skill_name).resolve()
    if root not in target.parents:
        raise ValueError("Invalid output path.")

    if target.exists():
        if not force:
            raise FileExistsError(f"Skill directory already exists: {target}")
        shutil.rmtree(target)

    target.mkdir(parents=True)
    (target / "examples").mkdir()
    (target / "templates").mkdir()

    template_path = Path(__file__).resolve().parents[2] / "templates" / "skill_template.md"
    content = template_path.read_text(encoding="utf-8").replace("{{ skill_name }}", skill_name)
    (target / "SKILL.md").write_text(content, encoding="utf-8")
    return target
