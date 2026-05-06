from __future__ import annotations

from collections import Counter
from html import escape
from pathlib import Path

from .models import SkillInfo, SkillRecommendation

DOMAINS_FOR_MAP = ["python", "swift_ios", "web_frontend", "git_github", "codex", "nastran_cae"]


def write_markdown_report(skills: list[SkillInfo], recs: list[SkillRecommendation], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    avg = round(sum(s.quality_score for s in skills) / len(skills), 1) if skills else 0
    maturity = Counter(s.maturity for s in skills)
    lines = ["# Codex Skill Manager Report", "", "## Summary", "", f"- Total skills: {len(skills)}", f"- Average quality score: {avg}", f"- Stable: {maturity.get('stable', 0)}", f"- Usable: {maturity.get('usable', 0)}", f"- Draft: {maturity.get('draft', 0)}", f"- Needs fix: {maturity.get('needs_fix', 0)}", "", "## Skill List", "", "| Skill | Domains | Phases | Score | Issues |", "|---|---|---|---:|---|"]
    for s in skills:
        lines.append(f"| {s.name} | {', '.join(s.domains)} | {', '.join(s.phases)} | {s.quality_score} | {'; '.join(s.issues)} |")
    lines += ["", "## Coverage Map", ""]
    lines.append("| Phase / Domain | " + " | ".join(DOMAINS_FOR_MAP) + " |")
    lines.append("|---|" + "---:|" * len(DOMAINS_FOR_MAP))
    for phase in ["requirements", "design", "implementation", "testing", "review", "documentation", "release", "troubleshooting", "domain_support"]:
        row = []
        for domain in DOMAINS_FOR_MAP:
            cnt = sum(1 for s in skills if phase in s.phases and domain in s.domains)
            row.append(str(cnt))
        lines.append(f"| {phase} | " + " | ".join(row) + " |")

    lines += ["", "## Weak Areas", ""]
    weak = [p for p in ["requirements", "design", "testing", "release", "domain_support"] if sum(1 for s in skills if p in s.phases) < 1]
    for w in weak or ["- None"]:
        lines.append(f"- {w}")

    lines += ["", "## Recommended Skills", "", "| Priority | Skill | Reason |", "|---|---|---|"]
    for r in recs:
        lines.append(f"| {r.priority} | {r.name} | {r.reason} |")
    lines += ["", "## Improvement Suggestions", ""]
    for s in skills:
        for rec in s.recommendations:
            lines.append(f"- {s.name}: {rec}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html_report(skills: list[SkillInfo], recs: list[SkillRecommendation], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    avg = round(sum(s.quality_score for s in skills) / len(skills), 1) if skills else 0
    body = ["<h1>Codex Skill Manager Report</h1>", "<h2>Summary</h2>", f"<p>Total skills: {len(skills)} / Average quality score: {avg}</p>", "<h2>Skill List</h2>", "<table border='1'><tr><th>Skill</th><th>Domains</th><th>Phases</th><th>Score</th><th>Issues</th></tr>"]
    for s in skills:
        body.append(f"<tr><td>{escape(s.name)}</td><td>{escape(', '.join(s.domains))}</td><td>{escape(', '.join(s.phases))}</td><td>{s.quality_score}</td><td>{escape('; '.join(s.issues))}</td></tr>")
    body.append("</table><h2>Coverage Map</h2><p>See markdown report for detailed matrix.</p>")
    body.append("<h2>Weak Areas</h2><ul>")
    weak = [p for p in ["requirements", "design", "testing", "release", "domain_support"] if sum(1 for s in skills if p in s.phases) < 1]
    for w in weak:
        body.append(f"<li>{escape(w)}</li>")
    body.append("</ul><h2>Recommended Skills</h2><ul>")
    for r in recs:
        body.append(f"<li><strong>{escape(r.priority)}</strong> {escape(r.name)}: {escape(r.reason)}</li>")
    body.append("</ul><h2>Improvement Suggestions</h2><ul>")
    for s in skills:
        for rec in s.recommendations:
            body.append(f"<li>{escape(s.name)}: {escape(rec)}</li>")
    body.append("</ul>")
    html = "<!doctype html><html lang='ja'><head><meta charset='UTF-8'><title>Codex Skill Manager Report</title></head><body>" + "".join(body) + "</body></html>"
    out_path.write_text(html, encoding="utf-8")
