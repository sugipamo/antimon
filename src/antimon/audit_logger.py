# Copyright (c) 2025 Your Name
# Licensed under the MIT License

"""
Audit logging functionality for antimon
Records security events, blocks, and LLM interactions in JSON format
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

from .config import _find_config_in_parents


def get_audit_log_path() -> str:
    """
    Get the path for antimon.log in the same directory as antimon.toml
    
    Returns:
        Absolute path to the audit log file
    """
    # Find the config file location to determine log directory
    config_path = _find_config_in_parents()
    
    if config_path:
        # Place log file next to config file
        config_dir = Path(config_path).parent
        log_path = config_dir / "antimon.log"
    else:
        # Fallback to current directory
        log_path = Path("./antimon.log")
    
    return str(log_path.resolve())


def log_security_event(
    event_type: str,
    severity: str,
    file_path: str,
    tool_name: str,
    detector_name: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    llm_conversation: Optional[List[Dict[str, str]]] = None
) -> None:
    """
    Log a security event to antimon.log
    
    Args:
        event_type: Type of event ('block', 'warning', 'allow')
        severity: Severity level ('error', 'warning', 'info')
        file_path: Path to the file being checked
        tool_name: Name of the tool being used
        detector_name: Name of the detector that triggered
        message: Human-readable message
        details: Additional details about the event
        llm_conversation: LLM conversation log if applicable
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "severity": severity,
        "file_path": file_path,
        "tool_name": tool_name,
        "detector": detector_name,
        "message": message,
        "details": details or {},
        "llm_conversation": llm_conversation or [],
        "version": "0.2.13"
    }
    
    _append_to_log(log_entry)


def log_llm_interaction(
    detector_name: str,
    model: str,
    prompt: str,
    response: str,
    file_path: str,
    detected: bool,
    api_call_duration: float
) -> List[Dict[str, str]]:
    """
    Log LLM interaction and return conversation for inclusion in security event
    
    Args:
        detector_name: Name of the AI detector
        model: LLM model used
        prompt: Prompt sent to LLM
        response: Response from LLM
        file_path: File being analyzed
        detected: Whether security issue was detected
        api_call_duration: Time taken for API call
        
    Returns:
        Conversation log for inclusion in security event
    """
    conversation = [
        {
            "role": "system", 
            "content": f"AI Security Detector: {detector_name}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Also log as separate LLM interaction event
    llm_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "llm_interaction",
        "detector": detector_name,
        "model": model,
        "file_path": file_path,
        "detected": detected,
        "api_call_duration_ms": round(api_call_duration * 1000, 2),
        "conversation": conversation,
        "version": "0.2.13"
    }
    
    _append_to_log(llm_event)
    
    return conversation


def log_pattern_match(
    pattern_name: str,
    pattern_type: str,
    matched_content: str,
    file_path: str,
    tool_name: str,
    severity: str
) -> None:
    """
    Log pattern-based detection event
    
    Args:
        pattern_name: Name of the pattern that matched
        pattern_type: Type of pattern (content, file, import)
        matched_content: Content that matched the pattern
        file_path: File being checked
        tool_name: Tool being used
        severity: Severity level
    """
    log_security_event(
        event_type="pattern_match",
        severity=severity,
        file_path=file_path,
        tool_name=tool_name,
        detector_name=f"pattern:{pattern_name}",
        message=f"Pattern '{pattern_name}' matched in {pattern_type}",
        details={
            "pattern_name": pattern_name,
            "pattern_type": pattern_type,
            "matched_content": matched_content[:200] + "..." if len(matched_content) > 200 else matched_content
        }
    )


def _append_to_log(log_entry: Dict[str, Any]) -> None:
    """
    Append a log entry to the audit log file
    
    Args:
        log_entry: Log entry to append
    """
    try:
        log_path = get_audit_log_path()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # Append to log file (one JSON object per line)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
    except Exception as e:
        # Don't fail the security check if logging fails
        # Just print to stderr for debugging
        import sys
        print(f"Warning: Failed to write to audit log: {e}", file=sys.stderr)


def log_json_input(json_data: Dict[str, Any], source: str = "stdin") -> None:
    """
    Log raw JSON input for tracing purposes
    
    Args:
        json_data: The JSON data received
        source: Source of the JSON (e.g., "stdin", "file")
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    
    log_entry = {
        "timestamp": timestamp,
        "event_type": "json_input_trace",
        "source": source,
        "raw_json": json_data,
        "version": "0.2.13"
    }
    
    try:
        log_path = get_audit_log_path()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # Append to log file (one JSON object per line)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
    except Exception as e:
        # Don't fail if logging fails
        import sys
        print(f"Warning: Failed to write JSON trace to audit log: {e}", file=sys.stderr)


def get_recent_blocks(hours: int = 24) -> List[Dict[str, Any]]:
    """
    Get recent block events from the audit log
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        List of recent block events
    """
    try:
        log_path = get_audit_log_path()
        
        if not os.path.exists(log_path):
            return []
        
        cutoff_time = time.time() - (hours * 3600)
        recent_blocks = []
        
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('event_type') == 'block':
                        # Parse timestamp
                        entry_time = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                        if entry_time.timestamp() > cutoff_time:
                            recent_blocks.append(entry)
                except json.JSONDecodeError:
                    continue
        
        return sorted(recent_blocks, key=lambda x: x['timestamp'], reverse=True)
        
    except Exception:
        return []