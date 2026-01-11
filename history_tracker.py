'''
历史数据跟踪模块 - 用于跨天去重
'''
import json
import os
from datetime import datetime, timedelta

HISTORY_FILE = "/home/ubuntu/tech_info_crawler/crawled_history.json"

def load_history():
    """加载历史爬取记录"""
    if not os.path.exists(HISTORY_FILE):
        return {
            'last_updated': None,
            'content_hashes': []
        }
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载历史记录失败: {e}")
        return {
            'last_updated': None,
            'content_hashes': []
        }

def save_history(history):
    """保存历史爬取记录"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        print(f"历史记录已保存到: {HISTORY_FILE}")
    except Exception as e:
        print(f"保存历史记录失败: {e}")

def update_history(content_hashes):
    """更新历史记录"""
    history = {
        'last_updated': datetime.now().isoformat(),
        'content_hashes': content_hashes
    }
    save_history(history)
    return history

def filter_new_articles(articles):
    """
    过滤出新文章(未在历史记录中的)
    
    Args:
        articles: 文章列表,每篇文章需包含 content_hash 字段
    
    Returns:
        tuple: (新文章列表, 过滤掉的数量)
    """
    history = load_history()
    historical_hashes = set(history.get('content_hashes', []))
    
    print(f"\n历史记录中有 {len(historical_hashes)} 篇文章")
    
    # 过滤新文章
    new_articles = []
    filtered_count = 0
    
    for article in articles:
        content_hash = article.get('content_hash')
        if content_hash and content_hash in historical_hashes:
            filtered_count += 1
        else:
            new_articles.append(article)
    
    print(f"本次爬取: {len(articles)} 篇")
    print(f"过滤重复: {filtered_count} 篇")
    print(f"新增文章: {len(new_articles)} 篇")
    
    return new_articles, filtered_count

def clean_old_history(days=7):
    """
    清理过期的历史记录(可选功能)
    
    Args:
        days: 保留最近几天的记录
    """
    history = load_history()
    last_updated = history.get('last_updated')
    
    if not last_updated:
        return
    
    try:
        last_date = datetime.fromisoformat(last_updated)
        if datetime.now() - last_date > timedelta(days=days):
            print(f"历史记录已超过 {days} 天,清空记录")
            update_history([])
    except Exception as e:
        print(f"清理历史记录失败: {e}")

if __name__ == "__main__":
    # 测试历史跟踪功能
    print("=== 测试历史跟踪模块 ===\n")
    
    # 模拟第一次爬取
    print("第一次爬取:")
    articles_day1 = [
        {'title': 'Article 1', 'content_hash': 'hash1'},
        {'title': 'Article 2', 'content_hash': 'hash2'},
        {'title': 'Article 3', 'content_hash': 'hash3'}
    ]
    
    new_articles, filtered = filter_new_articles(articles_day1)
    print(f"结果: {len(new_articles)} 篇新文章\n")
    
    # 更新历史
    hashes = [a['content_hash'] for a in articles_day1]
    update_history(hashes)
    
    # 模拟第二次爬取(有重复)
    print("\n第二次爬取(包含重复):")
    articles_day2 = [
        {'title': 'Article 2', 'content_hash': 'hash2'},  # 重复
        {'title': 'Article 3', 'content_hash': 'hash3'},  # 重复
        {'title': 'Article 4', 'content_hash': 'hash4'},  # 新文章
        {'title': 'Article 5', 'content_hash': 'hash5'}   # 新文章
    ]
    
    new_articles, filtered = filter_new_articles(articles_day2)
    print(f"结果: {len(new_articles)} 篇新文章, {filtered} 篇重复\n")
    
    # 更新历史(累加新文章的hash)
    all_hashes = hashes + [a['content_hash'] for a in new_articles]
    update_history(all_hashes)
    
    print("测试完成!")
