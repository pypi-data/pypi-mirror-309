from arxiv_api_integration import arxiv_api_calling
from GoogleScholar_spider import GoogleScholar_Author
from arxiv_api_integration_ai_connect import answer
from arxiv_api_integration_subpaper import answer_sub
import time
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))



def summary(article_title):

    # 调用arxiv函数, 获取文章信息
    # article_title = "Noncommutative Poisson structure and invariants of matrices"
    translation = "English"
    article = arxiv_api_calling(article_title, translation)

    # 调用GoogleScholar函数, 获取第一作者信息
    first_author_info = GoogleScholar_Author(article['authors'][0])
    # 若调取多个作者，则会报错StopIteration，暂时无法修复，所以只能调取第一作者信息
    # def process_authors(author_list):
    #     results = []
    #     for author in author_list:
    #         author_info = GoogleScholar_Author(author)
    #         results.append(author_info)
    #     return results

    # article = {
    #     "id": "http://arxiv.org/abs/2402.06909v2",
    #     "published": "2024-02-10",
    #     "updated": "2024-02-13",
    #     "title": "Noncommutative Poisson structure and invariants of matrices",
    #     "summary": (
    #         "We introduce a novel approach that employs techniques from noncommutative "
    #         "Poisson geometry to comprehend the algebra of invariants of two $n\\times n$ "
    #         "matrices. We entirely solve the open problem of computing the algebra of "
    #         "invariants of two $4 \\times 4$ matrices. As an application, we derive the "
    #         "complete description of the invariant commuting variety of $4 \\times 4$ "
    #         "matrices and the fourth Calogero-Moser space."
    #     ),
    #     "authors": ['Farkhod Eshmatov', 'Xabier García-Martínez', 'Rustam Turdibaev'],
    #     "pdf link": "http://arxiv.org/pdf/2402.06909v2",
    #     "summarized summary": (
    #         "The paper presents a novel approach using noncommutative Poisson geometry to study "
    #         "the algebra of invariants of two \\( n \\times n \\) matrices. The authors resolve "
    #         "the open problem of computing the algebra of invariants for two \\( 4 \\times 4 \\) "
    #         "matrices. As an application, they provide a full description of both the invariant "
    #         "commuting variety for \\( 4 \\times 4 \\) matrices and the fourth Calogero-Moser space."
    #     )
    # }

    # 构建输出字符串
    output = (
        f"ID: {article['id']}\n"
        f"Published: {article['published']}\n"
        f"Updated: {article['updated']}\n"
        f"Title: {article['title']}\n"
        f"Summary: {article['summary']}\n"
        f"Authors: {article['authors']}\n"
        f"First Author Info: {first_author_info}\n"
        f"PDF Link: {article.get('pdf_link', 'N/A')}\n"
    )


    ai_answer = answer(output, translation)
    # 打印输出字符串

    ai_substitute_paper = answer_sub(output, translation)

    # print(ai_substitute_paper)

    sep_ai_substitute_paper = ai_substitute_paper.split('\n')
    print(sep_ai_substitute_paper)
    paper1, paper2, paper3 = sep_ai_substitute_paper
    




    output_update = {
        "ID": article['id'],
        "Published": article['published'],
        "Updated": article['updated'],
        "Title": article['title'],
        "Summary": article['summary'],
        "Authors": article['authors'],
        "First Author Info": first_author_info,
        "PDF Link": article.get('pdf_link', 'N/A'),
        "Evaluation from AI": ai_answer,
        "Substitute paper names": [paper1, paper2, paper3]
    }



    return output_update

    # def(article):




