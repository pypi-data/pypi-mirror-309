# 谷歌学术接口
serpapi_key = "87e734f6134fcb72e3c2f4f9f3e0a2aa9435e0903ce9a205d8d7e9024abb05a0"
engine = "google_scholar"

# AI接口调用
OPENROUTER_API_KEY = "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"
MODEL = "openai/gpt-4o-mini-2024-07-18"
AI_URL = "https://openrouter.ai/api/v1/chat/completions"
SYSTEM_PROMPT = """
You are an academic assistant, please help me to analyse some articles in {translation}.
"""
USER_PROMPT = """
The article is:
"{article_text}"

What you need to do is analyzing the article, and output the following Information:
1. Chapters' title: Get each chapter's title of this article;
2. Chapters' original text : Get each chapter's original text of this article;
3. Chapters' summaries: Get each chapter's summary of this article;
4. Related work: The summary of this article's related work;
5. Logic Chain: Explain the argumentation process of this article in one paragraph.

Output in JSON format without ```json.
Example:
{ 
    "texts": {
        "chapter1's title": "chapter1's original text",
        "chapter2's title": "chapter2's original text",
        ......
    },
    "summaries":{
        "chapter1's title": "chapter1's summary",
        "chapter2's title": "chapter1's summary",
        ......
    },
    "related_work":{
        "{article_name}": "The summary of this article's related work."
    },
    "logical_chain": "The overall logic of this article."
}
"""