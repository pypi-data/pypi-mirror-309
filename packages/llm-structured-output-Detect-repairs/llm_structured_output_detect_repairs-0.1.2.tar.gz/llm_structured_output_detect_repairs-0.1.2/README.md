# llm_structured_output_Detect_repairs

A simple HTTP client library for interacting with a structured output API.

## 安装

```bash
pip install llm_structured_output_Detect_repairs

以下是一个完整的示例代码，展示了如何使用 llm_structured_output_Detect_repairs 发送请求并解析响应：



import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_structured_output_Detect_repairs.llm_output_parser import LLMOutputParser
import json

# 创建 LLMOutputParser 实例
client = LLMOutputParser()
model = 'openai'
output_format = [
    {"name": "name", "description": "name of people", "type": "str"},
    {"name": "age", "description": "age of person", "type": "int"},
    {"name": "stories", "description": "all stories in the life, list of story details", "type": "list"}
]
content = "李白简介"
response_data = client.parse(model, content, output_format)

if response_data:
    print("服务端返回数据:")
    print(json.dumps(response_data, indent=4, ensure_ascii=False))
else:
    print("请求失败或解析错误")