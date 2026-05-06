from skill_manager.analyzer import analyze_skill
from skill_manager.models import SkillInfo


def test_analyzer_score_never_over_100():
    s = SkillInfo(name="x", path=".", title="t", summary="s", inferred_tags=["when_to_use", "inputs", "outputs", "steps", "examples", "cautions", "troubleshooting"])
    s = analyze_skill(s)
    assert s.quality_score <= 100
    assert s.quality_score == 100
