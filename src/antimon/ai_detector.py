# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
AI-powered detection using OpenAI API
"""

import json
import os
from typing import Dict, Optional

from .detectors import DetectionResult, HookData


class AIDetector:
    """AI-powered security detection using OpenAI or compatible APIs"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        """
        Initialize AI detector
        
        Args:
            api_key: OpenAI API key (or from OPENAI_API_KEY env var)
            api_base: API base URL (for OpenAI-compatible services)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.api_base = api_base or "https://api.openai.com/v1"
        
        # Check if requests is available
        try:
            import requests
            self.requests = requests
        except ImportError:
            self.requests = None
    
    def detect(
        self, 
        content: str, 
        prompt: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        max_tokens: int = 100,
        response_format: str = "json"  # "json" or "simple"
    ) -> DetectionResult:
        """
        Run AI detection on content
        
        Args:
            content: Code content to analyze
            prompt: Detection prompt
            model: Model to use
            temperature: Temperature for response
            max_tokens: Max tokens in response
            
        Returns:
            DetectionResult with AI analysis
        """
        if not self.api_key:
            return DetectionResult(
                detected=False,
                message="OpenAI API key not configured",
                severity="info"
            )
        
        if not self.requests:
            return DetectionResult(
                detected=False,
                message="requests library not installed (pip install requests)",
                severity="info"
            )
        
        try:
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Create the detection prompt based on format
            if response_format == "simple":
                # Simple format: first line is True/False/Invalid
                system_prompt = """You are a security analyzer. 

IMPORTANT: Your response MUST follow this exact format:
- First line: ONLY one of these words: True, False, Invalid
- Second line: Brief description (if True) or reason (if False/Invalid)
- No other text allowed

Rules:
- Use "True" if security issue is found
- Use "False" if no issue is found  
- Use "Invalid" if the code/request is malformed
- Second line should be under 100 characters"""
                
                user_prompt = f"{prompt}\n\nCode to analyze:\n```\n{content}\n```"
                
                data = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            else:
                # JSON format (default)
                system_prompt = """You are a security analyzer. Your response MUST be valid JSON only, no other text.

IMPORTANT: Respond with EXACTLY this JSON structure:
{
  "detected": true,
  "message": "Brief description here",
  "severity": "error"
}

Rules:
- detected: MUST be boolean (true or false), not string
- message: Short description (max 100 chars)
- severity: MUST be one of: "error", "warning", "info"
- If no issue found: {"detected": false, "message": "No issues found", "severity": "info"}
- Do NOT include any text before or after the JSON
- Do NOT use markdown code blocks"""
                
                user_prompt = f"{prompt}\n\nCode to analyze:\n```\n{content}\n```"
                
                data = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "response_format": {"type": "json_object"}  # Force JSON response
                }
            
            # Make the API call
            response = self.requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                return DetectionResult(
                    detected=False,
                    message=f"API error: {response.status_code} - {response.text[:100]}",
                    severity="error"
                )
            
            # Parse response
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse AI response based on format
            if response_format == "simple":
                # Parse simple format
                lines = content.strip().split('\n')
                if len(lines) >= 1:
                    first_line = lines[0].strip().lower()
                    message = lines[1].strip() if len(lines) > 1 else "No description provided"
                    
                    if first_line == "true":
                        return DetectionResult(
                            detected=True,
                            message=message,
                            severity="warning"
                        )
                    elif first_line == "false":
                        return DetectionResult(
                            detected=False,
                            message=message,
                            severity="info"
                        )
                    elif first_line == "invalid":
                        return DetectionResult(
                            detected=False,
                            message=f"Invalid request: {message}",
                            severity="error"
                        )
                
                return DetectionResult(
                    detected=False,
                    message=f"Failed to parse simple response: {content[:100]}",
                    severity="error"
                )
            else:
                # Parse JSON format
                try:
                    ai_result = json.loads(content)
                    return DetectionResult(
                        detected=ai_result.get("detected", False),
                        message=ai_result.get("message", "AI detection completed"),
                        severity=ai_result.get("severity", "warning")
                    )
                except json.JSONDecodeError:
                    return DetectionResult(
                        detected=False,
                        message=f"Failed to parse AI response: {content[:100]}",
                        severity="error"
                    )
                
        except Exception as e:
            return DetectionResult(
                detected=False,
                message=f"AI detection error: {str(e)}",
                severity="error"
            )
    
    def detect_from_hook_data(
        self,
        json_data: HookData,
        prompt: str,
        model: str = "gpt-4o-mini"
    ) -> DetectionResult:
        """
        Run AI detection on hook data
        
        Args:
            json_data: Hook data from AI assistant
            prompt: Detection prompt
            model: Model to use
            
        Returns:
            DetectionResult with AI analysis
        """
        # Extract content to analyze
        tool_input = json_data.get("tool_input", {})
        content_parts = []
        
        if "content" in tool_input:
            content_parts.append(tool_input["content"])
        if "new_string" in tool_input:
            content_parts.append(tool_input["new_string"])
        if "command" in tool_input:
            content_parts.append(tool_input["command"])
            
        if not content_parts:
            return DetectionResult(
                detected=False,
                message="No content to analyze",
                severity="info"
            )
        
        content = "\n".join(content_parts)
        return self.detect(content, prompt, model)