from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SkillInfo:
    name: str
    path: str
    has_skill_md: bool = False
    has_examples: bool = False
    has_scripts: bool = False
    has_templates: bool = False
    has_resources: bool = False
    has_references: bool = False
    has_assets: bool = False
    title: str | None = None
    summary: str | None = None
    phases: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    explicit_tags: list[str] = field(default_factory=list)
    inferred_tags: list[str] = field(default_factory=list)
    maturity: str = "unknown"
    quality_score: int = 0
    issues: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class SkillCoverage:
    phase: str
    domain: str
    count: int
    strength: str


@dataclass
class SkillRecommendation:
    name: str
    reason: str
    priority: str
    suggested_files: list[str] = field(default_factory=list)
    phases: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)


def to_dict(data: Any) -> Any:
    if hasattr(data, "__dataclass_fields__"):
        return asdict(data)
    if isinstance(data, list):
        return [to_dict(item) for item in data]
    return data
