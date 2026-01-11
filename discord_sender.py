'''
Discord推送模块 - 通过Webhook发送每日科技资讯
'''
import json
import urllib.request
import urllib.parse
import ssl
import time
from datetime import datetime

# Discord Webhook URL - 请在环境变量或配置文件中设置
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"

def load_latest_processed_data():
    """加载最新的处理后数据"""
    import glob
    json_files = glob.glob("/home/ubuntu/tech_info_crawler/processed_data_*.json")
    if not json_files:
        print("未找到处理后的数据文件")
        return None
    
    latest_file = sorted(json_files)[-1]
    print(f"正在加载: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def send_discord_message(webhook_url, content=None, embeds=None):
    """
    发送Discord消息
    
    Args:
        webhook_url: Discord Webhook URL
        content: 纯文本消息内容
        embeds: Embed格式的富文本消息列表
    
    Returns:
        bool: 是否发送成功
    """
    payload = {}
    
    if content:
        payload['content'] = content
    
    if embeds:
        payload['embeds'] = embeds
    
    try:
        # 准备请求
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # 发送请求(禁用SSL验证)
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            if response.status == 204 or response.status == 200:
                return True
            else:
                print(f"发送失败: {response.status}")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # 触发速率限制,等待后重试
            try:
                error_data = json.loads(e.read().decode('utf-8'))
                retry_after = error_data.get('retry_after', 1)
                print(f"触发速率限制,等待 {retry_after} 秒后重试...")
                time.sleep(retry_after)
                return send_discord_message(webhook_url, content, embeds)
            except:
                time.sleep(1)
                return send_discord_message(webhook_url, content, embeds)
        else:
            print(f"HTTP错误: {e.code} - {e.reason}")
            return False
    except Exception as e:
        print(f"发送出错: {e}")
        return False

def create_summary_message(data):
    """创建概览消息"""
    # 统计数据
    total = len(data)
    
    category_counts = {}
    for entry in data:
        for category in entry.get('categories', ['General']):
            category_counts[category] = category_counts.get(category, 0) + 1
    
    # 构建消息
    message = f"📊 **今日科技资讯** - {datetime.now().strftime('%Y年%m月%d日')}\n\n"
    message += f"✅ 共爬取 **{total}** 篇新文章\n"
    
    # 分类统计
    category_emojis = {
        'AI': '🤖',
        'Biotech': '🧬',
        'Startup': '🚀',
        'VC': '💰',
        'General': '📰'
    }
    
    category_parts = []
    for category in ['AI', 'Biotech', 'Startup', 'VC']:
        count = category_counts.get(category, 0)
        if count > 0:
            emoji = category_emojis.get(category, '📌')
            category_parts.append(f"{emoji} {category}: {count}篇")
    
    if category_parts:
        message += " | ".join(category_parts) + "\n"
    
    message += f"\n📌 **精选TOP 10文章如下** ↓"
    
    return message

def create_article_embed(article, index):
    """
    创建单篇文章的Embed消息
    
    Args:
        article: 文章数据
        index: 文章序号
    
    Returns:
        dict: Discord Embed对象
    """
    # 获取分类和对应的emoji
    categories = article.get('categories', ['General'])
    category_emojis = {
        'AI': '🤖',
        'Biotech': '🧬',
        'Startup': '🚀',
        'VC': '💰',
        'General': '📰'
    }
    
    primary_category = categories[0] if categories else 'General'
    emoji = category_emojis.get(primary_category, '📌')
    
    # 获取标题(优先中文)
    title = article.get('chinese_title', article.get('title', 'N/A'))
    # 限制标题长度(Discord Embed标题最多256字符)
    if len(title) > 200:
        title = title[:197] + "..."
    
    # 获取摘要(优先中文)
    summary = article.get('chinese_summary', article.get('summary', 'N/A'))
    # 限制摘要长度(Discord Embed描述最多4096字符,但我们限制在300字符内)
    if len(summary) > 300:
        summary = summary[:297] + "..."
    
    # 质量评分转星级
    score = article.get('quality_score', 0)
    if score >= 24:
        stars = "⭐⭐⭐⭐⭐"
    elif score >= 20:
        stars = "⭐⭐⭐⭐"
    elif score >= 15:
        stars = "⭐⭐⭐"
    elif score >= 10:
        stars = "⭐⭐"
    else:
        stars = "⭐"
    
    # 颜色映射(十六进制)
    category_colors = {
        'AI': 0x5865F2,      # Discord蓝
        'Biotech': 0x57F287, # 绿色
        'Startup': 0xFEE75C, # 黄色
        'VC': 0xEB459E,      # 粉色
        'General': 0x99AAB5  # 灰色
    }
    
    color = category_colors.get(primary_category, 0x99AAB5)
    
    # 构建Embed
    embed = {
        "title": f"{emoji} {primary_category} #{index} - {title}",
        "description": summary,
        "color": color,
        "fields": [
            {
                "name": "📰 来源",
                "value": article.get('source', 'N/A'),
                "inline": True
            },
            {
                "name": "⭐ 评分",
                "value": f"{stars} ({score}分)",
                "inline": True
            }
        ],
        "url": article.get('link', ''),
        "footer": {
            "text": f"原标题: {article.get('title', 'N/A')[:100]}"
        }
    }
    
    return embed

def send_daily_report_to_discord(webhook_url, top_n=10):
    """
    发送每日报告到Discord
    
    Args:
        webhook_url: Discord Webhook URL
        top_n: 发送前N篇文章(默认10篇)
    
    Returns:
        bool: 是否发送成功
    """
    print("\n" + "=" * 60)
    print("开始向Discord推送每日科技资讯")
    print("=" * 60)
    
    # 加载数据
    data = load_latest_processed_data()
    if not data:
        print("❌ 没有可用的数据,无法推送")
        return False
    
    if len(data) == 0:
        print("❌ 数据为空,无法推送")
        return False
    
    # 1. 发送概览消息
    print("\n📤 发送概览消息...")
    summary = create_summary_message(data)
    success = send_discord_message(webhook_url, content=summary)
    
    if not success:
        print("❌ 概览消息发送失败")
        return False
    
    print("✅ 概览消息发送成功")
    time.sleep(1)  # 避免触发速率限制
    
    # 2. 发送TOP N文章
    articles_to_send = data[:top_n]
    print(f"\n📤 发送TOP {len(articles_to_send)} 篇文章...")
    
    for i, article in enumerate(articles_to_send, 1):
        embed = create_article_embed(article, i)
        success = send_discord_message(webhook_url, embeds=[embed])
        
        if success:
            print(f"  ✅ 文章 {i}/{len(articles_to_send)} 发送成功")
        else:
            print(f"  ❌ 文章 {i}/{len(articles_to_send)} 发送失败")
        
        # 避免触发Discord速率限制(每个webhook每秒最多5条消息)
        if i < len(articles_to_send):
            time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"✅ Discord推送完成!共发送 {len(articles_to_send) + 1} 条消息")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    # 测试Discord推送
    import sys
    
    # 从命令行参数或默认值获取webhook URL
    webhook_url = sys.argv[1] if len(sys.argv) > 1 else DISCORD_WEBHOOK_URL
    
    if webhook_url == "YOUR_WEBHOOK_URL_HERE":
        print("❌ 请设置Discord Webhook URL")
        print("使用方法: python3 discord_sender.py <webhook_url>")
        sys.exit(1)
    
    # 发送测试消息
    send_daily_report_to_discord(webhook_url, top_n=10)
