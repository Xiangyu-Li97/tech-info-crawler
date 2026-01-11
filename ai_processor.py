'''
AI处理模块 - 使用LLM进行翻译和总结
'''
import os
from openai import OpenAI

# 初始化OpenAI客户端(使用环境变量中的配置)
client = OpenAI()

def translate_and_summarize(title, summary, link):
    """
    使用AI翻译标题并生成中文摘要
    
    Args:
        title: 原始英文标题
        summary: 原始英文摘要
        link: 文章链接
    
    Returns:
        dict: {
            'chinese_title': 中文标题,
            'chinese_summary': 中文摘要
        }
    """
    
    # 构建提示词
    prompt = f"""请帮我处理以下科技文章信息:

原标题: {title}
原摘要: {summary[:500]}

请完成以下任务:
1. 将标题翻译成简洁的中文(保持专业性和可读性)
2. 基于摘要内容,用2-3句话生成中文总结(150字以内,突出核心信息和价值)

请以JSON格式返回:
{{
    "chinese_title": "中文标题",
    "chinese_summary": "中文摘要"
}}
"""
    
    try:
        # 调用GPT-4模型
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # 使用快速且经济的模型
            messages=[
                {"role": "system", "content": "你是一个专业的科技文章翻译和总结助手,擅长将英文科技资讯转换为简洁易懂的中文内容。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # 解析返回结果
        import json
        result = json.loads(response.choices[0].message.content)
        
        return {
            'chinese_title': result.get('chinese_title', title),
            'chinese_summary': result.get('chinese_summary', summary[:200])
        }
        
    except Exception as e:
        print(f"AI处理失败: {e}")
        # 如果AI处理失败,返回原始内容
        return {
            'chinese_title': title,
            'chinese_summary': summary[:200] + "..."
        }

def batch_process_articles(articles, max_articles=100):
    """
    批量处理文章,添加中文标题和摘要
    
    Args:
        articles: 文章列表
        max_articles: 最大处理数量(避免API调用过多)
    
    Returns:
        处理后的文章列表
    """
    print(f"\n开始AI处理文章(翻译标题和生成中文摘要)...")
    print(f"待处理文章数: {len(articles)}")
    
    processed_articles = []
    
    for i, article in enumerate(articles[:max_articles], 1):
        print(f"处理进度: {i}/{min(len(articles), max_articles)} - {article['title'][:50]}...")
        
        # 调用AI处理
        ai_result = translate_and_summarize(
            article['title'],
            article.get('summary', ''),
            article['link']
        )
        
        # 添加中文字段
        article['chinese_title'] = ai_result['chinese_title']
        article['chinese_summary'] = ai_result['chinese_summary']
        
        processed_articles.append(article)
    
    print(f"✅ AI处理完成,共处理 {len(processed_articles)} 篇文章")
    return processed_articles

if __name__ == "__main__":
    # 测试AI处理
    test_article = {
        'title': 'OpenAI Launches GPT-5 with Revolutionary Capabilities',
        'summary': 'OpenAI has announced the release of GPT-5, featuring unprecedented natural language understanding and generation capabilities. The new model shows significant improvements in reasoning, coding, and multimodal tasks.',
        'link': 'https://example.com/article'
    }
    
    result = translate_and_summarize(
        test_article['title'],
        test_article['summary'],
        test_article['link']
    )
    
    print("\n测试结果:")
    print(f"原标题: {test_article['title']}")
    print(f"中文标题: {result['chinese_title']}")
    print(f"\n原摘要: {test_article['summary']}")
    print(f"中文摘要: {result['chinese_summary']}")
