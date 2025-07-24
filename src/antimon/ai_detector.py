# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
AI-powered detection using OpenAI API
"""

import os
import time
from typing import Optional

from .constants import AI_API_BASE
from .detectors import DetectionResult, HookData
from .audit_logger import log_llm_interaction


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
        self.api_base = api_base or AI_API_BASE
        
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
        detector_name: str = "unknown",
        file_path: str = "unknown"
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
            
            # Simple format only: first line is True/False/Invalid
            system_prompt = """あなたはセキュリティ検証AIです。"""
            
            user_prompt = f"""**重要: 必ず以下の形式で回答してください:**

1行目: True, False, Invalid のいずれか（括弧や他の文字は一切含めない）
2行目以降: 理由の説明

## 判定基準
{prompt}

## 編集内容
{content}"""
            
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Make the API call with timing
            start_time = time.time()
            response = self.requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            api_duration = time.time() - start_time
            
            if response.status_code != 200:
                return DetectionResult(
                    detected=False,
                    message=f"API error: {response.status_code} - {response.text[:100]}",
                    severity="error"
                )
            
            # Parse response
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse simple format response
            lines = content.strip().split('\n')
            if len(lines) >= 1:
                first_line = lines[0].strip().lower()
                message = lines[1].strip() if len(lines) > 1 else "No description provided"
                
                if first_line == "true":
                    detection_result = DetectionResult(
                        detected=True,
                        message=message,
                        severity="warning"
                    )
                elif first_line == "false":
                    detection_result = DetectionResult(
                        detected=False,
                        message=message,
                        severity="info"
                    )
                elif first_line == "invalid":
                    detection_result = DetectionResult(
                        detected=False,
                        message=f"Invalid request: {message}",
                        severity="error"
                    )
                else:
                    detection_result = DetectionResult(
                        detected=False,
                        message=f"Failed to parse simple response: {content[:100]}",
                        severity="error"
                    )
            else:
                detection_result = DetectionResult(
                    detected=False,
                    message=f"Failed to parse simple response: {content[:100]}",
                    severity="error"
                )
            
            # Log LLM interaction
            try:
                log_llm_interaction(
                    detector_name=detector_name,
                    model=model,
                    prompt=user_prompt,
                    response=content,
                    file_path=file_path,
                    detected=detection_result.detected,
                    api_call_duration=api_duration
                )
            except Exception:
                pass  # Don't fail detection if logging fails
            
            return detection_result
                
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
        model: str = "gpt-4o-mini",
        detector_name: str = "unknown"
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
        
        # Handle MultiEdit edits array
        if "edits" in tool_input:
            edits = tool_input["edits"]
            if isinstance(edits, list):
                for edit in edits:
                    if isinstance(edit, dict):
                        if "new_string" in edit:
                            content_parts.append(edit["new_string"])
                        if "old_string" in edit:
                            content_parts.append(edit["old_string"])
            
        if not content_parts:
            return DetectionResult(
                detected=False,
                message="No content to analyze",
                severity="info"
            )
        
        content = "\n".join(content_parts)
        file_path = tool_input.get("file_path", "unknown")
        
        return self.detect(
            content=content, 
            prompt=prompt, 
            model=model,
            detector_name=detector_name,
            file_path=file_path
        )