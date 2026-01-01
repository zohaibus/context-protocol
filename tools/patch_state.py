#!/usr/bin/env python3
"""
Context Protocol — State Patch Tool

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
from datetime import datetime

# Try to import pyperclip for clipboard access
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False
    print("⚠️  Install pyperclip for clipboard support: pip install pyperclip")
    print("   Falling back to manual input mode.\n")


def find_core_prompt():
    """Find CORE_PROMPT.md relative to script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check common locations
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
        print("❌ Could not find CORE_PROMPT.md")
        return False
    
    if not os.path.exists(thread_file):
        print(f"❌ Could not find thread file: {thread_file}")
        return False
    
    with open(core_path, 'r', encoding='utf-8') as f:
        # Extract just the code block from CORE_PROMPT.md
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
    
    if HAS_CLIPBOARD:
        pyperclip.copy(full_context)
        print(f"✅ Loaded to clipboard!")
        print(f"   📄 Core prompt: {os.path.basename(core_path)}")
        print(f"   📄 Thread state: {thread_file}")
        print(f"   📋 {len(full_context):,} characters copied")
        print(f"\n👉 Paste into Claude/GPT/Gemini to start session")
    else:
        print("=" * 60)
        print(full_context)
        print("=" * 60)
        print(f"\n👆 Copy the above to start your session")
    
    return True


def get_patch_from_clipboard():
    """Get STATE PATCH from clipboard or manual input."""
    if HAS_CLIPBOARD:
        content = pyperclip.paste()
        if "STATE PATCH" in content or "[ADD]" in content or "[UPDATE]" in content:
            return content
        print("📋 Clipboard doesn't contain a STATE PATCH.")
    
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
        result['thread'] = header_match.group(1)
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


def apply_patch(thread_file, patch_data, auto_mode=False):
    """Apply parsed patch to thread state file."""
    with open(thread_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n📝 Applying changes to {thread_file}:")
    
    changes = []
    
    if patch_data['add_decisions']:
        changes.append(f"  + Adding {len(patch_data['add_decisions'])} decision(s)")
    if patch_data['add_rejected']:
        changes.append(f"  + Adding {len(patch_data['add_rejected'])} rejected idea(s)")
    if patch_data['update_status']:
        changes.append(f"  ~ Updating status")
    if patch_data['next_actions']:
        changes.append(f"  ~ Updating next actions ({len(patch_data['next_actions'])} items)")
    
    for change in changes:
        print(change)
    
    if not changes:
        print("  (no changes to apply)")
        return False
    
    # Confirm
    if not auto_mode:
        response = input("\nApply these changes? (y/n): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return False
    
    # Apply updates to content
    # Update "Last Updated" date
    today = datetime.now().strftime('%Y-%m-%d')
    content = re.sub(r'Last Updated:.*', f'Last Updated: {today}', content)
    
    # Add decisions
    if patch_data['add_decisions']:
        decisions_section = re.search(r'## Decisions Made\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if decisions_section:
            existing = decisions_section.group(1)
            # Count existing numbered items
            existing_numbers = re.findall(r'^(\d+)\.', existing, re.MULTILINE)
            next_num = max([int(n) for n in existing_numbers], default=0) + 1
            
            new_items = '\n'.join(f"{next_num + i}. **{item}**" 
                                  for i, item in enumerate(patch_data['add_decisions']))
            
            insert_pos = decisions_section.end(1)
            content = content[:insert_pos] + '\n' + new_items + content[insert_pos:]
    
    # Add rejected ideas
    if patch_data['add_rejected']:
        rejected_section = re.search(r'## Rejected Ideas\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if rejected_section:
            existing = rejected_section.group(1)
            existing_numbers = re.findall(r'^(\d+)\.', existing, re.MULTILINE)
            next_num = max([int(n) for n in existing_numbers], default=0) + 1
            
            new_items = '\n'.join(f"{next_num + i}. ~~{item}~~" 
                                  for i, item in enumerate(patch_data['add_rejected']))
            
            insert_pos = rejected_section.end(1)
            content = content[:insert_pos] + '\n' + new_items + content[insert_pos:]
    
    # Update status
    if patch_data['update_status']:
        for key, value in patch_data['update_status'].items():
            pattern = rf'\*\*{re.escape(key)}:\*\*.*'
            replacement = f'**{key}:** {value}'
            content = re.sub(pattern, replacement, content)
    
    # Update last session
    if patch_data['next_actions']:
        last_session = f"""## Last Session

**Date:** {today}
**Summary:** [Auto-updated via patch_state.py]
**Next Actions:**
"""
        for i, action in enumerate(patch_data['next_actions'], 1):
            last_session += f"{i}. {action}\n"
        
        # Replace existing Last Session section
        content = re.sub(r'## Last Session\n\n.*?(?=\n##|\Z)', 
                        last_session + '\n', content, flags=re.DOTALL)
    
    # Write updated content
    with open(thread_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Updated {thread_file}")
    
    # Git commit prompt
    if not auto_mode:
        commit = input("Git commit? (y/n): ")
        if commit.lower() == 'y':
            summary = patch_data.get('thread', 'update')
            os.system(f'git add "{thread_file}" && git commit -m "[{summary}] checkpoint: {today}"')
            print("✅ Committed")
    else:
        summary = patch_data.get('thread', 'update')
        os.system(f'git add "{thread_file}" && git commit -m "[{summary}] checkpoint: {today}"')
        print("✅ Committed")
    
    return True


def main():
    if len(sys.argv) < 3:
        print("Context Protocol — State Management Tool")
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
            print("❌ No patch content provided")
            sys.exit(1)
        
        patch_data = parse_state_patch(patch_text)
        
        print(f"\nParsed STATE PATCH:")
        print(f"  Thread: {patch_data['thread']}")
        print(f"  Date: {patch_data['date']}")
        print(f"  Decisions: {len(patch_data['add_decisions'])}")
        print(f"  Rejected: {len(patch_data['add_rejected'])}")
        print(f"  Status updates: {list(patch_data['update_status'].keys())}")
        print(f"  Next actions: {len(patch_data['next_actions'])}")
        
        apply_patch(thread_file, patch_data, auto_mode)
    
    else:
        print(f"❌ Unknown mode: {mode}")
        print("   Use 'load' or 'patch'")
        sys.exit(1)


if __name__ == "__main__":
    main()
