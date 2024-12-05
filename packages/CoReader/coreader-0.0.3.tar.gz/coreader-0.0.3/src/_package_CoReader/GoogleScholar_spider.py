from scholarly import scholarly
import json
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))



def GoogleScholar_Author(name):

    search_query = scholarly.search_author(name)
    # 获取第一个搜索结果
    result = next(search_query)



    author = scholarly.fill(result)
    publication = [pub['bib']['title'] for pub in author['publications']]

    # 将结果转换为字典
    result_dict = dict(result)

    # 提取 affiliation 和 scholar_id
    affiliation = result_dict.get('affiliation', 'N/A')
    scholar_id = result_dict.get('scholar_id', 'N/A')
    citation = result_dict.get('citedby', 'N/A')

    # print(f"Affiliation: {affiliation}")
    # print(f"Scholar ID: {scholar_id}")
    # print(f"Citation: {citation}")
    # print(f"Number of Publication: {len(publication)}")

    # 填充详细信息
    filled_result = scholarly.fill(result, sections=['counts', 'indices'])

    # 将结果转换为字典
    filled_result_dict = dict(filled_result)

    # 提取 hindex, hindex5y, i10index 和 i10index5y
    hindex = filled_result_dict.get('hindex', 'N/A')
    hindex5y = filled_result_dict.get('hindex5y', 'N/A')
    i10index = filled_result_dict.get('i10index', 'N/A')
    i10index5y = filled_result_dict.get('i10index5y', 'N/A')

    # print(f"hindex: {hindex}")
    # print(f"hindex5y: {hindex5y}")
    # print(f"i10index: {i10index}")
    # print(f"i10index5y: {i10index5y}")


    # 提取最新的三篇文章的标题及其发表日期
    publications = author.get('publications', [])
    
    if not publications:
        latest_three = "None publications found."
    if len(publications) < 3:
        latest_three = sorted(publications, key=lambda x: int(x.get('bib', {}).get('pub_year', 0)), reverse=True)
    else:
        sorted_publications = sorted(publications, key=lambda x: int(x.get('bib', {}).get('pub_year', 0)), reverse=True)
        latest_three = [(pub.get('bib', {}).get('title', 'N/A'), pub.get('bib', {}).get('pub_year', 'N/A')) for pub in sorted_publications[:3]]

    # print(f"Latest Three Titles: {latest_three}")

    author_info = {
        'affiliation': affiliation,
        'scholar_id': scholar_id,
        'citation': citation,
        'num_publications': len(publication),
        'hindex': hindex,
        'hindex5y': hindex5y,
        'i10index': i10index,
        'i10index5y': i10index5y,
        'latest_three_publications': latest_three
    }


    return author_info


# 测试
# author_info = GoogleScholar_Author('Farkhod Eshmatov')
# print(json.dumps(author_info, indent=2))