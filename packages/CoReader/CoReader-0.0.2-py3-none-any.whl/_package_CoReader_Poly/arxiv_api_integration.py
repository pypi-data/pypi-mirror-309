

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from arxiv_api_integration_ai_connect import answer
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader_Poly')))


def pdf_download(pdf_link, article_title):
    # 根据返回的PDF下载连接，下载 PDF 文件
    pdf_filename = article_title + ".pdf"
    urllib.request.urlretrieve(pdf_link, pdf_filename)
    
    

def arxiv_api_calling(article_title, translation):
    # 定义参数

    method_name = "query"
    start = 0
    max_results = 29

    # 对参数进行编码
    encoded_article_title = urllib.parse.quote(article_title)

    # 构建有效的 URL
    url = f"http://export.arxiv.org/api/{method_name}?search_query={encoded_article_title}&start={start}&max_results={max_results}"

    # 获取数据
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')

    # print(data)

    # 解析 XML 数据
    root = ET.fromstring(data)

    # print(root)

    # 提取文章信息
    article = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        # print(ET.tostring(entry, encoding='utf-8').decode('utf-8'))

        

        if entry.find('{http://www.w3.org/2005/Atom}title').text == article_title:

            # # Print the XML data，调试
            # print(ET.tostring(entry, encoding='utf-8').decode('utf-8'))

            article['id'] = entry.find('{http://www.w3.org/2005/Atom}id').text

            updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
            article['updated'] = updated[:10] # 只保留日期部分

            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            article['published'] = published[:10] 

            article['title'] = entry.find('{http://www.w3.org/2005/Atom}title').text
            article['summary'] = entry.find('{http://www.w3.org/2005/Atom}summary').text
            
            authors = entry.findall('{http://www.w3.org/2005/Atom}author')
            article['authors'] = [author.find('{http://www.w3.org/2005/Atom}name').text for author in authors]
            
            pdf_link = entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]')

            # print(pdf_link)
            if pdf_link is not None:
                article['pdf_link'] = pdf_link.attrib['href']
            
    # summarized_article = answer(article['summary'], translation)
    # article['summarized summary'] = summarized_article

    # 调用函数，下载 PDF 文件
    try:
        pdf_download(article.get('pdf_link'),article['title'])
        print(f"PDF downloaded successfully as {article['title']}.pdf .")
    except Exception as e:
        raise Exception(f"Download Fail: {e}")


    return article




# # 调用函数
# article_title = "Derived Poisson structures on almost commutative algebras and applications"
# translation = "English"
# article = arxiv_api_calling(article_title, translation).get('pdf_link')
# print(article)
