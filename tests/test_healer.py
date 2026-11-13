"""
Unit tests for json-heal.
"""

import json
import unittest
from json_heal.healer import repair_json, repair_json_to_dict


class TestJsonHeal(unittest.TestCase):
    def test_markdown_fence_stripping(self):
        broken = "```json\n{\"status\": \"ok\", \"count\": 42}\n```"
        fixed = repair_json(broken)
        data = json.loads(fixed)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["count"], 42)

    def test_trailing_comma(self):
        broken = '{"items": [1, 2, 3,], "user": {"name": "Alice",},}'
        fixed = repair_json(broken)
        data = json.loads(fixed)
        self.assertEqual(len(data["items"]), 3)
        self.assertEqual(data["user"]["name"], "Alice")

    def test_python_literals(self):
        broken = '{"active": True, "archived": False, "meta": None}'
        fixed = repair_json(broken)
        data = json.loads(fixed)
        self.assertTrue(data["active"])
        self.assertFalse(data["archived"])
        self.assertIsNone(data["meta"])

    def test_single_quotes(self):
        broken = "{'title': 'AI Agent', 'tags': ['ai', 'agent']}"
        fixed = repair_json(broken)
        data = json.loads(fixed)
        self.assertEqual(data["title"], "AI Agent")
        self.assertEqual(data["tags"], ["ai", "agent"])

    def test_truncated_json_closing(self):
        broken = '{"query": "search", "results": [{"id": 1, "text": "sample text'
        fixed = repair_json(broken)
        data = json.loads(fixed)
        self.assertEqual(data["query"], "search")
        self.assertEqual(data["results"][0]["id"], 1)

    def test_repair_to_dict(self):
        broken = "{'score': 99,}"
        d = repair_json_to_dict(broken)
        self.assertEqual(d["score"], 99)


if __name__ == "__main__":
    unittest.main()
