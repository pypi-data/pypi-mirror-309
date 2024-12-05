import pandas as pd
import sys
import os
from io import BytesIO
from get_output import get_Section_B_output
from Summary import summary


# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_4White9264CoReader')))


def get_article_details(title):
    # 为了测试目的，我们直接使用提供的数据

    # 在你的代码调通直接别解开这个，会耗费我的AI配额，不解开用的就是input.py里的数据
    Section_D_output = summary(title)
    Section_B_output = get_Section_B_output(title, title, "English")

    first_author_info_latest_three_pub = Section_D_output.get('First Author Info', {}).get('latest_three_publications', [])
    formated1 = f"\n{first_author_info_latest_three_pub[0][0]}, {first_author_info_latest_three_pub[0][1]}"
    formated2 = f"{first_author_info_latest_three_pub[1][0]}, {first_author_info_latest_three_pub[1][1]}"
    formated3 = f"{first_author_info_latest_three_pub[2][0]}, {first_author_info_latest_three_pub[2][1]}"
   

    article = {
        
       'cited_by_articles': Section_B_output.get('cited_by', {}),  # 从 Section_B_output 获取前三篇引用的文章信息
        'related_work': Section_B_output.get('related_work', {}),  # 从 Section_A_output 获取相关工作
        'logical_chain': Section_B_output.get('logical_chain', 'N/A'),  # 从 Section_B_output 获取逻辑链
        'Summaries': Section_B_output.get('summaries', {}),  # 从 Section_B_output 获取各章节总结
   
        'title': Section_D_output.get('Title', 'N/A'),  # 从 Section_D_output 获取标题
        'author_name': ', '.join(Section_D_output.get('Authors', [])),  # 从 Section_D_output 获取作者姓名
        'summary': Section_D_output.get('Summary', 'N/A'),  # 从 Section_D_output 获取摘要
        'pdf_link': Section_D_output.get('PDF Link', 'N/A'),  # 从 Section_D_output 获取 PDF 链接
        'published': Section_D_output.get('Published', 'N/A'),  # 从 Section_D_output 获取发表日期
        'updated': Section_D_output.get('Updated', 'N/A'),  # 从 Section_D_output 获取更新日期
        'author_info': Section_D_output.get('First Author Info', {}),  # 从 Section_D_output 获取第一作者信息
        "first_author_info_name":(Section_D_output.get('Authors', []))[0],  # 从 Section_D_output 获取第一作者姓名
        'first_author_info_affiliation': Section_D_output.get('First Author Info', {}).get('affiliation', 'N/A'),  # 从 Section_D_output 获取第一作者机构
        'first_author_info_scholar_id': Section_D_output.get('First Author Info', {}).get('scholar_id', 'N/A'),  # 从 Section_D_output 获取第一作者 Google Scholar ID
        'first_author_info_citation': Section_D_output.get('First Author Info', {}).get('citation', 'N/A'),  # 从 Section_D_output 获取第一作者引用次数
        "first_author_info_num_publications": Section_D_output.get('First Author Info', {}).get('num_publications', 'N/A'),  # 从 Section_D_output 获取第一作者发表文章数
        'first_author_info_hindex': Section_D_output.get('First Author Info', {}).get('hindex', 'N/A'),  # 从 Section_D_output 获取第一作者 h-index
        'first_author_info_hindex5y': Section_D_output.get('First Author Info', {}).get('hindex5y', 'N/A'),  # 从 Section_D_output 获取第一作者 5 年 h-index
        'first_author_info_i10index': Section_D_output.get('First Author Info', {}).get('i10index', 'N/A'),  # 从 Section_D_output 获取第一作者 i10-index
        'first_author_info_i10index5y': Section_D_output.get('First Author Info', {}).get('i10index5y', 'N/A'),  # 从 Section_D_output 获取第一作者 5 年 i10-index

       'first_author_info_latest_three1': formated1,
        'first_author_info_latest_three2': formated2,
        'first_author_info_latest_three3': formated3,

        "evaluation_from_ai": Section_D_output.get('Evaluation from AI', 'N/A'),  # 从 Section_D_output 获取 AI 评价

        "substitute_paper1_names": Section_D_output.get('Substitute paper names', 'N/A')[0],  # 从 Section_D_output 获取替代论文名称
        "substitute_paper2_names": Section_D_output.get('Substitute paper names', 'N/A')[1],  # 从 Section_D_output 获取替代论文名称
        "substitute_paper3_names": Section_D_output.get('Substitute paper names', 'N/A')[2],  # 从 Section_D_output 获取替代论文名称


    }

    return article

# __init__.py
def my_function():
    return "Hello from _package_4White9264CoReader!"

# article = get_article_details("Self-Modeling Based Diagnosis of Software-Defined Networks")
# print(article)

