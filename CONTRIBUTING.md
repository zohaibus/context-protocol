# Contributing to Context Protocol

Thank you for your interest in improving Context Protocol.

## Philosophy

This is a **thinking system**, not software. Contributions should:

- Maintain the core mental model (CPU / RAM / OS)
- Keep the protocol simple and portable
- Preserve human-in-the-loop design
- Avoid adding dependencies

## What We Welcome

### High Value
- Bug fixes to `patch_state.py`
- Improvements to constraint enforcement
- New examples for different use cases (consulting, research, design)
- Translations of documentation
- Workflow optimizations that don't add complexity

### Medium Value
- Typo fixes
- Documentation clarifications
- Additional response templates

### Please Discuss First
- Changes to `CORE_PROMPT.md` (this is the stable API)
- New commands or constraint tags
- Automation features
- Integrations with other tools

## Guidelines

### Keep Examples Anonymized

All example state files must be:
- Clearly fictional
- Free of real names, companies, or identifiable data
- Marked with a disclaimer banner

### Keep CORE_PROMPT Stable

The core prompt is designed to be backwards-compatible. Changes should:
- Not break existing state files
- Not require users to update their workflow
- Be tested across Claude, ChatGPT, and Gemini

### No Personal Data

Never commit:
- Real state files
- Personal information
- Company-specific data
- API keys or credentials

The `.gitignore` is configured to prevent accidental commits of `*_STATE.md` files.

## How to Contribute

1. **Open an issue first** for non-trivial changes
2. Fork the repository
3. Create a branch (`git checkout -b fix/your-fix`)
4. Make your changes
5. Test across at least one LLM platform
6. Submit a pull request

## Code Style

- Python: Follow PEP 8
- Markdown: Use consistent header levels
- Keep it simple

## Questions?

Open an issue. We're happy to discuss.

---

*"The LLM proposes. You ratify. The system records."*
