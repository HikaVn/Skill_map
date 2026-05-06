from __future__ import annotations

from .models import SkillInfo, SkillRecommendation


def recommend_skills(skills: list[SkillInfo]) -> list[SkillRecommendation]:
    names = {s.name for s in skills}
    domains = [d for s in skills for d in s.domains]
    phases = [p for s in skills for p in s.phases]

    def weak(phase: str) -> bool:
        return phases.count(phase) < 1

    recs: list[SkillRecommendation] = []

    def add(name: str, reason: str, priority: str, phases_l: list[str], domains_l: list[str]):
        if name in names or any(r.name == name for r in recs):
            return
        recs.append(SkillRecommendation(name=name, reason=reason, priority=priority, suggested_files=["SKILL.md", "examples/", "templates/"], phases=phases_l, domains=domains_l))

    if domains.count("codex") < 1 or weak("requirements") or weak("design"):
        add("codex-task-planner", "大きな開発依頼をCodexに渡しやすい単位へ分割するスキルが不足しています。", "high", ["requirements", "design"], ["codex"])
    if any(s.quality_score < 70 for s in skills):
        add("skill-auditor", "既存スキルの品質を継続的に点検するためのスキルが有用です。", "high", ["review"], ["codex"])
    if "codex" in domains and len(skills) >= 5:
        add("skill-generator", "新規SKILL.mdを一貫した形式で作成するスキルがあると、スキル追加が安定します。", "medium", ["implementation"], ["codex"])
    if any(d in domains for d in ["web_frontend", "git_github"]) and weak("release"):
        add("github-pages-troubleshooting", "GitHub Pages、Actions、PR反映確認の手順化が不足しています。", "medium", ["release", "troubleshooting"], ["git_github", "web_frontend"])
    if "swift_ios" in domains and (weak("testing") or weak("review")):
        add("swiftui-coredata-review", "SwiftUIとCoreDataを使うアプリ改修時のレビュー観点が不足しています。", "medium", ["testing", "review"], ["swift_ios"])
    if "nastran_cae" in domains or weak("domain_support"):
        add("nastran-support-answer", "MSC Nastran関連の問い合わせ回答を、仕様・制限・推論を分けて作成するスキルが有用です。", "low", ["domain_support"], ["nastran_cae"])

    return recs
