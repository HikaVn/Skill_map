from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_skill
from .classifier import classify_skill
from .generator import generate_skill
from .models import to_dict
from .parser import parse_skill_md
from .recommender import recommend_skills
from .report import write_html_report, write_markdown_report
from .scanner import scan_skills


def _pipeline(path: str):
    skills = scan_skills(path)
    out = []
    for s in skills:
        s = parse_skill_md(s)
        s = classify_skill(s)
        s = analyze_skill(s)
        out.append(s)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(prog="skill-manager")
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ["scan", "analyze", "recommend"]:
        p = sub.add_parser(cmd)
        p.add_argument("--path", required=True)
    rp = sub.add_parser("report")
    rp.add_argument("--path", required=True)
    rp.add_argument("--format", choices=["md", "html"], required=True)
    gp = sub.add_parser("generate")
    gp.add_argument("name")
    gp.add_argument("--output", required=True)
    gp.add_argument("--force", action="store_true")

    args = parser.parse_args()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    try:
        if args.command == "scan":
            skills = scan_skills(args.path)
            out = output_dir / "skills_inventory.json"
            out.write_text(json.dumps(to_dict(skills), ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Wrote {out}")
        elif args.command == "analyze":
            skills = _pipeline(args.path)
            out = output_dir / "skills_analysis.json"
            out.write_text(json.dumps(to_dict(skills), ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Wrote {out}")
        elif args.command == "report":
            skills = _pipeline(args.path)
            recs = recommend_skills(skills)
            if args.format == "md":
                out = output_dir / "skills_report.md"
                write_markdown_report(skills, recs, out)
            else:
                out = output_dir / "skills_report.html"
                write_html_report(skills, recs, out)
            print(f"Wrote {out}")
        elif args.command == "recommend":
            skills = _pipeline(args.path)
            recs = recommend_skills(skills)
            print(json.dumps(to_dict(recs), ensure_ascii=False, indent=2))
        elif args.command == "generate":
            created = generate_skill(args.name, args.output, force=args.force)
            print(f"Generated {created}")
    except Exception as e:
        raise SystemExit(f"Error: {e}")


if __name__ == "__main__":
    main()
