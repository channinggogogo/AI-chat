# test_api_openai.py — 适用于 OpenAI / DeepSeek（兼容接口）
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
     api_key=os.getenv("DEEPSEEK_API_KEY"),
     base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",  # DeepSeek 用 "deepseek-chat"
    messages=[{"role": "user", "content": "雒雪颖是谁，帮我查一下网上的资料"}]
)

print(response.choices[0].message.content)