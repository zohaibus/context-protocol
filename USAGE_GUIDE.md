# Usage Guide

A deep dive into the Context Protocol workflow, philosophy, and best practices.

---

## The Mental Model

### Why LLMs Feel Inconsistent

LLMs are **stateless text processors**. They don't "remember" anything - they process your input and generate output, then reset completely.

What feels like "memory" is actually:
- Chat history being re-fed into the context window
- That context window has limits (overflows)
- Attention degrades in the middle of long contexts
- "Memory" features are shallow retrieval, not true understanding

### The Reframe

Instead of fighting statelessness, embrace it:

| Traditional Thinking | Context Protocol Thinking |
|---------------------|---------------------------|
| "AI should remember" | "I maintain the memory" |
| "Memory features will improve" | "External state is more reliable" |
| "The AI is my partner" | "The AI is a CPU I operate" |
| "Trust chat history" | "Trust my files" |

### The Architecture

```
YOU (The Operating System)
├── Decide what context to inject
├── Make final decisions
├── Ratify AI outputs
└── Commit changes to files

YOUR FILES (The RAM)
├── Thread state (current context)
├── Locked decisions (immutable)
├── Rejected ideas (never resurrect)
└── Git history (full audit trail)

ANY LLM (The CPU)
├── Processes your input
├── Generates output
├── Follows your constraints
└── Then forgets completely
```

---

## The Workflow

### Quick Reference

```
START:   load -> paste -> work
END:     CHECKPOINT -> copy -> patch -> push
```

### Session Start

1. **Load context to clipboard:**
   ```bash
   python tools/patch_state.py load my-project.md
   ```
   This copies CORE_PROMPT + your thread state together.

2. **Open Claude/GPT/Gemini**

3. **Paste** (Ctrl+V / Cmd+V) - both files are combined

4. **Start working**

**Important:** Always use the `load` command. It ensures CORE_PROMPT is included, which defines the CHECKPOINT format.

### During Session

- Work normally - ask questions, brainstorm, code
- AI will respect your `<locked_decisions>` and `<constraints>`
- If AI tries to resurrect a `<rejected_ideas>`, it should warn you
- If you drift off topic, `SCOPE LOCK` will redirect you

### Mid-Session Checkpoint (Optional)

Every ~15 exchanges, or after making a decision:

1. Say: `CHECKPOINT`
2. AI outputs a structured STATE PATCH
3. Copy it somewhere (or apply immediately)

This prevents losing work if the session crashes or context degrades.

### Session End

1. Say: `CHECKPOINT`
2. AI outputs the STATE PATCH in strict format
3. Copy the output to clipboard
4. Apply to your file:
   ```bash
   python tools/patch_state.py patch my-project.md
   ```
5. Review changes, confirm
6. Git commit happens automatically
7. Push to remote:
   ```bash
   git push
   ```

---

## The Commands

### CHECKPOINT

**Purpose:** Export current state as a structured diff

**When to use:**
- Before closing a session
- After making an important decision
- Every ~15 exchanges in long sessions
- When you want to "save your game"

**Output format (STRICT):**
```
=== STATE PATCH ===
Thread: PROJECT-NAME | Date: 2025-01-01

[ADD] DECISIONS MADE
- Decision we made in this session
- Another decision

[ADD] REJECTED IDEAS
- Idea we explicitly ruled out

[REMOVE] OPEN QUESTIONS
- Question we answered

[UPDATE] STATUS
- Stage: New stage
- Focus: New focus

[NEXT]
- Action item 1
- Action item 2
```

**Strict Rules:**
- ONLY these 5 tags are allowed: `[ADD] DECISIONS MADE`, `[ADD] REJECTED IDEAS`, `[REMOVE] OPEN QUESTIONS`, `[UPDATE] STATUS`, `[NEXT]`
- NO custom tags (like `[ADD] DOCUMENTS CREATED`)
- NO tables, NO prose, NO explanations
- Bullet points only (`- item`)
- If a section has no items, omit it entirely

### SCOPE LOCK

**Purpose:** Refuse to discuss topics outside current thread

**When to use:**
- When you want focused work on one project
- When context bleed between projects is a risk
- When you catch yourself going off-topic

**How it works:**
1. Set `<scope>LOCKED</scope>` in your thread state
2. If you ask about another topic, AI responds:
   ```
   [!] SCOPE VIOLATION: [topic] is outside [THREAD].
   Unlock scope or switch thread?
   ```
3. AI stops and waits for your decision

### HARD STOP

**Purpose:** Emergency brake - stop all output immediately

**When to use:**
- AI is going in a wrong direction
- You need to re-inject context
- Something feels off

**How it works:**
- Say: `HARD STOP`
- AI outputs: "Stopped. Paste thread state or unlock."
- AI stops completely

### MODE: STRATEGY

**Purpose:** Deterministic, analytical responses

**When to use:**
- Making decisions
- Analyzing tradeoffs
- When you need consistent answers

**Behavior:**
- No speculation
- Flags contradictions
- Sticks to facts and constraints

### MODE: EXPLORATION

**Purpose:** Creative, challenging responses

**When to use:**
- Brainstorming
- Challenging assumptions
- Early ideation

**Behavior:**
- More speculative (flagged)
- Will challenge your constraints
- Suggests unconventional approaches

---

## The Constraint Tags

### `<locked_decisions>`

**Purpose:** Decisions you've made and won't revisit

**Behavior:** AI will not suggest alternatives or question these

**Example:**
```xml
<locked_decisions>
1. Using PostgreSQL for the database
2. API-first architecture
3. No mobile app for MVP
</locked_decisions>
```

### `<rejected_ideas>`

**Purpose:** Ideas you've explicitly ruled out

**Behavior:** If AI (or you) suggests these, it should warn immediately

**Example:**
```xml
<rejected_ideas>
1. GraphQL - too complex for MVP
2. Microservices - need monolith first
3. Blockchain - not relevant to our problem
</rejected_ideas>
```

### `<constraints>`

**Purpose:** Hard limits that cannot be violated

**Behavior:** AI checks all suggestions against these

**Example:**
```xml
<constraints>
- Budget: $0 (free tier only)
- Timeline: 4 weeks to MVP
- Team: Solo developer
- Must work offline
</constraints>
```

---

## Best Practices

### Always Use the Load Command

```bash
python tools/patch_state.py load my-project.md
```

This ensures CORE_PROMPT is always included. Without it, the AI won't know the CHECKPOINT format and will improvise.

### Keep Injection Blocks Small

The session injection should be **lean** - only what the AI needs for this specific session.

**Too big:**
- Full project history
- Every decision ever made
- Pages of background

**Just right:**
- Current status
- Relevant locked decisions
- Active constraints
- Today's focus

Move old context to the **Archive** section of your state file.

### Commit After Every Session

```bash
git commit -am "[PROJECT] checkpoint: summary of what happened"
git push
```

Your Git history becomes:
- An audit trail of all decisions
- A way to recover from mistakes
- A record of your thinking over time

### One Thread Per Domain

Don't mix unrelated work:

**Bad:**
- One file for "all my AI chats"
- Mixing work project with personal project

**Good:**
- `work-api-redesign.md`
- `personal-blog-migration.md`
- `q1-strategy.md`

### Update Immediately

After every session:
1. Apply the CHECKPOINT
2. Commit to Git
3. Push to remote
4. Don't "do it later"

State files that aren't updated become stale and useless.

### Review Before You Ratify

The CHECKPOINT is a proposal. Before applying:
- Does this accurately capture what we decided?
- Are the "rejected ideas" things we actually rejected?
- Are the "next actions" what I actually want to do?

You are the operating system. You ratify.

---

## Troubleshooting

### AI Ignores Constraints

1. Re-paste the CORE_PROMPT
2. Re-paste your `<constraints>` explicitly
3. If still failing, start a new session

### AI Resurrects Rejected Ideas

1. Point it to `<rejected_ideas>`
2. Say: "This was rejected. See rejected ideas."
3. If persistent, add: "Do not suggest variations of rejected ideas"

### Context Seems Degraded

Signs:
- AI "forgets" things from earlier in session
- Responses become generic
- Constraints stop being respected

Fix:
1. Say `CHECKPOINT` to save current state
2. Start a new session
3. Use `load` command to paste fresh context

### CHECKPOINT Format Is Wrong

If AI outputs custom tags like `[ADD] DOCUMENTS CREATED` or uses tables/prose:

Say:
```
Redo CHECKPOINT using ONLY these 5 tags:
[ADD] DECISIONS MADE
[ADD] REJECTED IDEAS
[REMOVE] OPEN QUESTIONS
[UPDATE] STATUS
[NEXT]

No custom tags. No tables. Bullets only.
```

### Script Can't Parse CHECKPOINT

The `patch_state.py` script expects the strict 5-tag format. If parsing fails:
1. Ask AI to redo CHECKPOINT in strict format
2. Or manually update your state file (the protocol still works)

---

## Philosophy

### Why Manual Is a Feature

Every time you:
- Copy a CHECKPOINT
- Review the changes
- Apply to your file
- Commit to Git

You are:
- Verifying the AI's output
- Taking ownership of decisions
- Creating an audit trail
- Maintaining your own memory

**The friction is intentional.** It's your quality control.

### Why Not Agents?

Agents try to automate the human out of the loop:
- Agent decides next step
- Agent retrieves "memory"
- Agent chains actions together

Problems:
- Hallucinations compound
- Hard to debug
- You lose control
- You can't audit decisions

Context Protocol keeps humans in the loop:
- You decide next step
- You control what AI sees
- You ratify before committing
- Full audit trail in Git

**Agents are for automation. This is for cognition.**

### Why Files Over Cloud Memory?

Cloud memory services:
- Store your data on their servers
- Use opaque formats
- Charge for retrieval
- Lock you into their ecosystem

Local files:
- Your machine, your control
- Plain text (readable forever)
- Free
- Works with any LLM

**Sovereign-first: Own your thinking.**

---

## The Mantra

```
The LLM proposes.
You ratify.
The system records.
```

```
load -> work -> CHECKPOINT -> patch -> push
```

You are the operating system.
Build accordingly.
