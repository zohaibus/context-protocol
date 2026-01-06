#!/usr/bin/env python3
"""
Context Protocol :: State Patch Tool

NOTE: This script operates only on local files.
It does not send data anywhere or perform network operations.
No telemetry, no logging of user data, fully offline.

Two modes:
1. LOAD: Copy CORE_PROMPT + thread state to clipboard for session start
2. PATCH: Apply CHECKPOINT output to update thread state file

Usage:
    python patch_state.py load my-project.md     # Load context to clipboard
    python patch_state.py patch my-project.md    # Apply checkpoint from clipboard
    python patch_state.py patch my-project.md --auto  # Auto-apply without confirmation

Requires: pip install pyperclip
"""

import re
import sys
import os
import subprocess
from datetime import datetime

# Try to import pyperclip for clipboard access
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False
    print("Note: Install pyperclip for clipboard support (pip install pyperclip)")
    print("Falling back to manual paste mode.\n")


def copy_to_clipboard_windows(text):
    """Windows-native clipboard copy that preserves Unicode."""
    try:
        process = subprocess.Popen(
            ['powershell', '-command', 'Set-Clipboard -Value $input'],
            stdin=subprocess.PIPE,
            encoding='utf-8'
        )
        process.communicate(input=text)
        return True
    except Exception as e:
        print(f"Warning: Windows clipboard failed: {e}")
        return False


def copy_to_clipboard(text):
    """Copy text to clipboard, preserving Unicode characters."""
    if sys.platform == 'win32':
        if copy_to_clipboard_windows(text):
            return True
    
    if HAS_CLIPBOARD:
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Warning: pyperclip failed: {e}")
    
    return False


def find_core_prompt():
    """Find CORE_PROMPT.md relative to script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    candidates = [
        os.path.join(script_dir, '..', 'CORE_PROMPT.md'),
        os.path.join(script_dir, 'CORE_PROMPT.md'),
        'CORE_PROMPT.md',
    ]
    
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None


def load_mode(thread_file):
    """Load CORE_PROMPT + thread state to clipboard."""
    core_path = find_core_prompt()
    
    if not core_path:
        print("Error: Could not find CORE_PROMPT.md")
        return False
    
    if not os.path.exists(thread_file):
        print(f"Error: Could not find thread file: {thread_file}")
        return False
    
    with open(core_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        core_content = match.group(1) if match else content
    
    with open(thread_file, 'r', encoding='utf-8') as f:
        thread_content = f.read()
    
    # Extract injection block if present
    injection_match = re.search(r'```\n(<thread>.*?</today_focus>.*?)\n```', 
                                thread_content, re.DOTALL)
    if injection_match:
        thread_injection = injection_match.group(1)
    else:
        thread_injection = thread_content
    
    full_context = f"{core_content}\n\n{thread_injection}"
    
    if copy_to_clipboard(full_context):
        print(f"Loaded to clipboard!")
        print(f"   Core prompt: {os.path.basename(core_path)}")
        print(f"   Thread state: {thread_file}")
        print(f"   {len(full_context):,} characters copied")
        print(f"\nPaste into Claude/GPT/Gemini to start session")
    else:
        print("=" * 60)
        print(full_context)
        print("=" * 60)
        print(f"\nCopy the above to start your session")
    
    return True


def get_patch_from_clipboard():
    """Get STATE PATCH from clipboard or manual input."""
    if HAS_CLIPBOARD:
        try:
            content = pyperclip.paste()
            if content and ("STATE PATCH" in content or "[ADD]" in content or "[UPDATE]" in content):
                return content
        except:
            pass
        print("Clipboard does not contain a STATE PATCH.")
    
    print("Paste your STATE PATCH below (press Enter twice when done):\n")
    lines = []
    empty_count = 0
    while empty_count < 2:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            empty_count += 1
        else:
            empty_count = 0
        lines.append(line)
    return "\n".join(lines[:-2]) if len(lines) > 2 else "\n".join(lines)


def parse_state_patch(patch_text):
    """Parse STATE PATCH into structured sections."""
    result = {
        'thread': None,
        'date': None,
        'add_decisions': [],
        'add_rejected': [],
        'add_open_questions': [],
        'remove_open_questions': [],
        'update_status': {},
        'next_actions': [],
    }
    
    # Extract thread and date
    header_match = re.search(r'Thread:\s*(.*?)\s*\|\s*Date:\s*([\d-]+)', patch_text)
    if header_match:
        result['thread'] = header_match.group(1).strip()
        result['date'] = header_match.group(2)
    
    current_section = None
    current_items = []
    
    for line in patch_text.split('\n'):
        line = line.strip()
        
        # Detect section headers
        if '[ADD] DECISIONS MADE' in line:
            current_section = 'add_decisions'
            current_items = result['add_decisions']
        elif '[ADD] REJECTED IDEAS' in line:
            current_section = 'add_rejected'
            current_items = result['add_rejected']
        elif '[ADD] OPEN QUESTIONS' in line:
            current_section = 'add_open_questions'
            current_items = result['add_open_questions']
        elif '[REMOVE] OPEN QUESTIONS' in line:
            current_section = 'remove_open_questions'
            current_items = result['remove_open_questions']
        elif '[UPDATE] STATUS' in line:
            current_section = 'update_status'
            current_items = None
        elif '[NEXT]' in line:
            current_section = 'next_actions'
            current_items = result['next_actions']
        elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
            item = line.lstrip('•-* ').strip()
            if item and current_items is not None:
                current_items.append(item)
            elif item and current_section == 'update_status':
                if ':' in item:
                    key, value = item.split(':', 1)
                    result['update_status'][key.strip()] = value.strip()
    
    return result


def sanitize_for_commit(text):
    """Sanitize text for safe use in git commit messages."""
    if not text:
        return "update"
    safe_text = text.replace('"', '').replace("'", "").replace('`', '')
    safe_text = safe_text.replace('\n', ' ').replace('\r', '')
    safe_text = safe_text.replace('$', '').replace('\\', '')
    safe_text = safe_text.replace(';', '').replace('&', '').replace('|', '')
    return safe_text[:50].strip() or "update"


def git_commit(thread_file, summary, today):
    """Safely commit changes using subprocess."""
    try:
        subprocess.run(
            ['git', 'add', thread_file],
            check=True,
            capture_output=True,
            text=True
        )
        
        safe_summary = sanitize_for_commit(summary)
        commit_msg = f"[{safe_summary}] checkpoint: {today}"
        
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            check=True,
            capture_output=True,
            text=True
        )
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr if e.stderr else 'Unknown error'}")
        return False
    except FileNotFoundError:
        print("Git not found. Please install git or commit manually.")
        return False


def get_next_number_in_list(text):
    """Find the highest number in a numbered list and return next number."""
    numbers = re.findall(r'^(\d+)\.', text, re.MULTILINE)
    if numbers:
        return max(int(n) for n in numbers) + 1
    return 1


def update_injection_block_list(content, tag_name, new_items):
    """
    Update a numbered list inside an XML tag within the SESSION INJECTION code block.
    
    Args:
        content: Full file content
        tag_name: e.g., 'locked_decisions' or 'rejected_ideas'
        new_items: List of strings to append
    
    Returns:
        Updated content
    """
    if not new_items:
        return content
    
    # Pattern to find the tag content within a code block
    # This matches <tag_name>...</tag_name> inside ``` blocks
    pattern = rf'(<{tag_name}>)(.*?)(</{tag_name}>)'
    
    def replacer(match):
        opening_tag = match.group(1)
        existing_content = match.group(2)
        closing_tag = match.group(3)
        
        # Find the next number
        next_num = get_next_number_in_list(existing_content)
        
        # Build new items string
        new_items_str = '\n'.join(
            f"{next_num + i}. {item}" 
            for i, item in enumerate(new_items)
        )
        
        # Append to existing content
        updated_content = existing_content.rstrip() + '\n' + new_items_str + '\n'
        
        return opening_tag + updated_content + closing_tag
    
    return re.sub(pattern, replacer, content, flags=re.DOTALL)


def update_markdown_section(content, section_name, new_items, strikethrough=False):
    """
    Update a markdown section (## Section Name) with new numbered items.
    
    Args:
        content: Full file content
        section_name: e.g., 'Decisions Made' or 'Rejected Ideas'
        new_items: List of strings to append
        strikethrough: If True, wrap items in ~~strikethrough~~
    
    Returns:
        Updated content
    """
    if not new_items:
        return content
    
    # Find the section
    pattern = rf'(## {re.escape(section_name)}\s*\n)(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return content
    
    section_header = match.group(1)
    section_content = match.group(2)
    
    # Find next number
    next_num = get_next_number_in_list(section_content)
    
    # Build new items
    if strikethrough:
        new_items_str = '\n'.join(
            f"{next_num + i}. ~~{item}~~" 
            for i, item in enumerate(new_items)
        )
    else:
        new_items_str = '\n'.join(
            f"{next_num + i}. {item}" 
            for i, item in enumerate(new_items)
        )
    
    # Insert at end of section
    updated_section = section_content.rstrip() + '\n' + new_items_str + '\n'
    
    return content[:match.start()] + section_header + updated_section + content[match.end():]


def mark_open_questions_resolved(content, resolved_items):
    """Mark open questions as resolved by changing [ ] to [x]."""
    if not resolved_items:
        return content
    
    for item in resolved_items:
        # Escape special regex chars in the item
        escaped_item = re.escape(item)
        # Try to find and mark as resolved
        pattern = rf'- \[ \] (.*?{escaped_item}.*?)$'
        content = re.sub(pattern, r'- [x] \1', content, flags=re.MULTILINE | re.IGNORECASE)
    
    return content


def update_last_session(content, today, next_actions):
    """Update the Last Session section."""
    if not next_actions:
        return content
    
    # Build new Last Session section
    last_session = f"""## Last Session

**Date:** {today}
**Summary:** [Auto-updated via patch_state.py]

**Next Actions:**
"""
    for i, action in enumerate(next_actions, 1):
        last_session += f"{i}. {action}\n"
    
    # Replace existing Last Session section
    pattern = r'## Last Session\s*\n.*?(?=\n## |\n---|\Z)'
    
    if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
        content = re.sub(pattern, last_session, content, flags=re.DOTALL | re.IGNORECASE)
    
    return content


def apply_patch(thread_file, patch_data, auto_mode=False):
    """Apply parsed patch to thread state file."""
    with open(thread_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nApplying changes to {thread_file}:")
    
    changes = []
    
    if patch_data['add_decisions']:
        changes.append(f"  + Adding {len(patch_data['add_decisions'])} decision(s) to <locked_decisions>")
    if patch_data['add_rejected']:
        changes.append(f"  + Adding {len(patch_data['add_rejected'])} rejected idea(s) to <rejected_ideas>")
    if patch_data['remove_open_questions']:
        changes.append(f"  - Marking {len(patch_data['remove_open_questions'])} question(s) as resolved")
    if patch_data['update_status']:
        changes.append(f"  ~ Updating status fields")
    if patch_data['next_actions']:
        changes.append(f"  ~ Updating next actions ({len(patch_data['next_actions'])} items)")
    
    for change in changes:
        print(change)
    
    if not changes:
        print("  (no changes to apply)")
        return False
    
    if not auto_mode:
        response = input("\nApply these changes? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return False
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Update Last Updated date
    content = re.sub(r'Last Updated:.*', f'Last Updated: {today}', content, flags=re.IGNORECASE)
    
    # Update <locked_decisions> in SESSION INJECTION block
    if patch_data['add_decisions']:
        content = update_injection_block_list(content, 'locked_decisions', patch_data['add_decisions'])
        # Also update the markdown section if it exists
        content = update_markdown_section(content, 'Decisions Made', patch_data['add_decisions'])
    
    # Update <rejected_ideas> in SESSION INJECTION block
    if patch_data['add_rejected']:
        content = update_injection_block_list(content, 'rejected_ideas', patch_data['add_rejected'])
        # Also update the markdown section if it exists
        content = update_markdown_section(content, 'Rejected Ideas', patch_data['add_rejected'], strikethrough=True)
    
    # Mark resolved open questions
    if patch_data['remove_open_questions']:
        content = mark_open_questions_resolved(content, patch_data['remove_open_questions'])
    
    # Update status fields
    if patch_data['update_status']:
        for key, value in patch_data['update_status'].items():
            # Update in markdown (e.g., **Stage:** value)
            pattern = rf'\*\*{re.escape(key)}:\*\*.*'
            replacement = f'**{key}:** {value}'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Update in status table if present
            table_pattern = rf'\| {re.escape(key)} \|.*?\|'
            table_replacement = f'| {key} | {value} |'
            content = re.sub(table_pattern, table_replacement, content, flags=re.IGNORECASE)
    
    # Update Last Session
    if patch_data['next_actions']:
        content = update_last_session(content, today, patch_data['next_actions'])
    
    # Write updated content
    with open(thread_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nUpdated {thread_file}")
    
    # Show what was added
    if patch_data['add_decisions']:
        print(f"\n  Added to <locked_decisions>:")
        for item in patch_data['add_decisions']:
            print(f"    + {item[:60]}{'...' if len(item) > 60 else ''}")
    
    if patch_data['add_rejected']:
        print(f"\n  Added to <rejected_ideas>:")
        for item in patch_data['add_rejected']:
            print(f"    + {item[:60]}{'...' if len(item) > 60 else ''}")
    
    # Git commit
    if not auto_mode:
        commit = input("\nGit commit? (y/n): ")
        if commit.lower() == 'y':
            if git_commit(thread_file, patch_data.get('thread'), today):
                print("Committed")
    else:
        if git_commit(thread_file, patch_data.get('thread'), today):
            print("Committed")
    
    return True


def main():
    if len(sys.argv) < 3:
        print("Context Protocol :: State Management Tool")
        print()
        print("Usage:")
        print("  python patch_state.py load <thread-file>    Load context to clipboard")
        print("  python patch_state.py patch <thread-file>   Apply checkpoint to file")
        print()
        print("Options:")
        print("  --auto    Skip confirmation prompts")
        print()
        print("Examples:")
        print("  python patch_state.py load my-project.md")
        print("  python patch_state.py patch my-project.md")
        print("  python patch_state.py patch my-project.md --auto")
        print()
        print("CHECKPOINT format expected:")
        print("  [ADD] DECISIONS MADE")
        print("  [ADD] REJECTED IDEAS")
        print("  [REMOVE] OPEN QUESTIONS")
        print("  [UPDATE] STATUS")
        print("  [NEXT]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    thread_file = sys.argv[2]
    auto_mode = '--auto' in sys.argv
    
    if mode == 'load':
        load_mode(thread_file)
    
    elif mode == 'patch':
        print(f"Thread file: {thread_file}")
        print("-" * 40)
        
        patch_text = get_patch_from_clipboard()
        
        if not patch_text.strip():
            print("Error: No patch content provided")
            sys.exit(1)
        
        patch_data = parse_state_patch(patch_text)
        
        print(f"\nParsed STATE PATCH:")
        print(f"  Thread: {patch_data['thread']}")
        print(f"  Date: {patch_data['date']}")
        print(f"  Decisions to add: {len(patch_data['add_decisions'])}")
        print(f"  Rejected to add: {len(patch_data['add_rejected'])}")
        print(f"  Questions resolved: {len(patch_data['remove_open_questions'])}")
        print(f"  Status updates: {list(patch_data['update_status'].keys())}")
        print(f"  Next actions: {len(patch_data['next_actions'])}")
        
        apply_patch(thread_file, patch_data, auto_mode)
    
    else:
        print(f"Error: Unknown mode: {mode}")
        print("Use 'load' or 'patch'")
        sys.exit(1)


if __name__ == "__main__":
    main()