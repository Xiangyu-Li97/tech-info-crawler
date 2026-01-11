'''
数据查看器模块
'''
import json
import glob
from datetime import datetime

def load_latest_data():
    """加载最新的处理后数据"""
    json_files = glob.glob("/home/ubuntu/tech_info_crawler/processed_data_*.json")
    if not json_files:
        print("未找到处理后的数据文件")
        return None
    
    latest_file = sorted(json_files)[-1]
    print(f"正在加载: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def show_statistics(data):
    """显示数据统计信息"""
    print("\n" + "=" * 60)
    print("数据统计")
    print("=" * 60)
    print(f"总文章数: {len(data)}")
    
    # 按来源统计
    source_counts = {}
    for entry in data:
        source = entry['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print("\n按来源统计:")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} 篇")
    
    # 按分类统计
    category_counts = {}
    for entry in data:
        for category in entry.get('categories', ['General']):
            category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\n按分类统计:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 篇")
    
    # 质量评分统计
    scores = [entry.get('quality_score', 0) for entry in data]
    avg_score = sum(scores) / len(scores) if scores else 0
    max_score = max(scores) if scores else 0
    min_score = min(scores) if scores else 0
    
    print(f"\n质量评分统计:")
    print(f"  平均分: {avg_score:.2f}")
    print(f"  最高分: {max_score}")
    print(f"  最低分: {min_score}")

def show_top_articles(data, n=10):
    """显示质量评分最高的文章"""
    print("\n" + "=" * 60)
    print(f"质量评分 TOP {n}")
    print("=" * 60)
    
    for i, entry in enumerate(data[:n], 1):
        print(f"\n{i}. {entry['title']}")
        print(f"   来源: {entry['source']}")
        print(f"   分类: {', '.join(entry.get('categories', ['General']))}")
        print(f"   评分: {entry.get('quality_score', 0)}")
        print(f"   链接: {entry['link']}")

def filter_by_category(data, category):
    """按分类筛选文章"""
    filtered = [entry for entry in data if category in entry.get('categories', [])]
    print(f"\n筛选结果: {category} 类别共有 {len(filtered)} 篇文章")
    return filtered

def interactive_viewer(data):
    """交互式查看器"""
    while True:
        print("\n" + "=" * 60)
        print("数据查看器 - 请选择操作:")
        print("=" * 60)
        print("1. 显示数据统计")
        print("2. 显示质量评分TOP 10")
        print("3. 按分类筛选 (AI)")
        print("4. 按分类筛选 (Biotech)")
        print("5. 按分类筛选 (Startup)")
        print("6. 按分类筛选 (VC)")
        print("7. 导出为Markdown报告")
        print("0. 退出")
        print("=" * 60)
        
        choice = input("请输入选项: ").strip()
        
        if choice == '1':
            show_statistics(data)
        elif choice == '2':
            show_top_articles(data, 10)
        elif choice == '3':
            filtered = filter_by_category(data, 'AI')
            show_top_articles(filtered, 5)
        elif choice == '4':
            filtered = filter_by_category(data, 'Biotech')
            show_top_articles(filtered, 5)
        elif choice == '5':
            filtered = filter_by_category(data, 'Startup')
            show_top_articles(filtered, 5)
        elif choice == '6':
            filtered = filter_by_category(data, 'VC')
            show_top_articles(filtered, 5)
        elif choice == '7':
            export_to_markdown(data)
        elif choice == '0':
            print("退出查看器")
            break
        else:
            print("无效选项,请重新选择")

def export_to_markdown(data):
    """导出为Markdown报告"""
    filename = f"/home/ubuntu/tech_info_crawler/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 优质科技信息爬取报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"总文章数: {len(data)}\n\n")
        
        # 按分类导出
        categories = ['AI', 'Biotech', 'Startup', 'VC']
        for category in categories:
            filtered = [entry for entry in data if category in entry.get('categories', [])]
            if filtered:
                f.write(f"## {category} ({len(filtered)} 篇)\n\n")
                for i, entry in enumerate(filtered[:20], 1):
                    f.write(f"### {i}. {entry['title']}\n\n")
                    f.write(f"- **来源**: {entry['source']}\n")
                    f.write(f"- **评分**: {entry.get('quality_score', 0)}\n")
                    f.write(f"- **链接**: [{entry['link']}]({entry['link']})\n")
                    f.write(f"- **摘要**: {entry.get('summary', 'N/A')[:200]}...\n\n")
    
    print(f"\n报告已导出到: {filename}")

def main():
    """主程序入口"""
    data = load_latest_data()
    if data:
        interactive_viewer(data)

if __name__ == "__main__":
    main()
