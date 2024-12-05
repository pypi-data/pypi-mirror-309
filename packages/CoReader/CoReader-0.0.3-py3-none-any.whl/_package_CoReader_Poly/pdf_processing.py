import fitz  # PyMuPDF
import pymupdf
import sys
import os
# 将src目录添加到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/_package_CoReader')))


# 提取 PDF 文本转化为txt
def pdf_to_txt(pdf_name): 
    if not os.path.exists(f"image/{pdf_name}"):
        os.makedirs(f"image/{pdf_name}")
    # 打开 PDF 文件
    pdf_document = pymupdf.open(f'{pdf_name}.pdf')
    pdf_txt = ''
    for i in range(len(pdf_document)):
        page = pdf_document.load_page(i)
        text = extract_text_and_images(page, i, pdf_name)
        pdf_txt += text + '\n'
        
    # 过滤或处理文本
    # 去除空行
    pdf_list = pdf_txt.split('\n')
    pdf_list = [x for x in pdf_list if x != '' and x != ' ']
    pdf_txt = '\n'.join(pdf_list)

    with open(f"{pdf_name}.txt", 'w', encoding='utf-8') as txt_file:
        txt_file.write(pdf_txt)
    print(f"PDF内容已保存到 {pdf_name}.txt")
    
# 提取一页
def extract_text_and_images(page, page_num, pdf_name):
    text_blocks = page.get_text("blocks")
    text = ""
    for i, block in enumerate(text_blocks):
        if i > 0:
            rect = pymupdf.Rect(text_blocks[i-1][:4])
            # 处理文本块
            text += block[4]
    return text

def is_valid_rect(rect):
    """检查矩形坐标是否有效"""
    return rect.x0 < rect.x1 and rect.y0 < rect.y1