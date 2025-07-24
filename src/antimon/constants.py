# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Configuration constants for antimon
"""

import os

# Default GitHub repository URL
DEFAULT_GITHUB_REPO = "https://github.com/your-org/antimon"

# Allow override via environment variable
GITHUB_REPO_URL = os.environ.get("ANTIMON_GITHUB_URL", DEFAULT_GITHUB_REPO)

# Issue tracker URL
ISSUE_TRACKER_URL = f"{GITHUB_REPO_URL}/issues"

# API Endpoints (centralized for clarity)
API_ENDPOINTS = {
    "openai": {
        "base": "https://api.openai.com/v1",
        "domain": "api.openai.com"
    },
    "google": {
        "domain": "gemini.google.com"
    },
    "anthropic": {
        "domain": "api.anthropic.com"
    },
    "cohere": {
        "domain": "api.cohere.ai"
    }
}

# Default AI detector API base (configurable via environment)
DEFAULT_AI_API_BASE = API_ENDPOINTS["openai"]["base"]
AI_API_BASE = os.environ.get("ANTIMON_AI_API_BASE", DEFAULT_AI_API_BASE)