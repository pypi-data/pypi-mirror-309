import requests
import json
class LLMOutputParser:
    def __init__(self, host='47.88.6.140', port='3009', endpoint='structured_output'):
        self.base_url = f"http://{host}:{port}/{endpoint}"

    def parse(self, model,content, output_format):
        try:
            data ={'model':model,'question': content, 'response_schemas': output_format}
            response = requests.post(self.base_url, json=data) # 使用json参数
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}")
            return None

# client = LLMOutputParser()
# model='openai'
# output_format=[{"name": "name", "description": "name of people", "type": "str"}, {"name": "age", "description": "age of person", "type": "int"}, {"name": "stories","description": "all stories in the life, list of story details","type": "list"}]
# content = "李白简介"

# response_data = client.parse(model,content, output_format)

# if response_data:
#     print("服务端返回数据:")
#     print(json.dumps(response_data, indent=4,ensure_ascii=False))
# else:
#     print("请求失败或解析错误")