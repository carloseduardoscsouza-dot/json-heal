"""
Core repair engine for corrupted, truncated, or malformed LLM JSON.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple


def strip_markdown_blocks(text: str) -> str:
    """Strips markdown code fences like ```json ... ```"""
    stripped = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", stripped, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # If text starts with ``` but wasn't closed (truncated)
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        first_line = lines[0]
        if first_line.startswith("```"):
            return "\n".join(lines[1:]).strip()
    return stripped


def strip_comments(text: str) -> str:
    """Removes single-line and multi-line comments from JSON string."""
    # Remove // comments
    text = re.sub(r"//.*$", "", text, flags=re.MULTILINE)
    # Remove /* ... */ comments
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return text


def fix_python_literals(text: str) -> str:
    """Replaces unquoted Python literals with valid JSON literals."""
    text = re.sub(r"\bTrue\b", "true", text)
    text = re.sub(r"\bFalse\b", "false", text)
    text = re.sub(r"\bNone\b", "null", text)
    return text


def remove_trailing_commas(text: str) -> str:
    """Removes trailing commas before closing braces/brackets."""
    return re.sub(r",\s*([\]}])", r"\1", text)


def fix_single_quotes(text: str) -> str:
    """Converts single-quoted keys and string values to valid double-quoted JSON."""
    # If standard double quotes are already valid JSON, don't touch
    try:
        json.loads(text)
        return text
    except Exception:
        pass

    # Replace single quotes surrounding keys and values
    # Pattern: 'key': 'value' -> "key": "value"
    def _quote_replace(m):
        return f'"{m.group(1)}"'

    # Replace keys: 'name': -> "name":
    text = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'\s*:", r'"\1":', text)
    # Replace values: : 'value' -> : "value"
    text = re.sub(r":\s*'([^'\\]*(?:\\.[^'\\]*)*)'", r': "\1"', text)
    # Replace array items: ['item1', 'item2'] -> ["item1", "item2"]
    text = re.sub(r"(?<=\[|,)\s*'([^'\\]*(?:\\.[^'\\]*)*)'", r' "\1"', text)
    return text


def close_truncated_json(text: str) -> str:
    """
    Intelligently closes unclosed strings, arrays, and objects
    caused by LLM token limit truncation.
    """
    stack = []
    in_string = False
    escape = False

    for ch in text:
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch in ("{", "["):
                stack.append(ch)
            elif ch == "}":
                if stack and stack[-1] == "{":
                    stack.pop()
            elif ch == "]":
                if stack and stack[-1] == "[":
                    stack.pop()

    # If string was cut off mid-way, close it
    if in_string:
        text += '"'

    # Remove any dangling key or comma before closing
    text = text.rstrip()
    if text.endswith(":"):
        text += ' null'
    if text.endswith(","):
        text = text[:-1].rstrip()

    # Close open brackets/braces in reverse order
    while stack:
        opener = stack.pop()
        if opener == "{":
            text += "}"
        elif opener == "[":
            text += "]"

    return text


def repair_json(raw_text: str) -> str:
    """
    Repairs broken or truncated LLM JSON and returns a valid JSON string.
    """
    if not raw_text or not raw_text.strip():
        return "{}"

    # Step 1: Strip markdown code blocks
    cleaned = strip_markdown_blocks(raw_text)

    # Step 2: Try fast path
    try:
        json.loads(cleaned)
        return cleaned
    except Exception:
        pass

    # Step 3: Strip comments & fix literals
    cleaned = strip_comments(cleaned)
    cleaned = fix_python_literals(cleaned)
    cleaned = fix_single_quotes(cleaned)
    cleaned = remove_trailing_commas(cleaned)

    try:
        json.loads(cleaned)
        return cleaned
    except Exception:
        pass

    # Step 4: Handle truncation (missing closing brackets/braces)
    cleaned = close_truncated_json(cleaned)
    cleaned = remove_trailing_commas(cleaned)

    try:
        json.loads(cleaned)
        return cleaned
    except Exception:
        pass

    # Step 5: Fallback: isolate first JSON object or array in text
    obj_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
    if obj_match:
        isolated = obj_match.group(1)
        isolated = close_truncated_json(remove_trailing_commas(isolated))
        try:
            json.loads(isolated)
            return isolated
        except Exception:
            pass

    return cleaned


def repair_json_to_dict(raw_text: str) -> Any:
    """Repairs and parses JSON directly into Python dict or list."""
    fixed_str = repair_json(raw_text)
    return json.loads(fixed_str)
