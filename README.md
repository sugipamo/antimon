# antimon

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourusername/antimon/releases)

A security validation tool for AI coding assistants that detects potentially dangerous operations and prohibited patterns in code modifications.

## Overview

`antimon` is a Python package that can be used as a pre-hook for AI coding assistants (like Claude Code) to validate code modifications before they are applied. It helps prevent:

- Access to sensitive system files
- Usage of external LLM APIs
- Hardcoded API keys
- Docker operations
- Unsafe localhost connections
- Anti-patterns detected by Claude

## Installation

```bash
pip install antimon
```

Or using uv:

```bash
uv pip install antimon
```

## Usage

### As a command-line tool

```bash
# Validate JSON input from stdin
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "test"}}' | antimon

# Or use with a file
cat hook_data.json | antimon
```

### As a Claude Code hook

Add to your Claude Code settings:

```json
{
  "hooks": {
    "PreToolUse": "antimon"
  }
}
```

### As a Python module

```python
from antimon import detect_filenames, detect_llm_api, detect_api_key

# Example JSON data from a hook
json_data = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Write", 
    "tool_input": {
        "file_path": "/home/user/config.json",
        "content": "api_key = 'secret'"
    }
}

# Check for dangerous filenames
result = detect_filenames(json_data)
if result.detected:
    print(f"Warning: {result.message}")

# Check for API keys
result = detect_api_key(json_data)
if result.detected:
    print(f"Warning: {result.message}")
```

## Features

### Detection Capabilities

1. **Filename Detection**: Prevents access to sensitive files like `/etc/passwd`, `.ssh/id_rsa`, `secrets.yaml`
2. **LLM API Detection**: Detects references to OpenAI, Gemini, GPT and suggests local alternatives
3. **API Key Detection**: Finds hardcoded API keys in code
4. **Docker Detection**: Identifies Docker-related operations
5. **Localhost Detection**: Catches localhost and specific port accesses
6. **Claude Anti-pattern Detection**: Uses Claude to detect fallback patterns and workarounds

### Exit Codes

- `0`: No issues detected (or non-code-editing operation)
- `1`: JSON parsing error
- `2`: Security issues detected

## Configuration

Antimon can be configured using an `antimon.toml` file. Place this file in your project root or specify its location with the `--config` flag.

Example `antimon.toml`:

```toml
# Enable/disable specific detectors
[detectors]
filenames = true
llm_api = true
api_key = true
docker = true
localhost = true
claude_antipatterns = true  # Enable Claude-based anti-pattern detection

# Custom patterns
[patterns]
filename_blacklist = [
    "credentials.json",
    "*.pem",
    "deploy_key"
]

# Whitelist specific files
[whitelist]
files = [
    "test_secrets.yaml",
    "example_config.json"
]
```

Note: Configuration file support is planned for version 0.3.0. The above example shows the planned configuration format. Currently, antimon uses built-in patterns only.

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/antimon.git
cd antimon

# Install in development mode
uv pip install -e .

# Run tests
python -m pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License