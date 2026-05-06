from pathlib import Path

from skill_manager.scanner import scan_skills


def test_scan_skills_detects_directories(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "SKILL.md").write_text("# A", encoding="utf-8")
    (tmp_path / "b").mkdir()
    skills = scan_skills(str(tmp_path))
    assert [s.name for s in skills] == ["a", "b"]
    assert skills[0].has_skill_md is True
    assert skills[1].has_skill_md is False
