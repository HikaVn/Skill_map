from skill_manager.models import SkillInfo
from skill_manager.parser import parse_skill_md


def test_parser_gets_title_summary(tmp_path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "SKILL.md").write_text("""---\nname: my-skill\ndescription: my-desc\n---\n\n## Purpose\nHello\n""", encoding="utf-8")
    s = parse_skill_md(SkillInfo(name="s", path=str(d), has_skill_md=True))
    assert s.title == "my-skill"
    assert s.summary == "my-desc"


def test_parser_handles_empty(tmp_path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "SKILL.md").write_text("", encoding="utf-8")
    s = parse_skill_md(SkillInfo(name="s", path=str(d), has_skill_md=True))
    assert s.title is None
