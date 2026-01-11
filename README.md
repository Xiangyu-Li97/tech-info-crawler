# 优质科技信息爬取工具

## 1. 项目概述

本项目旨在构建一个自动化的优质科技信息聚合工具,专注于抓取、处理、分类和存储来自全球顶级信息源的科技资讯。当前版本主要覆盖 **AI 人工智能**、**Biotech 生物科技**、**硅谷创业 (Startup)** 和 **一级市场投资 (VC)** 四大领域。

该工具通过定时任务自动从指定的 RSS 订阅源获取最新文章,并对抓取到的数据进行一系列处理,包括去重、关键词分类和质量评估,最终将结构化的数据以 JSON 格式存储,并可生成易于阅读的 Markdown 报告。

## 2. 核心功能

### ✨ 最新升级

- **AI智能翻译和总结**: 每篇文章自动生成中文标题和中文摘要
- **跨天去重机制**: 自动过滤历史已爬取的文章,确保每天只展示新内容
- **邮件自动发送**: 每天自动生成并发送Markdown格式的日报

### 主要功能

- **多源信息聚合**: 支持从多个 RSS 订阅源并行抓取信息。
- **智能数据处理**: 
    - **内容去重**: 基于文章标题和链接计算哈希值,防止重复存储。
    - **跨天去重**: 维护历史爬取记录,自动过滤已爬取的文章。
    - **自动分类**: 内置关键词词典,可自动为文章打上 AI、Biotech、Startup、VC 等标签。
    - **质量评估**: 根据信息源权威性、标题和摘要长度等维度为每篇文章计算质量分。
    - **AI翻译总结**: 使用GPT-4模型自动翻译标题并生成中文摘要。
- **结构化数据存储**: 将处理后的文章以 JSON 格式保存,包含来源、标题、链接、发布时间、摘要、分类、质量分、中文标题、中文摘要等丰富字段。
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
├── ai_processor.py       # AI处理模块,负责翻译标题和生成中文摘要
├── history_tracker.py    # 历史跟踪模块,负责跨天去重
├── email_sender.py       # 邮件发送模块,负责生成报告并发送邮件
├── scheduler.py          # 定时调度模块,负责自动执行任务
├── viewer.py             # 数据查看器模块,用于交互式浏览和报告生成
├── requirements.txt      # 项目依赖的Python库
├── README.md             # 本文件
├── SOLUTION_GUIDE.md     # 完整技术方案文档
├── crawled_data_*.json   # 原始抓取数据(临时文件)
├── processed_data_*.json # 处理后的结构化数据
├── crawled_history.json  # 历史爬取记录(用于跨天去重)
└── daily_report_*.md     # 生成的每日Markdown报告
```

## 4. 安装与部署

### 4.1 环境要求

- Python 3.10+
- 已配置 Gmail MCP 工具(用于发送邮件)
- OpenAI API 密钥(用于AI翻译和总结)

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

2.  **执行数据处理**(包含AI翻译和跨天去重):

    ```bash
    python3 data_processor.py
    ```

    该命令会自动:
    - 找到最新的 `crawled_data_*.json` 文件
    - 过滤掉历史已爬取的文章
    - 对新文章进行分类和质量评分
    - 使用AI翻译标题并生成中文摘要
    - 保存为 `processed_data_*.json` 文件
    - 更新历史记录

3.  **生成并发送邮件报告**:

    ```bash
    python3 email_sender.py
    ```

    该命令会生成Markdown格式的日报并通过Gmail发送到配置的邮箱。

### 5.2 自动化执行

本项目已配置为通过 Manus AI 的调度系统自动执行。每天早上9:00会自动:
1. 爬取最新科技信息
2. 过滤历史重复内容
3. AI翻译和总结新文章
4. 生成Markdown报告
5. 发送邮件到指定邮箱

无需手动干预,系统会自动运行!

### 5.3 查看和分析数据

执行交互式数据查看器:

```bash
python3 viewer.py
```

该脚本会自动加载最新的 `processed_data_*.json` 文件,并提供一个菜单供您进行交互式操作。

### 5.4 命令行选项

数据处理支持以下选项:

```bash
# 禁用AI处理(不翻译,不总结)
python3 data_processor.py --no-ai

# 禁用历史去重(处理所有文章,不过滤)
python3 data_processor.py --no-history

# 同时禁用AI和历史去重
python3 data_processor.py --no-ai --no-history
```

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

编辑 `scheduler.py` 文件,将 `RECIPIENT_EMAIL` 修改为您的邮箱地址。

### 6.3 如何调整执行时间?

当前系统配置为每天早上9:00执行。如需修改时间,请联系管理员调整调度任务的cron表达式。

### 6.4 如何清空历史记录?

如果需要重新开始爬取所有文章(不过滤历史):

```bash
rm -f /home/ubuntu/tech_info_crawler/crawled_history.json
```

## 7. 跨天去重机制

### 工作原理

系统维护一个 `crawled_history.json` 文件,记录所有已爬取文章的内容哈希值。每次处理新数据时:

1. 计算每篇文章的哈希值(基于标题和链接)
2. 与历史记录比对
3. 只保留新文章进行后续处理
4. 处理完成后更新历史记录

### 特点

- **自动维护**: 无需手动管理,系统自动更新
- **高效存储**: 只保存最近500篇文章的记录,避免文件过大
- **可选功能**: 可通过 `--no-history` 参数禁用

## 8. AI翻译和总结

### 功能说明

每篇文章都会通过GPT-4模型进行:
- **标题翻译**: 将英文标题翻译为简洁的中文
- **内容总结**: 基于摘要生成2-3句话的中文总结(150字以内)

### 数据结构

处理后的文章包含以下字段:
```json
{
  "title": "原英文标题",
  "chinese_title": "中文标题",
  "summary": "原英文摘要",
  "chinese_summary": "中文摘要",
  "link": "原文链接",
  "source": "来源",
  "quality_score": 24,
  "categories": ["AI", "Biotech"]
}
```

## 9. 邮件报告格式

每日邮件报告包含:

- **邮件主题**: 优质科技信息日报 - [日期]
- **邮件正文**: 简短的说明
- **附件**: Markdown格式的完整报告,包含:
  - 数据统计(总数、来源分布、分类分布)
  - AI领域精选文章(TOP 20)
  - Biotech领域精选文章(TOP 20)
  - Startup领域精选文章(TOP 20)
  - VC领域精选文章(TOP 20)
  
每篇文章包含:
- 中文标题
- 中文摘要
- 原文链接
- 来源和质量评分
- 原标题(参考)

## 10. 质量评分说明

质量评分基于以下维度计算(总分0-30分):

1. **信息源权威性** (5-10分): MIT Technology Review(10分)、Wired(9分)等
2. **标题长度** (0-5分): 30-100字符最佳(5分)
3. **摘要长度** (0-5分): >200字符(5分)
4. **分类标签** (0-8分): 每个非General分类+2分

## 11. 未来工作

- **增强爬虫能力**: 集成 Playwright/Selenium,支持抓取需要 JavaScript 渲染的网站
- **优化AI评分**: 使用LLM评估文章的创新性、深度和实用性
- **数据库存储**: 迁移到 SQLite 或 PostgreSQL,支持更复杂的查询
- **Web 界面**: 开发 Web 前端,提供更友好的浏览和检索体验
- **个性化推荐**: 根据用户阅读历史提供个性化内容推荐

## 12. 项目地址

GitHub: https://github.com/Xiangyu-Li97/tech-info-crawler
