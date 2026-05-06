# Codex Skill Manager

## Overview

Codex Skill Manager scans local Codex skills, analyzes SKILL.md files, classifies skills, checks quality, recommends missing skills, and generates new skill templates.

## Installation

```bash
pip install -e .
```

## Usage

```bash
skill-manager scan --path ./sample_skills
skill-manager analyze --path ./sample_skills
skill-manager report --path ./sample_skills --format html
skill-manager recommend --path ./sample_skills
skill-manager generate codex-task-planner --output ./sample_skills
```

## Commands

- `scan`: スキル候補を走査しJSON在庫を出力
- `analyze`: 解析・分類・品質診断を実施
- `report`: Markdown/HTMLレポートを生成
- `recommend`: 不足スキル候補を提案
- `generate`: 新規スキル雛形を安全生成

## Output Files

- output/skills_inventory.json
- output/skills_analysis.json
- output/skills_report.md
- output/skills_report.html

## Limitations

- This MVP does not install external skills automatically.
- This MVP does not execute scripts inside skills.
- This MVP does not modify Codex settings.

## Future Work

- Mermaid skill map output
- Duplicate skill detection
- Skill improvement patch generation
- GitHub skill candidate search
- Safety-checked skill acquisition
- GUI
- VS Code extension
