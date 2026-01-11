'''
主爬虫程序
'''
import feedparser
import json
from datetime import datetime

# 定义要抓取的RSS源
RSS_FEEDS = {
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
}

def fetch_rss_feeds():
    """抓取并解析所有定义的RSS源"""
    print("开始抓取RSS订阅源...")
    all_entries = []
    
    for name, url in RSS_FEEDS.items():
        try:
            print(f"正在抓取: {name} ({url})")
            feed = feedparser.parse(url)
            if feed.bozo:
                print(f"警告: {name} 的RSS源可能格式不正确或无法访问。错误: {feed.bozo_exception}")
                continue
            
            print(f"成功从 {name} 获取 {len(feed.entries)} 篇文章。")
            for entry in feed.entries:
                all_entries.append({
                    "source": name,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "N/A"),
                    "summary": entry.get("summary", "N/A"),
                    "crawled_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"抓取 {name} 时发生错误: {e}")

    return all_entries

def save_to_json(data, filename):
    """将数据保存为JSON文件"""
    print(f"正在将 {len(data)} 条数据保存到 {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("数据保存成功。")

def main():
    """主程序入口"""
    print("--- 开始执行优质科技信息爬取任务 ---")
    rss_entries = fetch_rss_feeds()
    
    if rss_entries:
        print(f"\n--- 抓取完成,共获取 {len(rss_entries)} 篇文章 ---")
        output_filename = f"/home/ubuntu/tech_info_crawler/crawled_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_to_json(rss_entries, output_filename)
    else:
        print("\n--- 本次未抓取到任何文章 ---")

if __name__ == "__main__":
    main()
