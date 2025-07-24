# antimon - Frequently Asked Questions (FAQ)

## General Questions

### What is antimon?

antimon is a security validation tool for AI coding assistants (like Claude Code) that detects potentially dangerous operations and prohibited patterns in code modifications. It acts as a pre-hook that validates code changes before they are applied.

### Why should I use antimon?

AI coding assistants are powerful but can sometimes generate code that:
- Accesses sensitive system files
- Contains hardcoded API keys
- Uses external LLM APIs when local alternatives exist
- Performs unsafe operations

antimon helps prevent these issues before they happen.

### Is antimon only for Claude Code?

No! While antimon integrates seamlessly with Claude Code, it can be used with any tool that can pipe JSON data. It's also useful in CI/CD pipelines, pre-commit hooks, and security audits.

## Installation & Setup

### How do I install antimon?

```bash
# Using pip
pip install antimon

# Using uv (recommended)
uv pip install antimon
```

### How do I set up antimon with Claude Code?

The easiest way is to use the automatic setup:

```bash
# Automatic setup wizard
antimon --setup-claude-code

# Or manual setup
claude-code config set hooks.PreToolUse antimon

# Verify it's working
antimon --status
```

### antimon is not working with Claude Code. What should I check?

1. **Check if antimon is in PATH:**
   ```bash
   which antimon
   ```

2. **Test antimon directly:**
   ```bash
   echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "test.txt", "content": "test"}}' | antimon
   ```

3. **Verify Claude Code configuration:**
   ```bash
   claude-code config get hooks.PreToolUse
   ```

4. **Ensure antimon has execute permissions:**
   ```bash
   chmod +x $(which antimon)
   ```

## Usage Questions

### How do I check a file without using JSON?

antimon supports direct file checking:

```bash
# Check a single file
antimon --check-file config.py

# Check with verbose output
antimon --check-file main.py --verbose

# Check with specific allowed files
antimon --check-file deploy.py --allow-file '*.env'
```

### How do I check code snippets directly?

You can check code content without creating a file:

```bash
# Check a code snippet
antimon --check-content 'api_key = "sk-1234567890abcdef"'

# Check with dry-run mode
antimon --check-content 'import openai' --dry-run
```

### What's the difference between --dry-run and normal mode?

- **Normal mode**: Blocks operations and returns exit code 2 when issues are found
- **Dry-run mode**: Shows what would be detected but returns exit code 0 (success)

Dry-run is useful for:
- Testing configurations
- Understanding why code is being flagged
- CI/CD pipelines where you want warnings but not failures

### How do I see what antimon checked after a run?

Use the `--stats` option to see detailed statistics:

```bash
# With JSON input
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "test.py", "content": "print()"}}' | antimon --stats

# With file checking
antimon --check-file main.py --stats
```

## Common Issues & Solutions

### "Security issue detected" but it's a false positive

antimon might flag legitimate code. Here are your options:

1. **Allow specific files:**
   ```bash
   antimon --allow-file '~/.config/app.conf'
   antimon --allow-file '*.env'
   antimon --allow-file 'config/*.json'
   ```

2. **Disable specific detectors:**
   ```bash
   antimon --disable-detector api_key
   antimon --disable-detector localhost --disable-detector docker
   ```

3. **For documentation/examples with fake API keys:**
   ```python
   # Instead of: API_KEY = "sk-fake123"
   # Use: API_KEY = "your-api-key-here"
   # Or: API_KEY = "${API_KEY}"
   ```

### "No JSON object could be decoded" error

This means the input is not valid JSON. Common issues:

- Missing quotes around strings
- Trailing commas after the last item
- Unescaped quotes in strings (use `\"`)
- Missing brackets or braces

Test your JSON:
```bash
# Validate JSON first
echo '{"your": "json"}' | python -m json.tool
```

### antimon blocks my CI/CD pipeline unnecessarily

For CI/CD pipelines, consider:

1. **Use dry-run mode for warnings only:**
   ```bash
   antimon --dry-run
   ```

2. **Allow test files:**
   ```bash
   antimon --allow-file '*.test.py' --allow-file 'tests/*'
   ```

3. **Disable detectors not relevant to CI:**
   ```bash
   antimon --disable-detector claude_antipatterns
   ```

### How do I get more information about why something was blocked?

After antimon blocks an operation:

```bash
# Use verbose mode for more context
antimon --check-file problematic.py --verbose
```

## Configuration Questions

### Can I create a configuration file?

Configuration file support (`antimon.toml`) is planned for version 0.3.0. Currently, you can use:

- Command-line options for runtime configuration
- Environment variables:
  - `ANTIMON_IGNORE_PATTERNS`: Comma-separated patterns to ignore
  - `ANTIMON_ALLOW_FILES`: Comma-separated files to allow
  - `ANTIMON_DISABLE_DETECTORS`: Comma-separated detectors to disable

### What detectors are available?

antimon includes these detectors:

1. **filenames**: Prevents access to sensitive files
2. **llm_api**: Detects external LLM API usage
3. **api_key**: Finds hardcoded API keys
4. **docker**: Identifies Docker operations
5. **localhost**: Catches localhost connections
6. **claude_antipatterns**: AI-powered pattern detection
7. **bash**: Detects dangerous bash commands
8. **read**: Prevents reading sensitive files

### How do I disable the colored output?

Use the `--no-color` option:

```bash
antimon --check-file script.py --no-color
```

This is useful for:
- CI/CD pipelines
- Terminals that don't support colors
- Log files

## Integration Questions

### How do I use antimon in a pre-commit hook?

Create a `.git/hooks/pre-commit` file:

```bash
#!/bin/bash
# Check all Python files being committed
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'); do
    if ! antimon --check-file "$file" --quiet; then
        echo "Security issues found in $file"
        exit 1
    fi
done
```

### How do I use antimon in GitHub Actions?

Add to your `.github/workflows/security.yml`:

```yaml
- name: Install antimon
  run: pip install antimon

- name: Check Python files
  run: |
    for file in $(find . -name "*.py" -type f); do
      antimon --check-file "$file" --allow-file "tests/*"
    done
```

### Can I use antimon with other AI assistants?

Yes! Any tool that can output JSON in antimon's format can use it. Example wrapper:

```python
import json
import subprocess

def check_with_antimon(file_path, content):
    hook_data = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": file_path,
            "content": content
        }
    }
    
    result = subprocess.run(
        ['antimon'],
        input=json.dumps(hook_data),
        text=True,
        capture_output=True
    )
    
    return result.returncode == 0
```

## Troubleshooting

### antimon is slow on large files

For large codebases:

1. Use specific file paths instead of wildcards when possible
2. Disable detectors you don't need
3. Consider checking only changed files in CI/CD

### I'm getting "Permission denied" errors

Fix permissions:
```bash
chmod +x $(which antimon)

# Or reinstall
pip uninstall antimon
pip install antimon
```

### antimon isn't detecting an issue it should

Enable verbose mode to see what's being checked:
```bash
antimon --check-file suspicious.py --verbose
```

If it's still not detected, please report it as an issue on GitHub.

## Getting Help

### Where can I report bugs or request features?

Please visit our GitHub repository:
https://github.com/your-org/antimon/issues

### How can I contribute to antimon?

We welcome contributions! See our repository for:
- Contributing guidelines
- Development setup
- Testing procedures

### Where can I find more examples?

1. Run the interactive demo:
   ```bash
   antimon --demo
   ```

2. Check the `examples/` directory in the repository

3. See the README for comprehensive usage examples

### Is there a community or support channel?

Currently, the best place for support is:
- GitHub Issues for bugs and features
- GitHub Discussions for questions and community help

---

For more information, visit: https://github.com/your-org/antimon