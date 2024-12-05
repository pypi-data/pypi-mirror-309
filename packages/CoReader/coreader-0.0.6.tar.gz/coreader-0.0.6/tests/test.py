# test.py
import sys
import os
import json

# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))

# 导入函数
from __init__ import get_article_details

# 使用函数

article = 'Self-Modeling Based Diagnosis of Software-Defined Networks'
article_info = get_article_details(article)
print(json.dumps(article_info, indent=4, ensure_ascii=False))