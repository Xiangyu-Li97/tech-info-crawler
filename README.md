# 优质科技信息爬取工具

[![Daily Crawler](https://github.com/Xiangyu-Li97/tech-info-crawler/actions/workflows/daily-crawl.yml/badge.svg)](https://github.com/Xiangyu-Li97/tech-info-crawler/actions/workflows/daily-crawl.yml)

## 1. 项目概述

本项目旨在构建一个自动化的优质科技信息聚合工具,专注于抓取、处理、分类和存储来自全球顶级信息源的科技资讯。当前版本主要覆盖 **AI 人工智能**、**Biotech 生物科技**、**硅谷创业 (Startup)** 和 **一级市场投资 (VC)** 四大领域。

该工具通过GitHub Actions自动化执行,每天定时从指定的RSS订阅源获取最新文章,并对抓取到的数据进行一系列处理,包括去重、关键词分类、AI翻译总结和质量评估,最终将精选内容推送到Discord频道。

## 2. 核心功能

### ✨ 最新特性

- **GitHub Actions自动化**: 完全托管在GitHub,无需自己的服务器
- **Discord推送**: 每天自动推送TOP 10文章到Discord频道
- **AI智能翻译和总结**: 每篇文章自动生成中文标题和中文摘要
- **跨天去重机制**: 自动过滤历史已爬取的文章,确保每天只展示新内容
- **邮件自动发送**: 可选的邮件推送功能

### 主要功能

- **多源信息聚合**: 支持从多个RSS订阅源并行抓取信息
- **智能数据处理**: 
    - **内容去重**: 基于文章标题和链接计算哈希值,防止重复存储
    - **跨天去重**: 维护历史爬取记录,自动过滤已爬取的文章
    - **自动分类**: 内置关键词词典,可自动为文章打上AI、Biotech、Startup、VC等标签
    - **质量评估**: 根据信息源权威性、标题和摘要长度等维度为每篇文章计算质量分
    - **AI翻译总结**: 使用GPT-4模型自动翻译标题并生成中文摘要
- **Discord推送**: 精美的Embed卡片格式,支持富文本展示
- **GitHub Actions自动化**: 每天定时执行,完全托管,无需维护服务器

## 3. 快速开始

### 🚀 3分钟配置指南

1. **Fork本仓库到您的GitHub账号**

2. **配置GitHub Secrets**
   
   访问: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
   
   添加两个Secrets:
   - `DISCORD_WEBHOOK_URL`: 您的Discord Webhook URL
   - `OPENAI_API_KEY`: 您的OpenAI API密钥(可选)

3. **启用GitHub Actions**
   
   访问: `Actions` 标签 → 启用工作流

4. **手动测试运行**
   
   `Actions` → `Daily Tech Info Crawler` → `Run workflow`

5. **完成!** 🎉
   
   系统将每天早上9:00(北京时间)自动执行

📚 **详细配置指南**: 查看 [QUICK_START.md](QUICK_START.md)

## 4. 项目结构

```
/home/ubuntu/tech_info_crawler/
├── .github/
│   └── workflows/
│       └── daily-crawl.yml      # GitHub Actions工作流配置
├── crawler.py                   # 核心爬虫模块
├── data_processor.py            # 数据处理模块
├── ai_processor.py              # AI翻译和总结模块
├── history_tracker.py           # 历史跟踪模块
├── discord_sender.py            # Discord推送模块
├── email_sender.py              # 邮件发送模块(可选)
├── scheduler.py                 # 本地调度模块(可选)
├── viewer.py                    # 数据查看器
├── requirements.txt             # Python依赖
├── README.md                    # 本文件
├── QUICK_START.md               # 快速开始指南
├── GITHUB_ACTIONS_SETUP.md      # GitHub Actions详细配置
└── SOLUTION_GUIDE.md            # 完整技术方案
```

## 5. Discord推送效果

### 概览消息
```
📊 今日科技资讯 - 2026年01月11日

✅ 共爬取 60 篇新文章
🤖 AI: 24篇 | 🧬 Biotech: 12篇 | 🚀 Startup: 4篇 | 💰 VC: 3篇

📌 精选TOP 10文章如下 ↓
```

### 文章卡片(Embed格式)
每篇文章以精美的Embed卡片展示:
- 🎨 **分类图标和颜色**: AI(蓝色)、Biotech(绿色)、Startup(黄色)、VC(粉色)
- 📝 **中文标题**: AI自动翻译
- 📄 **中文摘要**: 2-3句话精炼总结
- ⭐ **质量评分**: 五星评级系统
- 🔗 **原文链接**: 一键跳转
- 📰 **来源标注**: 权威媒体来源

## 6. 本地使用(可选)

如果您想在本地运行,而不使用GitHub Actions:

### 6.1 环境要求

- Python 3.10+
- OpenAI API密钥(用于AI翻译和总结)

### 6.2 安装依赖

```bash
pip install -r requirements.txt
```

### 6.3 手动执行

```bash
# 1. 爬取数据
python3 crawler.py

# 2. 处理数据(包含AI翻译和跨天去重)
python3 data_processor.py

# 3. 推送到Discord
python3 discord_sender.py "YOUR_WEBHOOK_URL"

# 4. 查看数据(可选)
python3 viewer.py
```

## 7. 配置说明

### 7.1 添加新的RSS源

编辑 `crawler.py` 文件中的 `RSS_FEEDS` 字典:

```python
RSS_FEEDS = {
    "TechCrunch": "http://feeds.feedburner.com/TechCrunch/",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    # 在这里添加新的源
    "Example News": "https://example.com/feed"
}
```

### 7.2 修改推送时间

编辑 `.github/workflows/daily-crawl.yml`:

```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = 北京时间 9:00
```

### 7.3 修改推送文章数量

编辑 `discord_sender.py`:

```python
send_daily_report_to_discord(webhook_url, top_n=10)  # 修改为您想要的数量
```

### 7.4 禁用AI处理(节省成本)

编辑 `.github/workflows/daily-crawl.yml`:

```yaml
- name: Process data without AI
  run: python data_processor.py --no-ai
```

## 8. 跨天去重机制

### 工作原理

系统维护一个 `crawled_history.json` 文件,记录所有已爬取文章的内容哈希值。每次处理新数据时:

1. 计算每篇文章的哈希值(基于标题和链接)
2. 与历史记录比对
3. 只保留新文章进行后续处理
4. 处理完成后更新历史记录

### 特点

- **自动维护**: GitHub Actions自动提交更新
- **高效存储**: 只保存最近500篇文章的记录
- **可选功能**: 可通过参数禁用

## 9. AI翻译和总结

### 功能说明

每篇文章都会通过GPT-4模型进行:
- **标题翻译**: 将英文标题翻译为简洁的中文
- **内容总结**: 基于摘要生成2-3句话的中文总结(150字以内)

### 成本估算

- 每篇文章约消耗 500-1000 tokens
- 每天处理60篇文章约消耗 0.05-0.1 USD
- 每月成本约 1.5-3 USD

## 10. 质量评分说明

质量评分基于以下维度计算(总分0-30分):

1. **信息源权威性** (5-10分): MIT Technology Review(10分)、Wired(9分)等
2. **标题长度** (0-5分): 30-100字符最佳(5分)
3. **摘要长度** (0-5分): >200字符(5分)
4. **分类标签** (0-8分): 每个非General分类+2分

## 11. 故障排查

### GitHub Actions执行失败

1. 检查Secrets是否正确配置
2. 查看Actions日志找到具体错误
3. 确认Discord Webhook URL有效
4. 验证OpenAI API密钥有效(如果启用AI)

### Discord没有收到消息

1. 检查Webhook URL是否正确
2. 确认Discord频道权限设置
3. 查看Actions日志中的Discord推送步骤

### AI处理失败

1. 检查OpenAI API密钥是否有效
2. 确认API账户有足够余额
3. 可以临时禁用AI处理

## 12. 技术栈

- **语言**: Python 3.11
- **爬虫**: feedparser, requests
- **AI**: OpenAI GPT-4
- **自动化**: GitHub Actions
- **推送**: Discord Webhook API
- **数据处理**: JSON, hashlib

## 13. 未来工作

- **增强爬虫能力**: 支持更多信息源
- **优化AI评分**: 使用LLM评估文章质量
- **数据库存储**: 迁移到数据库
- **Web界面**: 开发Web前端
- **个性化推荐**: 根据阅读历史推荐

## 14. 贡献指南

欢迎提交Issue和Pull Request!

## 15. 许可证

MIT License

## 16. 项目地址

GitHub: https://github.com/Xiangyu-Li97/tech-info-crawler

---

**开始使用吧!** 🚀 查看 [QUICK_START.md](QUICK_START.md) 获取3分钟配置指南。
