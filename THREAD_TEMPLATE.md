# Thread State Template

> Copy this file and rename it for your project (e.g., `my-project.md`)

---

## Session Injection Block

Copy everything below this line when starting a session:

```
<thread>[PROJECT-NAME]</thread>
<scope>LOCKED</scope>

<status>
Stage: [Planning | Design | Implementation | Review]
Focus: [What you're working on now]
Last Updated: [YYYY-MM-DD]
</status>

<locked_decisions>
1. [Decision you've made and won't revisit]
2. [Another final decision]
</locked_decisions>

<rejected_ideas>
1. [Idea you considered but rejected] :: reason
2. [Another rejected approach] :: reason
</rejected_ideas>

<constraints>
• [Hard constraint 1]
• [Hard constraint 2]
• [Budget, timeline, technical limits, etc.]
</constraints>

<today_focus>[Your specific goal for this session]</today_focus>

[Your first question or task]
```

---

## Full State File Structure

Use this structure to maintain your thread state between sessions:

```markdown
# [Project Name] :: Thread State
## Last Updated: YYYY-MM-DD

---

## Current Status

**Stage:** [Planning | Design | Implementation | Review]
**Focus:** [Current area of work]
**Blockers:** [What's blocking progress, if anything]

---

## Decisions Made

1. [Decision] :: [Brief rationale]
2. [Decision] :: [Brief rationale]
3. [Decision] :: [Brief rationale]

---

## Rejected Ideas

1. ~~[Rejected idea]~~ :: [Why rejected]
2. ~~[Rejected idea]~~ :: [Why rejected]

---

## Open Questions

- [ ] [Question still to be resolved]
- [ ] [Another open question]
- [x] [Resolved question] :: [Answer]

---

## Constraints

• [Constraint 1]
• [Constraint 2]
• [Constraint 3]

---

## Context / Background

[Any important background the AI needs to know]

---

## Last Session

**Date:** YYYY-MM-DD
**Summary:** [What was accomplished]
**Next Actions:**
1. [Action item]
2. [Action item]

---

## Archive

[Move old decisions, resolved questions, and historical context here]
```

---

## Tips

1. **Keep the injection block lean** :: Only include what the AI needs for *this* session
2. **Update after every session** :: Apply CHECKPOINT output immediately
3. **Commit frequently** :: `git commit -am "checkpoint: [summary]"` 
4. **Archive aggressively** :: Move old context to Archive section to keep injection small
5. **One thread per project** :: Don't mix unrelated work in the same file
