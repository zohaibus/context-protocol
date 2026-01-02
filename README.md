# Context Protocol

> **The LLM is the CPU. Your files are the memory. You are the operating system.**
⚠️ Not affiliated with Anthropic's Model Context Protocol (MCP). This is a human workflow protocol for manual context injection using markdown + Git — not an MCP server implementation.

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
│    Claude │ GPT-4 │ Gemini — Interchangeable                │
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
| `HARD STOP` | Emergency brake — stop completely |
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
START SESSION:
1. Paste CORE_PROMPT.md (the rules)
2. Paste your thread state (the context)
3. Work normally

END SESSION:
1. Say "CHECKPOINT"
2. Copy the structured output
3. Update your state file
4. Git commit
```

---

## Quick Start

### Prerequisites
- A text editor (VS Code, Obsidian, or any markdown editor)
- Git
- An LLM (Claude, GPT-4, or Gemini)

### Setup

```bash
git clone https://github.com/zohaibus/context-protocol.git
cd context-protocol
pip install -r requirements.txt
```

### First Session

1. Copy `THREAD_TEMPLATE.md` to `my-project.md`
2. Edit the template with your project context
3. Open Claude/GPT/Gemini
4. Paste contents of `CORE_PROMPT.md`
5. Paste contents of `my-project.md`
6. Start working

### End Session

1. Type: `CHECKPOINT`
2. AI outputs a structured state patch
3. Update your `my-project.md` file
4. Commit: `git commit -am "checkpoint: [summary]"`

### Automation (Optional)

```bash
# Copy CHECKPOINT output to clipboard, then:
python tools/patch_state.py my-project.md

# Script parses the patch and updates your file
```

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
The friction is intentional — it's your quality control checkpoint.

### "What about [Mem.ai / Notion AI / etc]?"

Those store your data on their servers.
This is sovereign-first. Your files, your machine, your control.

---

## Validation

Tested across Claude, GPT-4, and Gemini:

| Test | Result |
|------|--------|
| Constraint enforcement | ✅ Pass |
| Rejected idea protection | ✅ Pass |
| Scope lock compliance | ✅ Pass |
| Checkpoint format consistency | ✅ Pass |

The protocol is model-agnostic. Same files work everywhere.

---

## Repository Structure

## Documentation

For a high-level architectural overview to share with your team, download the **[Executive Summary (PDF)](docs/context-protocol-one-pager.pdf)**.

---

## Updated Repository Structure

Update the repository structure to include the new files:

```
context-protocol/
├── README.md               # This file
├── CORE_PROMPT.md          # Paste this first every session
├── THREAD_TEMPLATE.md      # Copy this for new projects
├── USAGE_GUIDE.md          # Deep dive on workflow
├── CONTRIBUTING.md         # How to contribute
├── tools/
│   └── patch_state.py      # Optional automation script
├── examples/
│   ├── README.md           # Examples overview
│   ├── PROJECT_STATE.md    # Example: software project
│   └── STRATEGY_STATE.md   # Example: strategic planning
├── docs/
│   |── context-protocol-one-pager.pdf  # Executive summary
│   |── comparison-table.png            # Old vs New Comparison
|   |── README.md                       # Example : Exec Summary for Teams
└── LICENSE                 # MIT
```

## The Mantra

```
The LLM proposes.
You ratify.
The system records.
```

---

## License

MIT — Fork it. Adapt it. Own it.

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

This repository contains no proprietary employer information and was developed independently using publicly available principles.

If this helps you think more clearly, that's the goal.
