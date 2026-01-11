'''
邮件发送模块
'''
import json
import subprocess
from datetime import datetime

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

def generate_markdown_report(data):
    """生成Markdown格式的完整报告"""
    filename = f"/home/ubuntu/tech_info_crawler/daily_report_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 优质科技信息日报\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n\n")
        f.write(f"**总文章数**: {len(data)}\n\n")
        
        # 数据统计
        f.write("## 📊 数据统计\n\n")
        
        # 按来源统计
        source_counts = {}
        for entry in data:
            source = entry['source']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        f.write("### 按来源统计\n\n")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{source}**: {count} 篇\n")
        f.write("\n")
        
        # 按分类统计
        category_counts = {}
        for entry in data:
            for category in entry.get('categories', ['General']):
                category_counts[category] = category_counts.get(category, 0) + 1
        
        f.write("### 按分类统计\n\n")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{category}**: {count} 篇\n")
        f.write("\n")
        
        f.write("---\n\n")
        
        # 按分类导出
        categories = ['AI', 'Biotech', 'Startup', 'VC']
        for category in categories:
            filtered = [entry for entry in data if category in entry.get('categories', [])]
            if filtered:
                f.write(f"## 🔥 {category} 领域 ({len(filtered)} 篇)\n\n")
                for i, entry in enumerate(filtered[:20], 1):
                    f.write(f"### {i}. {entry['title']}\n\n")
                    f.write(f"- **来源**: {entry['source']}\n")
                    f.write(f"- **评分**: {entry.get('quality_score', 0)}\n")
                    f.write(f"- **发布时间**: {entry.get('published', 'N/A')}\n")
                    f.write(f"- **链接**: [{entry['link']}]({entry['link']})\n")
                    
                    # 添加摘要(截取前300字符)
                    summary = entry.get('summary', 'N/A')
                    if len(summary) > 300:
                        summary = summary[:300] + "..."
                    f.write(f"- **摘要**: {summary}\n\n")
                    f.write("---\n\n")
        
        # 添加页脚
        f.write("\n---\n\n")
        f.write("*本报告由优质科技信息爬取系统自动生成*\n\n")
        f.write(f"*项目地址*: [https://github.com/Xiangyu-Li97/tech-info-crawler](https://github.com/Xiangyu-Li97/tech-info-crawler)\n")
    
    print(f"Markdown报告已生成: {filename}")
    return filename

def send_email_via_mcp(to_email, subject, markdown_file):
    """通过MCP工具发送邮件"""
    print(f"正在准备发送邮件到: {to_email}")
    
    # 构建邮件内容
    content = f"您好！\n\n这是今天的优质科技信息日报,详细内容请查看附件中的Markdown报告。\n\n"
    content += f"本邮件由优质科技信息爬取系统自动生成并发送。\n"
    content += f"项目地址: https://github.com/Xiangyu-Li97/tech-info-crawler\n"
    
    # 创建临时JSON输入文件
    email_data = {
        "messages": [
            {
                "to": [to_email],
                "subject": subject,
                "content": content,
                "attachments": [markdown_file]
            }
        ]
    }
    
    temp_json = "/tmp/email_input_temp.json"
    with open(temp_json, 'w', encoding='utf-8') as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)
    
    # 调用MCP工具发送邮件
    try:
        result = subprocess.run(
            f'manus-mcp-cli tool call gmail_send_messages --server gmail --input "$(cat {temp_json})"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("MCP工具输出:")
        print(result.stdout)
        
        if result.returncode == 0 and "Message ID" in result.stdout:
            print("✅ 邮件发送成功!")
            return True
        else:
            print(f"❌ 邮件发送失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 邮件发送超时")
        return False
    except Exception as e:
        print(f"❌ 邮件发送出错: {e}")
        return False

def send_daily_report(to_email):
    """发送每日报告的主函数"""
    print("\n" + "=" * 60)
    print("开始生成并发送每日科技信息报告")
    print("=" * 60)
    
    # 加载数据
    data = load_latest_processed_data()
    if not data:
        print("❌ 没有可用的数据,无法发送报告")
        return False
    
    # 生成Markdown报告附件
    markdown_file = generate_markdown_report(data)
    
    # 发送邮件
    subject = f"优质科技信息日报 - {datetime.now().strftime('%Y年%m月%d日')}"
    success = send_email_via_mcp(to_email, subject, markdown_file)
    
    if success:
        print(f"\n✅ 每日报告已成功发送到: {to_email}")
    else:
        print(f"\n❌ 每日报告发送失败")
    
    return success

if __name__ == "__main__":
    # 测试邮件发送 - 请替换为您的邮箱地址
    send_daily_report("your-email@example.com")
