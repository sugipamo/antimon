# antimon

[![Version](https://img.shields.io/badge/version-0.2.13-blue.svg)](https://github.com/antimon-security/antimon/releases)

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

## Quick Start

antimon is designed to be simple and focused. It primarily works through JSON input, making it ideal for integration with AI coding assistants and CI/CD pipelines:

```bash
# Example 1: Detect attempt to write to sensitive file
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "malicious"}}' | antimon
# Output: Security issue detected: Attempt to access sensitive file: /etc/passwd

# Example 2: Detect hardcoded API key
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "config.py", "content": "api_key = \"your-api-key-here\""}}' | antimon
# Output: Security issue detected: API key found in content

# Example 3: Safe operation (should pass)
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "main.py", "content": "print(\"Hello World\")"}}' | antimon
# Output: (no output, exit code 0)
```

## Design Philosophy

antimon follows a minimalist design approach, focusing on essential functionality:

### Core Principles

1. **Simplicity First**: antimon is intentionally kept simple with a focused feature set
2. **JSON-Based Interface**: All security validation happens through JSON input via stdin
3. **AI Assistant Integration**: Optimized for use as a security hook with AI coding tools
4. **Clear Communication**: Debug messages provide transparency about what's being checked

### Primary Use Cases

- Integration with AI coding assistants (Claude Code, etc.)
- CI/CD pipeline security checks
- Automated security validation via JSON input
- Pre-commit hooks and automated workflows


## Usage

### Command Line Usage

#### Available Commands

```bash
# Initialize Claude Code integration
antimon init

# List all security detectors
antimon list

# List configured patterns from config file
antimon list --patterns

# Create configuration file
antimon config

# Test a specific AI detector
antimon test sql_injection
```

#### JSON Input Mode (Primary Interface)

```bash
# Validate JSON input from stdin
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "/etc/passwd", "content": "test"}}' | antimon

# Or use with a file
cat hook_data.json | antimon

# Real-world example: Save hook data and validate
cat > suspicious_operation.json << EOF
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "deploy.py",
    "old_string": "# Deploy script",
    "new_string": "import openai\\nopenai.api_key = 'sk-proj-123456'"
  }
}
EOF
cat suspicious_operation.json | antimon
```

### As a Claude Code hook

#### Automatic Setup

Use the interactive setup wizard:

```bash
# Initialize antimon with Claude Code integration
antimon init
```

#### Manual Setup

Claude Code supports three levels of settings files with different priorities:

1. **Project-local settings** (`.claude/settings.local.json`) - Personal, not committed to Git
2. **Project settings** (`.claude/settings.json`) - Shared with team, committed to Git  
3. **Global settings** (`~/.claude/settings.json`) - User-wide configuration

**Recommended: Project-local setup** for individual security preferences:

Create `.claude/settings.local.json` in your project root:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|Task",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -m antimon"
          }
        ]
      }
    ]
  }
}
```

**Alternative: Global setup** for all projects:

```bash
# Add to ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command", 
            "command": "antimon"
          }
        ]
      }
    ]
  }
}
```

### As a Python module

```python
from antimon import (
    detect_filenames, 
    detect_llm_api, 
    detect_api_key,
    detect_docker,
    detect_localhost,
    validate_hook_data
)

# Example 1: Check all detectors at once using validate_hook_data
json_data = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Write", 
    "tool_input": {
        "file_path": "/home/user/.env",
        "content": "OPENAI_API_KEY=sk-1234567890abcdef"
    }
}

has_issues, messages = validate_hook_data(json_data)
if has_issues:
    for message in messages:
        print(f"Security issue: {message}")

# Example 2: Use specific detectors
# Check for dangerous filenames
result = detect_filenames(json_data)
if result.detected:
    print(f"Filename issue: {result.message}")

# Check for external LLM APIs
content_with_llm = {
    "hook_event_name": "PreToolUse",
    "tool_name": "Write",
    "tool_input": {
        "file_path": "chat.py",
        "content": "from openai import OpenAI\\nclient = OpenAI()"
    }
}
result = detect_llm_api(content_with_llm)
if result.detected:
    print(f"LLM API detected: {result.message}")
    print(f"Suggestion: {result.suggestion}")

# Example 3: Integration in your own validation pipeline
def validate_code_change(hook_data):
    """Custom validation function using antimon"""
    issues = []
    
    # Run all antimon detectors
    has_issues, messages = validate_hook_data(hook_data)
    for message in messages:
        # Parse detector type from message if needed
        issues.append({
            'severity': 'high' if 'sensitive file' in message or 'API key' in message else 'medium',
            'message': message
        })
    
    # Add your custom validations
    if hook_data.get('tool_input', {}).get('file_path', '').endswith('.prod.yaml'):
        issues.append({
            'severity': 'high',
            'detector': 'custom',
            'message': 'Direct production file modification detected'
        })
    
    return issues

# Example 4: Create a validate_all helper function
def validate_all(hook_data):
    """Helper function to run all detectors individually"""
    from antimon import (
        detect_filenames, detect_llm_api, detect_api_key,
        detect_docker, detect_localhost, detect_claude_antipatterns,
        DetectionResult
    )
    
    detectors = [
        ('filenames', detect_filenames),
        ('llm_api', detect_llm_api),
        ('api_key', detect_api_key),
        ('docker', detect_docker),
        ('localhost', detect_localhost),
        ('claude_antipatterns', detect_claude_antipatterns)
    ]
    
    results = []
    for name, detector in detectors:
        result = detector(hook_data)
        if result.detected:
            # Add detector name to result
            results.append(DetectionResult(
                detected=True,
                message=result.message,
                detector=name
            ))
    
    return results
```

## Features

### Available Commands

1. **Initialize Integration**: `antimon init` - Setup Claude Code integration
2. **List Detectors**: `antimon list` - View available security detectors
3. **List Patterns**: `antimon list --patterns` - View configured detection patterns
4. **Create Config**: `antimon config` - Generate configuration file template
5. **Test Detectors**: `antimon test DETECTOR` - Test specific AI detectors

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

### JSON Input Examples

Antimon processes JSON input to validate operations before they're executed. This design makes it perfect for integration with AI coding assistants and automation pipelines.

```bash
# Use with JSON input for testing
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "config.py", "content": "api_key = \"sk-123\""}}' | antimon

# Or pipe from a file
cat operation.json | antimon
```

## Common Use Cases

### 1. Protecting Production Systems

```bash
# Create a wrapper script for your CI/CD pipeline
cat > validate_changes.sh << 'EOF'
#!/bin/bash
# Validate all code changes before deployment

for change in changes/*.json; do
    if ! antimon < "$change"; then
        echo "Security violation in $change"
        exit 1
    fi
done
EOF

chmod +x validate_changes.sh
```

### 2. Preventing API Key Leaks

```python
# pre_commit_hook.py
import json
import subprocess
import sys

def check_commit(files):
    """Check files for API keys before commit"""
    for file in files:
        hook_data = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": file,
                "content": open(file).read()
            }
        }
        
        result = subprocess.run(
            ['antimon'],
            input=json.dumps(hook_data),
            text=True,
            capture_output=True
        )
        
        if result.returncode != 0:
            print(f"Security issue in {file}: {result.stderr}")
            return False
    return True
```

### 3. Enforcing Security Policies

```python
# security_policy.py
from antimon import validate_hook_data

class SecurityPolicy:
    """Corporate security policy enforcement"""
    
    BLOCKED_PATHS = [
        '/etc/',
        '/var/log/',
        '~/.aws/',
        '~/.ssh/'
    ]
    
    def validate_file_operation(self, operation):
        # Check with antimon first
        has_issues, messages = validate_hook_data(operation)
        if has_issues:
            return False, messages
        
        # Additional custom checks
        file_path = operation.get('tool_input', {}).get('file_path', '')
        for blocked in self.BLOCKED_PATHS:
            if file_path.startswith(blocked):
                return False, [f"Access to {blocked} is prohibited by policy"]
        
        return True, []
```

### 4. Integration with AI Coding Tools

```bash
# Setup for various AI coding assistants
# Claude Code
claude-code config set hooks.PreToolUse antimon

# Custom AI assistant wrapper
cat > ai_assistant_safe.py << 'EOF'
#!/usr/bin/env python3
import json
import subprocess
import sys

def safe_execute(ai_operation):
    # Validate with antimon first
    result = subprocess.run(
        ['antimon'],
        input=json.dumps(ai_operation),
        text=True,
        capture_output=True
    )
    
    if result.returncode == 0:
        # Safe to proceed
        execute_ai_operation(ai_operation)
    else:
        print(f"Operation blocked: {result.stderr}")
        sys.exit(1)
EOF
```

### 5. Monitoring and Alerting

```python
# security_monitor.py
import json
import logging
from datetime import datetime
from antimon import validate_hook_data

class SecurityMonitor:
    def __init__(self, log_file='security_violations.log'):
        logging.basicConfig(
            filename=log_file,
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def check_operation(self, operation):
        has_issues, messages = validate_hook_data(operation)
        
        if has_issues:
            # Log the violation
            for message in messages:
                logging.warning(f"Security violation detected: {message}")
                logging.warning(f"Operation details: {json.dumps(operation)}")
            
            # Send alert (implement your alerting mechanism)
            self.send_alert(messages, operation)
            
            return False
        return True
    
    def send_alert(self, messages, operation):
        # Example: Send to Slack, email, etc.
        alert_message = f"Security violations detected at {datetime.now()}:\n"
        for message in messages:
            alert_message += f"- {message}\n"
        
        # Implement your alerting logic here
        print(f"ALERT: {alert_message}")
```

## Configuration

Antimon can be configured using an `antimon.toml` file. Generate a sample configuration with:

```bash
antimon config
```

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

## Troubleshooting

### Common Errors and Solutions

#### 1. "No JSON object could be decoded"

**Error:**
```bash
$ echo "not json" | antimon
Error: No JSON object could be decoded
```

**Solution:** Ensure you're passing valid JSON. Use a JSON validator or pretty-print:
```bash
# Validate JSON first
echo '{"hook_event_name": "PreToolUse"}' | python -m json.tool

# Then pipe to antimon
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "test.py", "content": "print()"}}' | antimon
```

#### 2. "Security issue detected" when it shouldn't

**Error:**
```bash
$ echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "config.yaml", "content": "# Example API_KEY=fake"}}' | antimon
Security issue detected: API key found in content
```

**Solution:** False positives can occur with example/fake keys. Current workarounds:
```python
# Option 1: Use clearly fake patterns
content = "# Example: API_KEY=your-key-here"  # Won't trigger

# Option 2: Use placeholders
content = "API_KEY=${API_KEY}"  # Environment variable pattern

# Option 3: Split the string (for documentation)
content = "# Set your API" + "_KEY here"  # Split to avoid detection
```

#### 3. Hook not triggering in Claude Code

**Problem:** Antimon isn't being called by Claude Code.

**Solution:** Verify installation and configuration:
```bash
# 1. Check if antimon is in PATH
which antimon

# 2. Test antimon directly
echo '{"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "test.txt", "content": "test"}}' | antimon

# 3. Verify Claude Code configuration
claude-code config get hooks.PreToolUse

# 4. If not set, configure it
claude-code config set hooks.PreToolUse antimon

# 5. Ensure antimon has execute permissions
chmod +x $(which antimon)
```

#### 4. "Permission denied" errors

**Error:**
```bash
$ antimon < test.json
bash: /usr/local/bin/antimon: Permission denied
```

**Solution:**
```bash
# Fix permissions
chmod +x $(which antimon)

# Or reinstall
pip uninstall antimon
pip install antimon
```

#### 5. Import errors in Python

**Error:**
```python
>>> from antimon import validate_hook_data
ImportError: cannot import name 'validate_hook_data'
```

**Solution:** Check your installation and Python path:
```bash
# Verify installation
pip show antimon

# Reinstall if needed
pip install --upgrade antimon

# Check Python path
python -c "import antimon; print(antimon.__file__)"
```

#### 6. False negatives (missed detections)

**Problem:** Antimon doesn't detect an issue it should.

**Debug steps:**
```python
# Enable verbose output (if available in your version)
import antimon
import json

# Check what detectors are running
data = {"hook_event_name": "PreToolUse", "tool_name": "Write", "tool_input": {"file_path": "test.py", "content": "suspicious content"}}

# Test individual detectors
from antimon import detect_api_key, detect_llm_api, detect_filenames

print("Checking API keys:", detect_api_key(data))
print("Checking LLM APIs:", detect_llm_api(data))
print("Checking filenames:", detect_filenames(data))
```

### Getting Help

1. **Check the exit code:**
   ```bash
   antimon < test.json
   echo $?  # 0=OK, 1=JSON error, 2=Security issue
   ```

2. **Enable debug logging (if supported):**
   ```bash
   ANTIMON_DEBUG=1 antimon < test.json
   ```

3. **Report issues:**
   - Include the exact JSON that causes the problem
   - Include antimon version: `pip show antimon | grep Version`
   - Include Python version: `python --version`

## Development

```bash
# Clone the repository
git clone https://github.com/antimon-security/antimon.git
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