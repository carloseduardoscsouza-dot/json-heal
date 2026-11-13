"""
json-heal - Blazing-fast, zero-dependency JSON healer for LLM outputs.
Fixes truncated JSON, missing brackets, trailing commas, single quotes, and Python literals.
"""

__version__ = "1.0.0"
__author__ = "Carlos"

from .healer import repair_json, repair_json_to_dict

__all__ = [
    "repair_json",
    "repair_json_to_dict",
]
