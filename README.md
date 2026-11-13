# 🩹 json-heal (`jheal`)

> **Blazing-fast (<1ms), zero-dependency JSON healer for LLM outputs. Fixes truncated JSON, missing brackets, trailing commas, single quotes, and Python literals.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](pyproject.toml)
[![Zero Dependency](https://img.shields.io/badge/core-zero--dependency-orange.svg)](#)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow.svg?logo=buy-me-a-coffee)](https://buymeacoffee.com/carlosdevkadu)

LLMs (GPT-4o, Claude 3.5, Gemini, DeepSeek) frequently return malformed, cut-off, or non-standard JSON that crashes `json.loads()` in production AI agents.

**`json-heal`** repairs broken LLM JSON in sub-milliseconds without calling external APIs or requiring heavy dependencies.

---

## 💖 Support & Sponsor

If **json-heal** saved your AI production pipeline from crashing, consider buying me a coffee:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow.svg?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/carlosdevkadu)

👉 [buymeacoffee.com/carlosdevkadu](https://buymeacoffee.com/carlosdevkadu)

---

## ⚡ What it Fixes

* ✂️ **Token Truncation**: Automatically closes unclosed strings `"`, arrays `]`, and objects `}` when cut off mid-sentence by max token limits.
* 📦 **Markdown Code Fences**: Strips ````json ... ```` and ```` ... ```` blocks automatically.
* 🐍 **Python Literals**: Fixes `True` -> `true`, `False` -> `false`, and `None` -> `null`.
* 콤 **Trailing Commas**: Cleans up illegal trailing commas (e.g. `{"a": 1,}`).
* 💬 **Comments**: Removes single-line `//` and multi-line `/* */` comments.
* 🔤 **Single Quotes**: Converts `'key': 'val'` into valid `"key": "val"`.

---

## 🚀 Quick Start

### Installation

```bash
pip install .
```

### Python SDK

```python
from json_heal import repair_json, repair_json_to_dict

# Example 1: Truncated JSON from an LLM cutoff
raw_output = '{"status": "success", "results": [{"id": 1, "name": "Item'
fixed_json = repair_json(raw_output)
# Result: '{"status": "success", "results": [{"id": 1, "name": "Item"}]}'

# Example 2: Directly parse into Python dictionary
data = repair_json_to_dict("{'active': True, 'count': 42,}")
print(data["active"])  # True
```

### CLI Usage

```bash
# Heal broken JSON string
jheal "{'key': 'value',}"

# Heal broken JSON file and pretty print
jheal -f raw_llm_response.txt -p
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
