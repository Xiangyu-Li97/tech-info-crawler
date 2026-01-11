# 优质科技信息爬取工具

## 1. 项目概述

本项目旨在构建一个自动化的优质科技信息聚合工具,专注于抓取、处理、分类和存储来自全球顶级信息源的科技资讯。当前版本主要覆盖 **AI 人工智能**、**Biotech 生物科技**、**硅谷创业 (Startup)** 和 **一级市场投资 (VC)** 四大领域。

该工具通过定时任务自动从指定的 RSS 订阅源获取最新文章,并对抓取到的数据进行一系列处理,包括去重、关键词分类和质量评估,最终将结构化的数据以 JSON 格式存储,并可生成易于阅读的 Markdown 报告。

**✨ 新功能**: 现已支持每天自动爬取并通过邮件发送Markdown格式的日报!

## 2. 主要功能

- **多源信息聚合**: 支持从多个 RSS 订阅源并行抓取信息。
- **智能数据处理**: 
    - **内容去重**: 基于文章标题和链接计算哈希值,防止重复存储。
    - **自动分类**: 内置关键词词典,可自动为文章打上 AI、Biotech、Startup、VC 等标签。
    - **质量评估**: 根据信息源权威性、标题和摘要长度等维度为每篇文章计算质量分,便于筛选高价值内容。
- **结构化数据存储**: 将处理后的文章以 JSON 格式保存,包含来源、标题、链接、发布时间、摘要、分类、质量分等丰富字段。
- **定时自动执行**: 支持每天自动执行爬取和数据处理任务。
- **邮件自动发送**: 每天自动生成Markdown格式的日报并发送到指定邮箱。
- **数据可视化与报告**: 
    - 提供一个交互式的命令行查看器,支持查看数据统计、按分类筛选和浏览高质量文章。
    - 可一键生成按类别组织的 Markdown 格式报告,方便快速浏览最新资讯。

## 3. 项目结构

```
/home/ubuntu/tech_info_crawler/
├── crawler.py            # 核心爬虫模块,负责从RSS源抓取数据
├── data_processor.py     # 数据处理模块,负责去重、分类、评分
├── email_sender.py       # 邮件发送模块,负责生成报告并发送邮件
├── scheduler.py          # 定时调度模块,负责自动执行任务
├── viewer.py             # 数据查看器模块,用于交互式浏览和报告生成
├── requirements.txt      # 项目依赖的Python库
├── README.md             # 本文件
├── SOLUTION_GUIDE.md     # 完整技术方案文档
├── crawled_data_*.json   # 原始抓取数据(临时文件)
├── processed_data_*.json # 处理后的结构化数据
└── daily_report_*.md     # 生成的每日Markdown报告
```

## 4. 安装与部署

### 4.1 环境要求

- Python 3.10+
- 已配置 Gmail MCP 工具(用于发送邮件)

### 4.2 安装依赖

在项目根目录下执行以下命令,安装所有必需的 Python 库:

```bash
sudo pip3 install -r requirements.txt
```

*注意: 由于部分库可能需要系统级权限,建议使用 `sudo`。*

## 5. 使用指南

所有命令都建议在 `/home/ubuntu/tech_info_crawler/` 目录下执行。

### 5.1 手动执行一次完整的爬取和处理

1.  **执行爬虫**:

    ```bash
    python3 crawler.py
    ```

    该命令会抓取 `crawler.py` 中配置的所有 RSS 源,并将原始数据保存为一个新的 `crawled_data_*.json` 文件。

2.  **执行数据处理**:

    ```bash
    python3 data_processor.py
    ```

    该命令会自动找到最新的 `crawled_data_*.json` 文件,对其进行处理,并保存为 `processed_data_*.json` 文件。

3.  **生成并发送邮件报告**:

    ```bash
    python3 email_sender.py
    ```

    该命令会生成Markdown格式的日报并通过Gmail发送到配置的邮箱。

### 5.2 自动化执行

本项目已配置为通过 Manus AI 的调度系统自动执行。每天早上9:00会自动:
1. 爬取最新科技信息
2. 处理和分类数据
3. 生成Markdown报告
4. 发送邮件到 xiangyuli997@gmail.com

无需手动干预,系统会自动运行!

### 5.3 查看和分析数据

执行交互式数据查看器:

```bash
python3 viewer.py
```

该脚本会自动加载最新的 `processed_data_*.json` 文件,并提供一个菜单供您进行交互式操作,包括:

- 查看数据统计(总数、来源分布、分类分布等)。
- 查看按质量分排序的 TOP 10 文章。
- 按指定分类(AI, Biotech 等)筛选文章。
- 生成一份完整的 Markdown 格式报告。

## 6. 配置说明

### 6.1 如何添加新的 RSS 源?

要添加或修改 RSS 订阅源,请直接编辑 `crawler.py` 文件中的 `RSS_FEEDS` 字典:

```python
# crawler.py

RSS_FEEDS = {
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    # 在这里添加新的源
    "Example News": "https://example.com/feed"
}
```

添加后,下次运行爬虫时就会自动包含新的信息源。

### 6.2 如何修改收件人邮箱?

编辑 `scheduler.py` 和 `email_sender.py` 文件,将 `RECIPIENT_EMAIL` 或 `xiangyuli997@gmail.com` 修改为您的邮箱地址。

### 6.3 如何调整执行时间?

当前系统配置为每天早上9:00执行。如需修改时间,请联系管理员调整调度任务的cron表达式。

## 7. 邮件报告格式

每日邮件报告包含:

- **邮件主题**: 优质科技信息日报 - [日期]
- **邮件正文**: 简短的问候和说明
- **附件**: Markdown格式的完整报告,包含:
  - 数据统计(总数、来源分布、分类分布)
  - AI领域精选文章(TOP 20)
  - Biotech领域精选文章(TOP 20)
  - Startup领域精选文章(TOP 20)
  - VC领域精选文章(TOP 20)
  - 每篇文章包含:标题、来源、评分、发布时间、链接、摘要

## 8. 未来工作

- **增强爬虫能力**: 集成 Playwright/Selenium,以支持抓取需要 JavaScript 渲染或受 Cloudflare 等保护的网站。
- **集成大语言模型 (LLM)**: 调用 GPT-4 或类似模型,实现更精准的内容摘要、质量评估和情感分析。
- **数据库存储**: 将数据存储从 JSON 文件迁移到 SQLite 或 PostgreSQL 数据库,以支持更复杂的查询和长期数据管理。
- **Web 界面**: 开发一个简单的 Web 前端,以更友好的方式展示和检索数据。
- **个性化推荐**: 根据用户阅读历史和兴趣标签,提供个性化的内容推荐。

## 9. 项目地址

GitHub: https://github.com/Xiangyu-Li97/tech-info-crawler
