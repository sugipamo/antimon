#!/usr/bin/env python3
"""
Example script showing how to use antimon
"""

import json
import sys
from pathlib import Path

# Add parent directory to path so we can import antimon
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from antimon import __version__, validate_hook_data


def run_example(filename: str) -> None:
    """Run a single example file"""
    print(f"\n{'='*60}")
    print(f"Running example: {filename}")
    print('='*60)

    filepath = Path(__file__).parent / filename

    with open(filepath) as f:
        json_data = json.load(f)

    print(f"Tool: {json_data.get('tool_name', 'N/A')}")
    print(f"File path: {json_data.get('tool_input', {}).get('file_path', 'N/A')}")

    has_issues, issues = validate_hook_data(json_data)

    if has_issues:
        print("\n❌ Security issues detected:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ No security issues detected")

def main():
    """Run all examples"""
    print(f"antimon version {__version__} - Security validation examples")

    examples = [
        "example_dangerous.json",
        "example_api_key.json",
        "example_safe.json"
    ]

    for example in examples:
        run_example(example)

    print(f"\n{'='*60}")
    print("Examples completed!")

if __name__ == "__main__":
    main()
