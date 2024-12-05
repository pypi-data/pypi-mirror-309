from article_summary import get_context_and_feedback_from_ai
from get_cited_by import get_cited_by
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))


def get_Section_B_output(pdf_name, article_name, translation = "English"):
    # 因为需要把两个模块的输出合并，故另写一个函数来完成
    output_dict_1 = get_context_and_feedback_from_ai(pdf_name, article_name, translation)
    output_dict_2 = get_cited_by(article_name)

    Section_B_output = {
        "summaries": output_dict_1.get("summaries", {}),
        "related_work": output_dict_1.get("related_work", {}),
        "logical_chain": output_dict_1.get("logical_chain", {}),
        "cited_by": output_dict_2
    }

    return Section_B_output