'''
AI处理模块 - 支持OpenAI和Google Gemini
'''
import os
import json

def get_ai_client():
    """
    根据环境变量选择AI服务提供商
    
    优先级:
    1. GEMINI_API_KEY -> 使用Google Gemini
    2. OPENAI_API_KEY -> 使用OpenAI
    3. 都没有 -> 返回None,跳过AI处理
    """
    gemini_key = os.getenv('GEMINI_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if gemini_key:
        print("🤖 使用 Google Gemini API")
        return 'gemini', gemini_key
    elif openai_key:
        print("🤖 使用 OpenAI API")
        from openai import OpenAI
        return 'openai', OpenAI()
    else:
        print("⚠️  未配置AI API密钥,将跳过AI处理")
        return None, None

def translate_and_summarize_with_gemini(api_key, title, summary, link):
    """
    使用Google Gemini进行翻译和总结
    """
    try:
        import google.generativeai as genai
        
        # 配置Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
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
        
        # 调用Gemini
        response = model.generate_content(prompt)
        
        # 解析返回结果
        result_text = response.text.strip()
        
        # 尝试提取JSON(Gemini可能会返回带markdown的JSON)
        if '```json' in result_text:
            result_text = result_text.split('```json')[1].split('```')[0].strip()
        elif '```' in result_text:
            result_text = result_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(result_text)
        
        return {
            'chinese_title': result.get('chinese_title', title),
            'chinese_summary': result.get('chinese_summary', summary[:200])
        }
        
    except Exception as e:
        print(f"Gemini处理失败: {e}")
        return {
            'chinese_title': title,
            'chinese_summary': summary[:200] + "..."
        }

def translate_and_summarize_with_openai(client, title, summary, link):
    """
    使用OpenAI进行翻译和总结
    """
    try:
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
        
        # 调用GPT模型
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的科技文章翻译和总结助手,擅长将英文科技资讯转换为简洁易懂的中文内容。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # 解析返回结果
        result = json.loads(response.choices[0].message.content)
        
        return {
            'chinese_title': result.get('chinese_title', title),
            'chinese_summary': result.get('chinese_summary', summary[:200])
        }
        
    except Exception as e:
        print(f"OpenAI处理失败: {e}")
        return {
            'chinese_title': title,
            'chinese_summary': summary[:200] + "..."
        }

def translate_and_summarize(title, summary, link):
    """
    使用AI翻译标题并生成中文摘要
    自动选择可用的AI服务
    
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
    
    # 获取AI客户端
    ai_type, ai_client = get_ai_client()
    
    if ai_type is None:
        # 没有配置AI,返回原始内容
        return {
            'chinese_title': title,
            'chinese_summary': summary[:200] + "..." if len(summary) > 200 else summary
        }
    
    # 根据AI类型调用相应的函数
    if ai_type == 'gemini':
        return translate_and_summarize_with_gemini(ai_client, title, summary, link)
    elif ai_type == 'openai':
        return translate_and_summarize_with_openai(ai_client, title, summary, link)
    else:
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
    # 检查是否配置了AI
    ai_type, _ = get_ai_client()
    
    if ai_type is None:
        print("\n⚠️  未配置AI API密钥,跳过AI处理,使用原始英文内容")
        # 直接添加原始内容作为"中文"字段
        for article in articles:
            article['chinese_title'] = article['title']
            article['chinese_summary'] = article.get('summary', '')[:200] + "..."
        return articles
    
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
