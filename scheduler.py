'''
定时调度模块
'''
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import subprocess
import os

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
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 爬虫执行成功")
            
            # 自动处理数据
            run_data_processor()
    except subprocess.TimeoutExpired:
        print("爬虫执行超时")
    except Exception as e:
        print(f"爬虫执行出错: {e}")

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
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 数据处理成功")
    except subprocess.TimeoutExpired:
        print("数据处理超时")
    except Exception as e:
        print(f"数据处理出错: {e}")

def main():
    """主程序入口"""
    print("=" * 60)
    print("优质科技信息爬取系统 - 定时调度器")
    print("=" * 60)
    print("调度配置:")
    print("  - 每2小时执行一次爬取任务")
    print("  - 爬取完成后自动进行数据处理")
    print("=" * 60)
    
    # 创建调度器
    scheduler = BlockingScheduler()
    
    # 添加定时任务:每2小时执行一次
    scheduler.add_job(
        run_crawler,
        trigger=IntervalTrigger(hours=2),
        id='crawler_job',
        name='科技信息爬取任务',
        replace_existing=True
    )
    
    # 立即执行一次
    print("\n立即执行首次爬取任务...")
    run_crawler()
    
    # 启动调度器
    print("\n调度器已启动,按 Ctrl+C 停止...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n调度器已停止")

if __name__ == "__main__":
    main()
