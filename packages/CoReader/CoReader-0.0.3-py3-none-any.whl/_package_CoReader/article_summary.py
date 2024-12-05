# Author: Zehao ZHANG 24069596g

from arxiv_api_integration_ai_connect_sub import answer
from pdf_processing import pdf_to_txt
# 从settings.py中导入全局变量
from settings import USER_PROMPT
import json
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))


# 考虑PDF文件名和文章名不一致的情况
# 文件名可从用户上传的文件中读取，文章名由另一section提供
def get_context_and_feedback_from_ai(pdf_name, article_name, translation = "English"):
    pdf_to_txt(pdf_name)
    with open(f"{pdf_name}.txt", "r") as f:
        article_text = f.read()
    user_prompt = USER_PROMPT
    user_prompt = user_prompt.replace("{article_text}", article_text)
    user_prompt = user_prompt.replace("{article_name}", article_name)
    # print(user_prompt)
    
    output_information = answer(user_prompt, translation)
    output_dict = json.loads(output_information)
    # 按照段落标题来分割原文
    # 滑动空间？-未实现
    titles = []
    for key in output_dict['texts'].keys():
        titles.append(key)
    # print(titles)
    # print("/*---------------------------------------------------------------*/")
    for title in titles:
        article_text = article_text.replace(title, "\n\n\n\n\n")
    article_text_list = article_text.split("\n\n\n\n\n")
    # print(article_text_list)
    # print("/*---------------------------------------------------------------*/")
    output_dict['texts'] = dict(zip(titles, article_text_list[1:]))

    return output_dict