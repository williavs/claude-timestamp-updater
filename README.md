# Claude Timestamp Updater

A Python tool that automatically updates CLAUDE.md configuration files with current date/time information. Designed to keep AI assistants (like Claude Code, OpenCode, Cursor, etc.) temporally aware by injecting aggressive timestamp reminders into their instruction files.

## Why This Exists

AI language models often default to their training cutoff date when generating responses about "current" events. This tool solves that by:

- **Injecting current timestamps** directly into AI instruction files
- **Reinforcing temporal awareness** with bold, aggressive messaging
- **Preventing date confusion** by explicitly stating the current year vs. previous year
- **Automating updates** via cron jobs so timestamps stay fresh

## Features

- 🔍 **Recursive search** - Finds all CLAUDE.md files in a directory tree
- 📝 **Smart updates** - Only modifies the timestamp section, preserves other content
- 🛡️ **Automatic backups** - Creates `.backup` files before changes
- 🔧 **Flexible targeting** - Update single files, specific directories, or entire home folder
- 🎯 **Portable** - Works on any system, no hardcoded paths
- ⚡ **Safe** - Rollback on errors, skip backup/trash directories

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-timestamp-updater.git
cd claude-timestamp-updater

# Make executable
chmod +x update-claude-dates.py

# No dependencies beyond Python 3 standard library!
```

## Usage

### Basic Usage

```bash
# Update all CLAUDE.md files in your home directory
python3 update-claude-dates.py

# Update all CLAUDE.md files in a specific directory
python3 update-claude-dates.py -d /path/to/project

# Update all CLAUDE.md files in current directory
python3 update-claude-dates.py -d .

# Update a single file
python3 update-claude-dates.py -f ~/CLAUDE.md

# Verbose output
python3 update-claude-dates.py -v
```

### Command Line Options

```
-h, --help              Show help message and exit
-d, --directory DIR     Root directory to search (default: home directory)
-f, --file FILE         Update a single specific file
-v, --verbose           Enable verbose output
```

## Automation with Cron

To keep timestamps fresh, run it hourly via cron:

```bash
# Edit your crontab
crontab -e

# Add this line (runs every hour at :00)
0 * * * * /usr/bin/python3 /path/to/update-claude-dates.py >> /var/log/claude-date-updates.log 2>&1

# Or run it every 15 minutes
*/15 * * * * /usr/bin/python3 /path/to/update-claude-dates.py >> /var/log/claude-date-updates.log 2>&1
```

## How It Works

The script looks for special marker comments in your CLAUDE.md files:

```markdown
<!-- TIMESTAMP-START-DO-NOT-EDIT -->
... timestamp content here ...
<!-- TIMESTAMP-END-DO-NOT-EDIT -->
```

**If markers exist**: It replaces everything between them with fresh timestamp data.

**If markers don't exist**: It adds the timestamp section at the beginning of the file.

### Example Output

```markdown
<!-- TIMESTAMP-START-DO-NOT-EDIT -->
# 🚨 CRITICAL TEMPORAL AWARENESS UPDATE 🚨

## MANDATORY DATE/TIME RECOGNITION - READ THIS FIRST!

**CURRENT ACTUAL DATE AND TIME:**
- **TODAY IS: Friday, October 03, 2025**
- **CURRENT DATE: 2025-10-03**
- **CURRENT TIME: 11:47:23**
- **THE YEAR IS: 2025**
- **IT IS NOT 2024! IT IS 2025!**

### ENFORCEMENT PROTOCOL:
1. **ALWAYS use 2025 when referencing current year**
2. **When using WebSearch, ALWAYS include "2025" in queries for recent content**
3. **NEVER default to 2024 - that was last year**
4. **If you think it's 2024, YOU ARE WRONG - check this header again**

### Examples of CORRECT date usage:
- "The latest docs from 2025"
- "Recent updates in October 2025"
- "Current 2025 best practices"

### VIOLATION ALERT:
Using 2024 for current events = TEMPORAL CONFUSION = FAILURE

**Last Updated: 2025-10-03 11:47:23**
<!-- TIMESTAMP-END-DO-NOT-EDIT -->
```

## Use Cases

### Individual Developers
- Keep your personal AI assistants temporally aware
- Update local CLAUDE.md files before starting work
- Ensure AI responses reference current dates

### Multi-Project Environments
- Update all project instruction files at once
- Coordinate timestamp updates across development environment
- Maintain consistency across multiple AI tools

### Team Environments
- Sync timestamp updates via CI/CD
- Ensure all team members' AI configs stay current
- Prevent temporal confusion in collaborative AI-assisted development

## Safety Features

- **Automatic backups**: Creates `.backup` files before any modifications
- **Rollback on error**: Restores from backup if update fails
- **Skip trash directories**: Ignores `.backup`, `.trash` paths
- **Read-only search**: File scanning doesn't modify anything
- **Validation**: Checks file existence before operations

## Configuration

The script includes these key components:

```python
START_MARKER = "<!-- TIMESTAMP-START-DO-NOT-EDIT -->"
END_MARKER = "<!-- TIMESTAMP-END-DO-NOT-EDIT -->"
```

Change these if you want custom markers, though these are designed to work with standard Claude Code configs.

## Troubleshooting

### No files found
```bash
# Check if CLAUDE.md files exist
find ~ -name "CLAUDE.md" -type f 2>/dev/null | head -10

# Try with explicit directory
python3 update-claude-dates.py -d /your/specific/path -v
```

### Permission errors
```bash
# Make sure you have write permissions
ls -la ~/CLAUDE.md

# Check if files are locked or in use
lsof ~/CLAUDE.md
```

### Backup files piling up
```bash
# Remove old backups (be careful!)
find ~ -name "CLAUDE.md.backup" -type f -delete
```

## Contributing

Contributions welcome! This tool is simple by design, but improvements could include:

- [ ] Support for multiple marker formats
- [ ] Customizable timestamp templates
- [ ] Dry-run mode to preview changes
- [ ] Parallel processing for large file sets
- [ ] Integration with other AI tool configs

## License

MIT License - use freely, modify as needed.

## Credits

Created to solve the "AI thinks it's 2024" problem in multi-agent development environments.

## Related Projects

- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI for Claude
- [Cursor](https://cursor.sh) - AI-first code editor
- [OpenCode](https://github.com/opencodeinterpreter/OpenCodeInterpreter) - Open source code interpreter
