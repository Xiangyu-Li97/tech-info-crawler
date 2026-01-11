'''
数据处理模块
'''
import json
import hashlib
from datetime import datetime

def calculate_content_hash(title, link):
    """计算内容哈希值用于去重"""
    content = f"{title}{link}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def deduplicate_entries(entries):
    """去除重复的文章条目"""
    seen_hashes = set()
    unique_entries = []
    duplicates = 0
    
    for entry in entries:
        content_hash = calculate_content_hash(entry['title'], entry['link'])
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            entry['content_hash'] = content_hash
            unique_entries.append(entry)
        else:
            duplicates += 1
    
    print(f"去重完成: 原始 {len(entries)} 条,去重后 {len(unique_entries)} 条,移除 {duplicates} 条重复")
    return unique_entries

def classify_by_keywords(entry):
    """基于关键词对文章进行分类"""
    title = entry.get('title', '').lower()
    summary = entry.get('summary', '').lower()
    content = title + ' ' + summary
    
    categories = []
    
    # AI关键词
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 
                   'neural network', 'chatgpt', 'gpt', 'llm', 'large language model',
                   'computer vision', 'nlp', 'natural language processing']
    if any(keyword in content for keyword in ai_keywords):
        categories.append('AI')
    
    # Biotech关键词
    biotech_keywords = ['biotech', 'biotechnology', 'pharma', 'pharmaceutical', 'drug', 
                        'medicine', 'gene', 'genetic', 'crispr', 'therapy', 'clinical trial',
                        'fda approval', 'vaccine', 'antibody']
    if any(keyword in content for keyword in biotech_keywords):
        categories.append('Biotech')
    
    # 创业关键词
    startup_keywords = ['startup', 'founder', 'entrepreneur', 'silicon valley', 
                        'y combinator', 'accelerator', 'incubator', 'launch']
    if any(keyword in content for keyword in startup_keywords):
        categories.append('Startup')
    
    # 投资关键词
    vc_keywords = ['venture capital', 'vc', 'funding', 'investment', 'investor', 
                   'series a', 'series b', 'seed round', 'ipo', 'acquisition', 
                   'valuation', 'unicorn']
    if any(keyword in content for keyword in vc_keywords):
        categories.append('VC')
    
    return categories if categories else ['General']

def add_categories(entries):
    """为所有文章添加分类标签"""
    print("正在为文章添加分类标签...")
    for entry in entries:
        entry['categories'] = classify_by_keywords(entry)
    
    # 统计各类别数量
    category_counts = {}
    for entry in entries:
        for category in entry['categories']:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    print("分类统计:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 篇")
    
    return entries

def calculate_quality_score(entry):
    """计算文章质量评分"""
    score = 0
    
    # 基于信息源的权威性评分
    source_scores = {
        'MIT Technology Review': 10,
        'Wired': 9,
        'TechCrunch': 8,
        'Fierce Biotech': 9,
        'PitchBook': 8
    }
    score += source_scores.get(entry['source'], 5)
    
    # 基于标题长度评分(过短或过长都不好)
    title_length = len(entry['title'])
    if 30 <= title_length <= 100:
        score += 5
    elif 20 <= title_length < 30 or 100 < title_length <= 150:
        score += 3
    
    # 基于摘要长度评分
    summary_length = len(entry.get('summary', ''))
    if summary_length > 200:
        score += 5
    elif summary_length > 100:
        score += 3
    
    # 基于分类数量评分(有明确分类的文章更有价值)
    if 'categories' in entry and 'General' not in entry['categories']:
        score += len(entry['categories']) * 2
    
    return score

def add_quality_scores(entries):
    """为所有文章添加质量评分"""
    print("正在计算文章质量评分...")
    for entry in entries:
        entry['quality_score'] = calculate_quality_score(entry)
    
    # 按质量评分排序
    entries.sort(key=lambda x: x['quality_score'], reverse=True)
    
    avg_score = sum(e['quality_score'] for e in entries) / len(entries) if entries else 0
    print(f"平均质量评分: {avg_score:.2f}")
    
    return entries

def process_data(input_file, output_file):
    """处理数据的主函数"""
    print(f"正在从 {input_file} 读取数据...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取了 {len(data)} 条原始数据")
    
    # 去重
    data = deduplicate_entries(data)
    
    # 添加分类
    data = add_categories(data)
    
    # 添加质量评分
    data = add_quality_scores(data)
    
    # 保存处理后的数据
    print(f"正在将处理后的数据保存到 {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("数据处理完成!")
    return data

if __name__ == "__main__":
    # 测试数据处理
    import glob
    json_files = glob.glob("/home/ubuntu/tech_info_crawler/crawled_data_*.json")
    if json_files:
        latest_file = sorted(json_files)[-1]
        output_file = latest_file.replace('crawled_data_', 'processed_data_')
        process_data(latest_file, output_file)
    else:
        print("未找到待处理的数据文件")
