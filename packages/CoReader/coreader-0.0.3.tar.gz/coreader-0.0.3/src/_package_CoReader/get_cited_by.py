from serpapi import GoogleSearch
# 从settings.py中导入全局变量
from settings import serpapi_key, engine
import requests
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))


def get_cited_by(article_title):
    # 从谷歌学术官方提供的api中获取信息
    params = {
        "api_key": serpapi_key,
        "engine": engine,
        "q": article_title
    }
   
    search = GoogleSearch(params)
    results = search.get_dict()

    if 'organic_results' not in results or \
       len(results['organic_results']) <= 0 or \
       'inline_links' not in results['organic_results'][0] or \
       'cited_by' not in results['organic_results'][0]['inline_links']:
        # 如果相关信息不存在
        output_dict = {
            "Status": "Error",
            "Error_info": "Sorry, there is no articles citing this paper in Google Scholar."
        }
        return output_dict

    cited_by_url = results['organic_results'][0]["inline_links"]["cited_by"]["serpapi_scholar_link"]
    cited_by_num = results['organic_results'][0]["inline_links"]["cited_by"]["total"]
    #print(cited_by_url)

    response = requests.get(cited_by_url,  params={"api_key": serpapi_key})

    #print("/*------------------------------------------------------*/")
    #print(response)
    #print("/*------------------------------------------------------*/")

    if response.status_code == 200:
        cited_by_articles_dict = response.json()
        # list↓
        cited_by_articles = cited_by_articles_dict["organic_results"]
        output_dict = {}
        output_dict["Status"] = "OK"
        output_dict["cited_by_num"] = cited_by_num
        output_dict["cited_by_details"] = {}
        for i in range(len(cited_by_articles)):
            cited_by_article_dict = {}
            # 只需要title, snippet
            cited_by_article_dict["title"] = cited_by_articles[i]["title"]
            # cited_by_article_dict["link"] = cited_by_articles[i]["link"]
            cited_by_article_dict["snippet"] = cited_by_articles[i]["snippet"]
            # cited_by_article_dict["authors"] = cited_by_articles[i]["publication_info"]["authors"]
            # cited_by_article_dict["resources"] = cited_by_articles[i]["resources"]
            output_dict["cited_by_details"][f"cited_by_{i}"] = cited_by_article_dict

            if i >= 2:
                break

        #print(output_dict)
        #print("/*------------------------------------------------------*/")

        return output_dict
    
    # 若请求不成功：
    else:
        output_dict = {
            "Status": "Error",
            "Error_info": f"Your request is not successful. The status code is {response.status_code}. Please contact the authors of this web application."
        }
        return output_dict
    