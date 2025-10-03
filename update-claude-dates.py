#!/usr/bin/env python3
"""
CLAUDE.md Date/Time Updater
Updates all CLAUDE.md files with current date/time in a special header section
Preserves all existing content and only updates the timestamp section
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path
import shutil

# The marker comments that define our date section
START_MARKER = "<!-- TIMESTAMP-START-DO-NOT-EDIT -->"
END_MARKER = "<!-- TIMESTAMP-END-DO-NOT-EDIT -->"

def create_timestamp_section():
    """Create the timestamp section with aggressive prompting"""
    now = datetime.now()

    # Format different time representations
    date_str = now.strftime("%Y-%m-%d")  # 2025-08-17
    time_str = now.strftime("%H:%M:%S %Z")  # 14:30:45
    full_date = now.strftime("%B %d, %Y")  # August 17, 2025
    day_name = now.strftime("%A")  # Saturday
    prev_year = now.year - 1
    current_year = now.year
    current_month = now.strftime("%B")
    
    timestamp_content = f"""
{START_MARKER}
# 🚨 CRITICAL TEMPORAL AWARENESS UPDATE 🚨

## MANDATORY DATE/TIME RECOGNITION - READ THIS FIRST!

**CURRENT ACTUAL DATE AND TIME:**
- **TODAY IS: {day_name}, {full_date}**
- **CURRENT DATE: {date_str}**
- **CURRENT TIME: {time_str}**
- **THE YEAR IS: {current_year}**
- **IT IS NOT {prev_year}! IT IS {current_year}!**

### ENFORCEMENT PROTOCOL:
1. **ALWAYS use {current_year} when referencing current year**
2. **When using WebSearch, ALWAYS include "{current_year}" in queries for recent content**
3. **NEVER default to {prev_year} - that was last year**
4. **If you think it's {prev_year}, YOU ARE WRONG - check this header again**

### Examples of CORRECT date usage:
- "The latest docs from {current_year}"
- "Recent updates in {current_month} {current_year}"
- "Current {current_year} best practices"

### VIOLATION ALERT:
Using {prev_year} for current events = TEMPORAL CONFUSION = FAILURE

**Last Updated: {now.strftime("%Y-%m-%d %H:%M:%S")}**
{END_MARKER}
"""
    return timestamp_content

def update_claude_md(filepath):
    """Update a single CLAUDE.md file with timestamp"""
    try:
        # Create backup
        backup_path = f"{filepath}.backup"
        shutil.copy2(filepath, backup_path)
        
        # Read current content
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if timestamp section exists
        if START_MARKER in content and END_MARKER in content:
            # Replace existing timestamp section
            pattern = re.compile(
                re.escape(START_MARKER) + r'.*?' + re.escape(END_MARKER),
                re.DOTALL
            )
            new_content = pattern.sub(create_timestamp_section().strip(), content)
        else:
            # Add timestamp section at the very beginning
            new_content = create_timestamp_section() + "\n" + content
        
        # Write updated content
        with open(filepath, 'w') as f:
            f.write(new_content)
        
        # Remove backup if successful
        os.remove(backup_path)
        return True
        
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        # Restore from backup if it exists
        if os.path.exists(backup_path):
            shutil.move(backup_path, filepath)
        return False

def find_all_claude_md_files(root_dir=None):
    """Find all CLAUDE.md files in the system"""
    claude_files = []

    # Default to home directory if not specified
    if root_dir is None:
        root_dir = str(Path.home())

    # Use Path.rglob for recursive search
    root_path = Path(root_dir)
    
    # Search for CLAUDE.md and claude.md (case variations)
    for pattern in ['CLAUDE.md', 'claude.md']:
        for file_path in root_path.rglob(pattern):
            # Skip backup files and certain directories
            if '.backup' not in str(file_path) and '.trash' not in str(file_path):
                claude_files.append(str(file_path))
    
    return claude_files

def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description="Update CLAUDE.md files with current timestamp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Update all CLAUDE.md files in home directory
  %(prog)s -d /path/to/dir   # Update all CLAUDE.md files in specific directory
  %(prog)s -d .              # Update all CLAUDE.md files in current directory
  %(prog)s -f ~/CLAUDE.md    # Update a single file
        """
    )
    parser.add_argument(
        '-d', '--directory',
        help='Root directory to search for CLAUDE.md files (default: home directory)',
        default=None
    )
    parser.add_argument(
        '-f', '--file',
        help='Update a single CLAUDE.md file instead of searching',
        default=None
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose output',
        action='store_true'
    )

    args = parser.parse_args()

    print(f"🕐 Starting CLAUDE.md timestamp update at {datetime.now()}")

    if args.file:
        # Update single file
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            return 1

        print(f"Updating single file: {args.file}")
        if update_claude_md(args.file):
            print(f"  ✓ Successfully updated")
            return 0
        else:
            print(f"  ✗ Failed to update")
            return 1
    else:
        # Find all CLAUDE.md files
        search_dir = args.directory if args.directory else str(Path.home())
        print(f"Searching in: {search_dir}")

        claude_files = find_all_claude_md_files(search_dir)
        print(f"Found {len(claude_files)} CLAUDE.md file(s)")

        if not claude_files:
            print("⚠️  No CLAUDE.md files found")
            return 0

        # Update each file
        success_count = 0
        for filepath in claude_files:
            if args.verbose:
                print(f"Updating: {filepath}")
            if update_claude_md(filepath):
                success_count += 1
                if args.verbose:
                    print(f"  ✓ Successfully updated")
            else:
                print(f"  ✗ Failed to update: {filepath}")

        print(f"\n✅ Updated {success_count}/{len(claude_files)} files successfully")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())