import requests
import json
# 从settings.py中导入全局变量
from settings import OPENROUTER_API_KEY, SYSTEM_PROMPT, MODEL, AI_URL
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))


def answer(article_summary, translation = "English"):

    # 构建对比 prompt
    system_prompt = SYSTEM_PROMPT.replace("{translation}", translation)

    # 构建消息
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User question: {article_summary}"},
    ]

    response = requests.post(
        url = AI_URL,
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        data=json.dumps({ 
            "messages": messages,
            "model": MODEL
        })
    )

    # 打印响应的 JSON 数据以进行调试
    # print("Response JSON:", response.json())
    # print("/*---------------------------------------------------------------*/")
    # 检查响应状态码
    if response.status_code != 200:
        raise Exception(f"API 请求失败，状态码: {response.status_code}, 错误信息: {response.json()}")

    # 解析响应数据
    try:
        resp = response.json()
        if 'choices' in resp and len(resp['choices']) > 0:
            content = resp['choices'][0]['message']['content']
            return content
        else:
            raise KeyError("响应中没有 'choices' 键或 'choices' 为空")
    except KeyError as e:
        raise KeyError(f"解析响应数据时出错: {e}")