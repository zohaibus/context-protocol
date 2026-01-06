# [PROJECT-NAME] Thread State
## Last Updated: YYYY-MM-DD

<!--
=== NEW SESSION CHECKLIST ===
1. Run: python tools/patch_state.py load [this-file].md
2. Paste into Claude/GPT/Gemini
3. Work
4. Say CHECKPOINT before ending
5. Run: python tools/patch_state.py patch [this-file].md
6. git push
-->

---

## Session Injection Block

Copy everything inside the code block below when starting a session.
Or use: `python tools/patch_state.py load [this-file].md`

```
<thread>[PROJECT-NAME]</thread>
<scope>LOCKED</scope>

<status>
Stage: [Planning | Design | Implementation | Review]
Focus: [What you are working on now]
</status>

<locked_decisions>
1. [Decision you have made and will not revisit]
2. [Another final decision]
</locked_decisions>

<rejected_ideas>
1. [Idea you rejected] - [reason]
2. [Another rejected idea] - [reason]
</rejected_ideas>

<constraints>
- [Hard constraint 1]
- [Hard constraint 2]
- [Budget, timeline, technical limits, etc.]
</constraints>

<today_focus>[Your specific goal for this session]</today_focus>
```

---

## Current Status

| Field | Value |
|-------|-------|
| Stage | [Planning / Design / Implementation / Review] |
| Focus | [Current area of work] |
| Blockers | [What is blocking progress, if anything] |

---

## Decisions Made

1. [Decision] - [Brief rationale]
2. [Decision] - [Brief rationale]

---

## Rejected Ideas

1. ~~[Rejected idea]~~ - [Why rejected]
2. ~~[Rejected idea]~~ - [Why rejected]

---

## Open Questions

- [ ] [Question still to be resolved]
- [ ] [Another open question]

---

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

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
