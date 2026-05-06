from __future__ import annotations

import re
from pathlib import Path

from .models import SkillInfo

PHASE_KEYWORDS = {
    "requirements": ["requirement", "spec", "仕様", "要件"],
    "design": ["design", "architecture", "設計"],
    "implementation": ["implement", "code", "実装"],
    "testing": ["test", "pytest", "unittest", "テスト"],
    "review": ["review", "pull request", "レビュー", "pr"],
    "documentation": ["document", "markdown", "readme", "ドキュメント"],
    "release": ["release", "deploy", "github pages", "リリース", "公開"],
    "troubleshooting": ["troubleshoot", "error", "fix", "debug", "エラー", "修正"],
    "domain_support": ["support", "answer", "nastran", "cae", "サポート"],
}

DOMAIN_KEYWORDS = {
    "python": ["python", "pytest", "pip", "pyproject"],
    "swift_ios": ["swift", "swiftui", "xcode", "coredata", "ios"],
    "web_frontend": ["html", "css", "javascript", "react", " lp "],
    "git_github": ["git", "github", "pull request", "actions", "pages", " pr "],
    "codex": ["codex", "skill", "skill.md"],
    "claude_code": ["claude code"],
    "nastran_cae": ["nastran", "msc nastran", "cae", "bdf", "f06", "op2"],
    "esp32_iot": ["esp32", "arduino", "gpio", "sensor"],
    "music_audio": ["audio", "midi", "logic pro", "fft", "音声", "音楽"],
    "image_asset": ["image", "png", "jpg", "asset", "画像", "透過"],
    "business_planning": ["business", "monetization", " lp ", "マネタイズ", "事業"],
}


def classify_skill(skill: SkillInfo) -> SkillInfo:
    md_path = Path(skill.path) / "SKILL.md"
    text = f"{skill.name}\n{skill.title or ''}\n{skill.summary or ''}"
    if md_path.is_file():
        text += "\n" + md_path.read_text(encoding="utf-8", errors="ignore")
    normalized = f" {text.lower()} "

    skill.phases = sorted(_match_categories(normalized, PHASE_KEYWORDS))
    skill.domains = sorted(_match_categories(normalized, DOMAIN_KEYWORDS))
    skill.explicit_tags = sorted(set(skill.phases + skill.domains))
    return skill


def _match_categories(text: str, mapping: dict[str, list[str]]) -> list[str]:
    results = []
    for category, keywords in mapping.items():
        for keyword in keywords:
            if len(keyword.strip()) <= 2:
                continue
            if _contains_keyword(text, keyword.lower()):
                results.append(category)
                break
    return results


def _contains_keyword(text: str, keyword: str) -> bool:
    if " " in keyword or any(ord(c) > 127 for c in keyword):
        return keyword in text
    pattern = rf"\b{re.escape(keyword)}\b"
    return re.search(pattern, text) is not None
