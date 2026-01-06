# Context Protocol

> **The LLM is the CPU. Your files are the memory. You are the operating system.**

⚠️ Not affiliated with Anthropic's Model Context Protocol (MCP). This is a human workflow protocol for manual context injection using markdown + Git :: not an MCP server implementation.

- ❌ Not an MCP server (different from Anthropic's Model Context Protocol)
- ❌ Not a RAG pipeline or vector database
- ❌ Not an agent framework
- ✅ A protocol for human-in-the-loop cognition

---

A sovereign-first workflow for thinking with LLMs. No agents, no vector databases, no vendor lock-in. Just text files and a protocol for human-in-the-loop cognition.

---

![Context Protocol Comparison](docs/comparison-table.png)

---

## The Problem

LLMs feel inconsistent because they are stateless.
Chat history overflows. Attention decays. "Memory" features are shallow.
The result: ideas resurface, decisions vanish, and trust erodes.

## The Insight

Stop expecting AI to remember. Start acting like an Operating System.

```
┌─────────────────────────────────────────────────────────────┐
│                         YOU                                 │
│                  (The Operating System)                     │
│                                                             │
│    Inject context │ Make decisions │ Ratify outputs         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     YOUR FILES                              │
│                      (The RAM)                              │
│                                                             │
│    Thread states │ Locked decisions │ Constraints           │
│    Plain markdown │ Git version control                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       ANY LLM                               │
│                      (The CPU)                              │
│                                                             │
│    Claude │ GPT │ Gemini  |  Interchangeable                │
│    Processes input → Generates output → Forgets             │
└─────────────────────────────────────────────────────────────┘
```

## Who This Is For

People who think across days or weeks:
- **Engineers** managing complex projects
- **PMs** tracking product decisions  
- **Founders** holding strategic context
- **Consultants** juggling client work
- **Executives** maintaining decision history

If your work requires consistent AI behavior over time, this is for you.

---

## The System

### 5 Commands

| Command | What It Does |
|---------|--------------|
| `CHECKPOINT` | Export state as structured diff |
| `SCOPE LOCK` | Refuse to discuss other topics |
| `HARD STOP` | Emergency brake, stop completely |
| `MODE: STRATEGY` | Deterministic, flag contradictions |
| `MODE: EXPLORATION` | Creative, challenge assumptions |

### 3 Constraint Tags

```xml
<locked_decisions>
Decisions we've made. Don't revisit.
</locked_decisions>

<rejected_ideas>
Ideas we've discarded. Don't resurrect.
</rejected_ideas>

<constraints>
Rules to always obey. No exceptions.
</constraints>
```

### The Workflow

```
load → work → CHECKPOINT → patch → push
```

**START SESSION:**
```bash
python tools/patch_state.py load my-project.md
# Copies CORE_PROMPT + thread state to clipboard
# Paste into Claude/GPT/Gemini
```

**WORK:** Ask questions, brainstorm, make decisions

**END SESSION:**
```bash
# 1. Say "CHECKPOINT" in the chat
# 2. Copy AI output to clipboard
python tools/patch_state.py patch my-project.md
git push
```

---

## Quick Start

### Prerequisites
- A text editor (VS Code, Obsidian, or any markdown editor)
- Git
- An LLM (Claude, GPT, or Gemini)
- Python 3.7+ (for automation script)

### Setup

```bash
git clone https://github.com/zohaibus/context-protocol.git
cd context-protocol
pip install -r requirements.txt
```

### First Session (New Project)

1. Copy `THREAD_TEMPLATE.md` to `my-project.md`
2. Edit the template with your project context
3. Load and start:
   ```bash
   python tools/patch_state.py load my-project.md
   ```
4. Paste into Claude/GPT/Gemini
5. Start working

### Resuming a Session (Existing Project)

```bash
python tools/patch_state.py load my-project.md
# Paste into Claude/GPT/Gemini
# Continue working
```

### End Session

1. Type: `CHECKPOINT`
2. Copy the AI's output to clipboard
3. Apply the patch:
   ```bash
   python tools/patch_state.py patch my-project.md
   ```
4. Push to remote:
   ```bash
   git push
   ```

---

## CHECKPOINT Format

When you say `CHECKPOINT`, the AI outputs a strict format:

```
=== STATE PATCH ===
Thread: PROJECT-NAME | Date: YYYY-MM-DD

[ADD] DECISIONS MADE
- Decision 1
- Decision 2

[ADD] REJECTED IDEAS
- Rejected item

[REMOVE] OPEN QUESTIONS
- Resolved question

[UPDATE] STATUS
- Stage: Current stage
- Focus: Current focus

[NEXT]
- Action item 1
- Action item 2
```

**Rules:**
- Only these 5 tags are valid
- No custom tags, no tables, no prose
- Bullet points only (`-` or `*`)
- Omit empty sections

The `patch_state.py` script parses this format and updates your state file automatically, including the `<locked_decisions>` and `<rejected_ideas>` in your SESSION INJECTION block.

---

## Automation Script

The `patch_state.py` script handles context loading and checkpoint parsing:

**LOAD: Start a session**
```bash
python tools/patch_state.py load my-project.md
# Copies CORE_PROMPT + thread state to clipboard
# Paste into Claude/GPT/Gemini
```

**PATCH: End a session**
```bash
# After saying CHECKPOINT, copy AI output to clipboard, then:
python tools/patch_state.py patch my-project.md
# Script updates <locked_decisions>, <rejected_ideas>, and Next Actions
```

**Options:**
```bash
python tools/patch_state.py patch my-project.md --auto  # Skip confirmations
```

**Always use `load` to start sessions** :: it ensures CORE_PROMPT is included, which defines the CHECKPOINT format. Without CORE_PROMPT, the AI may improvise and output non-standard formats.

---

## What Makes It Different

| Typical AI Workflow | Context Protocol |
|---------------------|------------------|
| Memory on their servers | Memory in **your** files |
| Locked to one model | Works on Claude, GPT-4, Gemini |
| Vector DBs, embeddings, RAG | Plain markdown + Git |
| Agent decides next step | **You** decide, AI proposes |
| Proprietary formats | Readable in 100 years |
| Trust the AI | Trust yourself |

---

## Why "Sovereign"?

Most AI memory solutions:
- Store your data on their servers
- Lock you into their ecosystem
- Charge API fees to retrieve your own thoughts
- Use opaque formats you can't inspect

**Context Protocol is sovereign-first:**
- **Local-first:** Text files on your machine
- **Model-agnostic:** Switch providers mid-thought
- **Auditable:** Full Git history of every decision
- **Portable:** Plain markdown, no dependencies
- **Future-proof:** Readable forever

---

## Philosophy

> **This is not a tool. It's a way of thinking.**

Agents try to make AI autonomous.
This system keeps humans in the loop by design.

The AI proposes. You ratify. The system records.

**Manual where decisions matter is a feature.**

Every CHECKPOINT is a human review point. Every commit is an audit trail. Every state file is a thinking artifact you own completely.

---

## FAQ

### "This is just good note-taking"

Yes. Good note-taking plus explicit contracts plus enforcement.
That's the point. Systems beat magic.

### "This doesn't scale"

It's not meant to scale. It's meant to think clearly.
This is a personal cognitive system, not enterprise software.

### "Better models will fix this"

Statelessness is architectural, not about model quality.
Even perfect models reset between sessions.

### "Why not use agents?"

Agents are great for automation. This is for cognition.
Different problems, different solutions.

### "This is too manual"

Manual where decisions matter is a feature, not a bug.
The friction is intentional :: it's your quality control checkpoint.

### "What about [Mem.ai / Notion AI / etc]?"

Those store your data on their servers.
This is sovereign-first. Your files, your machine, your control.

### "CHECKPOINT gave me a weird format"

You probably forgot to include CORE_PROMPT at session start. Always use:
```bash
python tools/patch_state.py load my-project.md
```
This ensures CORE_PROMPT is included, which defines the strict CHECKPOINT format.

---

## Validation

Tested across Claude, GPT, and Gemini:

| Test | Result |
|------|--------|
| Constraint enforcement | ✅ Pass |
| Rejected idea protection | ✅ Pass |
| Scope lock compliance | ✅ Pass |
| Checkpoint format consistency | ✅ Pass |

The protocol is model-agnostic. Same files work everywhere.

---

## Documentation

For a high-level architectural overview to share with your team, download the **[Executive Summary (PDF)](docs/context-protocol-one-pager.pdf)**.

---

## Repository Structure

```
context-protocol/
├── README.md               # This file
├── CORE_PROMPT.md          # Paste this first every session
├── THREAD_TEMPLATE.md      # Copy this for new projects
├── USAGE_GUIDE.md          # Deep dive on workflow
├── CONTRIBUTING.md         # How to contribute
├── SECURITY.md             # Security considerations
├── tools/
│   └── patch_state.py      # Automation script
├── examples/
│   ├── README.md           # Examples overview
│   ├── PROJECT_STATE.md    # Example: software project
│   └── STRATEGY_STATE.md   # Example: strategic planning
├── docs/
│   ├── context-protocol-one-pager.pdf  # Executive summary
│   ├── comparison-table.png            # Old vs New comparison
│   └── README.md                       # Documentation index
└── LICENSE                 # MIT
```

---

## The Mantra

```
The LLM proposes.
You ratify.
The system records.
```

```
load → work → CHECKPOINT → patch → push
```

---

## License

MIT. Fork it. Adapt it. Own it.

---

## Contributing

This is a thinking system, not software. Contributions welcome:
- Improvements to the core prompt
- New examples for different use cases
- Workflow optimizations
- Bug fixes to the automation script

Open an issue or PR.

---

## Author

Built by a practitioner who uses LLMs daily for long-horizon thinking.

Also the author of [DeckBuilder](https://github.com/zohaibus/deckbuilder), a local-first presentation editor. Same philosophy: your files, your control.

This repository contains no proprietary employer information and was developed independently using publicly available principles.

If this helps you think more clearly, that's the goal.