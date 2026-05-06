---
name: swiftui-coredata-review
description: Review and test viewpoints for SwiftUI + CoreData app modifications.
---

# swiftui-coredata-review

## Purpose

Help review SwiftUI and CoreData changes with consistency, testability, and data safety checks.

## When to use

Use this skill when a PR touches SwiftUI views, CoreData models, or persistence logic.

## Inputs

- SwiftUI/CoreData diff
- Test scope and risk notes

## Outputs

- Review comments
- Test focus list

## Steps

1. Check data model migration safety.
2. Confirm SwiftUI state flow and binding correctness.
3. Verify fetch/request performance risks.
4. Validate unit/UI test coverage expectations.
5. Provide prioritized review feedback.

## Examples

### Example input

```text
Review this CoreData schema and SwiftUI list rendering update.
```

### Example output

```text
Migration risk: low, add one test for empty-state fetch and one for delete rollback.
```

## Cautions

- Never assume migration compatibility without schema diff.
- Watch for main-thread blocking fetch operations.

## Troubleshooting

If data disappears after update, inspect migration policy and persistent store compatibility first.
