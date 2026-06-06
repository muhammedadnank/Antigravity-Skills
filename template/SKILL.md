---
name: replace-with-skill-name-using-hyphens
# CRITICAL: Description MUST describe "When to use" (triggers, symptoms, errors).
# NEVER summarize the skill's workflow here. Keep under 500 chars if possible.
description: Use when [describe triggering conditions, symptoms, or specific errors]. 
---

# Skill Name

## Overview
[1-2 sentences explaining the core principle. What is the fundamental insight of this skill?]

## When to Use (Triggers)
- **Symptoms**: [Errors, behaviors, or patterns that indicate this skill is needed]
- **Contexts**: [Specific scenarios where this pattern applies]

### When NOT to Use
- [Scenario A] -> Use `[other-skill-name]` instead.
- [Scenario B] -> Does not apply because...

## Core Pattern
[Explain the mental model. Use a before/after code block or a small `dot` flowchart if the decision process is non-obvious.]

```language
// ❌ Anti-pattern / Baseline failure
[Show the common mistake or naive approach]
```

```language
// ✅ Best practice / Correct implementation
[Show the correct pattern]
```

## Step-by-Step Workflow
[Clear, numbered steps for the agent to follow. Use imperative verbs.]

1. **[Phase 1]**: [Action to take]
2. **[Phase 2]**: [Action to take]
   - *Requirement*: [Specific constraint]
3. **[Phase 3]**: [Action to take]

## Quick Reference
[A table for fast lookup of commands, syntax, or common operations.]

| Operation / Scenario | Syntax / Command | Notes |
|----------------------|------------------|-------|
| [Operation]          | `[Command]`      | [Note] |

## Verification (Success Criteria)
[How to prove the implementation is correct (The GREEN phase). Agent must run these checks.]
- [ ] [Verification check 1, e.g., run test suite]
- [ ] [Verification check 2, e.g., verify no lint errors]

## Common Mistakes & Red Flags
[List specific rationalizations, shortcuts, or misunderstandings the agent might have. Address the "RED" phase baseline failures here.]

| Red Flag (Excuse / Mistake) | Reality / Fix (What to do instead) |
|-----------------------------|------------------------------------|
| "I'll just skip testing this time." | **STOP.** You must verify the behavior first. |
| [Mistake or excuse]         | **STOP.** [Correct action]         |