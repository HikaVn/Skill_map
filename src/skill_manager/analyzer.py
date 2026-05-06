from __future__ import annotations

from .models import SkillInfo


def analyze_skill(skill: SkillInfo) -> SkillInfo:
    score = 0
    issues: list[str] = []
    recommendations: list[str] = []

    def check(ok: bool, points: int, issue: str, rec: str) -> None:
        nonlocal score
        if ok:
            score += points
        else:
            issues.append(issue)
            recommendations.append(rec)

    inferred = set(skill.inferred_tags)
    check(bool(skill.title), 10, "titleが不足しています。", "タイトルを追加してください。")
    check(bool(skill.summary), 10, "summaryが不足しています。", "Purpose/Summary/Descriptionを追記してください。")
    check("when_to_use" in inferred, 10, "When to useが不足しています。", "When to useが不足しています。どの場面でこのスキルを使うべきかを追記してください。")
    check("inputs" in inferred, 10, "Inputsが不足しています。", "Inputsを追加してください。")
    check("outputs" in inferred, 10, "Outputsが不足しています。", "Outputsを追加してください。")
    check("steps" in inferred, 20, "Stepsが不足しています。", "Stepsが不足しています。Codexが再現できる具体的な手順を追加してください。")
    check("examples" in inferred, 10, "Examplesが不足しています。", "Examplesが不足しています。入力例と出力例を追加してください。")
    check("cautions" in inferred, 10, "Cautionsが不足しています。", "Cautionsを追加してください。")
    check("troubleshooting" in inferred, 10, "Troubleshootingが不足しています。", "Troubleshootingまたは失敗時対応を追加してください。")

    skill.quality_score = min(100, score)
    skill.issues = issues
    skill.recommendations = recommendations
    if score >= 85:
        skill.maturity = "stable"
    elif score >= 70:
        skill.maturity = "usable"
    elif score >= 50:
        skill.maturity = "draft"
    else:
        skill.maturity = "needs_fix"
    return skill
