# tests/test_http_client.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from llm_structured_output_Detect_repairs.llm_output_parser import LLMOutputParser


class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = LLMOutputParser('localhost', 5000, 'structured_output')

    def test_parse(self):
        model = 'openai'
        content = "李白简介"
        output_format = [
            {"name": "name", "description": "name of people", "type": "str"},
            {"name": "age", "description": "age of person", "type": "int"},
            {"name": "stories", "description": "all stories in the life, list of story details", "type": "list"}
        ]
        response_data = self.client.parse(model, content, output_format)
        self.assertIsNotNone(response_data)
        self.assertIn('name', response_data)
        self.assertIn('age', response_data)
        self.assertIn('stories', response_data)

if __name__ == '__main__':
    unittest.main()