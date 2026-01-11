# 优质科技信息爬取工具

## 1. 项目概述

本项目旨在构建一个自动化的优质科技信息聚合工具,专注于抓取、处理、分类和存储来自全球顶级信息源的科技资讯。当前版本主要覆盖 **AI 人工智能**、**Biotech 生物科技**、**硅谷创业 (Startup)** 和 **一级市场投资 (VC)** 四大领域。

该工具通过定时任务自动从指定的 RSS 订阅源获取最新文章,并对抓取到的数据进行一系列处理,包括去重、关键词分类和质量评估,最终将结构化的数据以 JSON 格式存储,并可生成易于阅读的 Markdown 报告。

## 2. 主要功能

- **多源信息聚合**: 支持从多个 RSS 订阅源并行抓取信息。
- **智能数据处理**: 
    - **内容去重**: 基于文章标题和链接计算哈希值,防止重复存储。
    - **自动分类**: 内置关键词词典,可自动为文章打上 AI、Biotech、Startup、VC 等标签。
    - **质量评估**: 根据信息源权威性、标题和摘要长度等维度为每篇文章计算质量分,便于筛选高价值内容。
- **结构化数据存储**: 将处理后的文章以 JSON 格式保存,包含来源、标题、链接、发布时间、摘要、分类、质量分等丰富字段。
- **定时自动执行**: 内置调度器,可配置为定时自动执行爬取和数据处理任务(默认为每2小时)。
- **数据可视化与报告**: 
    - 提供一个交互式的命令行查看器,支持查看数据统计、按分类筛选和浏览高质量文章。
    - 可一键生成按类别组织的 Markdown 格式报告,方便快速浏览最新资讯。

## 3. 项目结构

```
/home/ubuntu/tech_info_crawler/
├── crawler.py            # 核心爬虫模块,负责从RSS源抓取数据
├── data_processor.py     # 数据处理模块,负责去重、分类、评分
├── scheduler.py          # 定时调度模块,负责自动执行任务
├── viewer.py             # 数据查看器模块,用于交互式浏览和报告生成
├── requirements.txt      # 项目依赖的Python库
├── tech_solution_design.md # (开发者文档)系统技术方案设计
├── crawled_data_*.json   # 原始抓取数据(临时文件)
├── processed_data_*.json # 处理后的结构化数据
└── report_*.md            # 生成的Markdown报告
```

## 4. 安装与部署

### 4.1 环境要求

- Python 3.10+

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

### 5.2 启动定时自动爬取

要让系统自动在后台定时运行,请执行调度器脚本:

```bash
python3 scheduler.py
```

该脚本会立即执行一次任务,然后根据预设的时间间隔(默认为每2小时)持续在后台运行。您可以按 `Ctrl+C` 停止调度器。

*建议使用 `nohup` 或 `screen` 等工具让调度器在后台持久运行:*

```bash
nohup python3 scheduler.py &> scheduler.log &
```

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

### 如何添加新的 RSS 源?

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

## 7. 未来工作

- **增强爬虫能力**: 集成 Playwright/Selenium,以支持抓取需要 JavaScript 渲染或受 Cloudflare 等保护的网站。
- **集成大语言模型 (LLM)**: 调用 GPT-4 或类似模型,实现更精准的内容摘要、质量评估和情感分析。
- **数据库存储**: 将数据存储从 JSON 文件迁移到 SQLite 或 PostgreSQL 数据库,以支持更复杂的查询和长期数据管理。
- **Web 界面**: 开发一个简单的 Web 前端,以更友好的方式展示和检索数据。
