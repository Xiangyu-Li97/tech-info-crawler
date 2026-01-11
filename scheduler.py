'''
定时调度模块 - 每日自动爬取并发送邮件
'''
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import subprocess
import os

# 配置收件人邮箱
RECIPIENT_EMAIL = "xiangyuli997@gmail.com"

def run_crawler():
    """执行爬虫任务"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行定时爬取任务...")
    try:
        result = subprocess.run(
            ['python3', '/home/ubuntu/tech_info_crawler/crawler.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"爬虫执行失败: {result.stderr}")
            return False
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 爬虫执行成功")
            return True
    except subprocess.TimeoutExpired:
        print("爬虫执行超时")
        return False
    except Exception as e:
        print(f"爬虫执行出错: {e}")
        return False

def run_data_processor():
    """执行数据处理任务"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行数据处理任务...")
    try:
        result = subprocess.run(
            ['python3', '/home/ubuntu/tech_info_crawler/data_processor.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"数据处理失败: {result.stderr}")
            return False
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 数据处理成功")
            return True
    except subprocess.TimeoutExpired:
        print("数据处理超时")
        return False
    except Exception as e:
        print(f"数据处理出错: {e}")
        return False

def send_email_report():
    """发送邮件报告"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始发送邮件报告...")
    try:
        result = subprocess.run(
            ['python3', '/home/ubuntu/tech_info_crawler/email_sender.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"邮件发送失败: {result.stderr}")
            return False
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 邮件发送成功")
            return True
    except subprocess.TimeoutExpired:
        print("邮件发送超时")
        return False
    except Exception as e:
        print(f"邮件发送出错: {e}")
        return False

def daily_task():
    """每日任务:爬取 -> 处理 -> 发送邮件"""
    print("\n" + "=" * 60)
    print(f"开始执行每日任务 - {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("=" * 60)
    
    # 步骤1: 爬取数据
    if not run_crawler():
        print("❌ 爬取失败,任务终止")
        return
    
    # 步骤2: 处理数据
    if not run_data_processor():
        print("❌ 数据处理失败,任务终止")
        return
    
    # 步骤3: 发送邮件
    if not send_email_report():
        print("❌ 邮件发送失败")
        return
    
    print("\n" + "=" * 60)
    print(f"✅ 每日任务执行完成 - {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("=" * 60)

def main():
    """主程序入口"""
    print("=" * 60)
    print("优质科技信息爬取系统 - 每日自动调度器")
    print("=" * 60)
    print(f"收件人邮箱: {RECIPIENT_EMAIL}")
    print("调度配置:")
    print("  - 每天早上 9:00 执行一次爬取和邮件发送")
    print("  - 时区: 系统本地时间")
    print("=" * 60)
    
    # 创建调度器
    scheduler = BlockingScheduler()
    
    # 添加定时任务:每天早上9点执行
    scheduler.add_job(
        daily_task,
        trigger=CronTrigger(hour=9, minute=0),
        id='daily_crawler_job',
        name='每日科技信息爬取和邮件发送任务',
        replace_existing=True
    )
    
    # 立即执行一次
    print("\n立即执行首次任务...")
    daily_task()
    
    # 启动调度器
    print("\n调度器已启动,将在每天早上9:00自动执行...")
    print("按 Ctrl+C 停止调度器\n")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n调度器已停止")

if __name__ == "__main__":
    main()
