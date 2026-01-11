# 优质科技信息爬取工具

[![Daily Crawler](https://github.com/Xiangyu-Li97/tech-info-crawler/actions/workflows/daily-crawl.yml/badge.svg)](https://github.com/Xiangyu-Li97/tech-info-crawler/actions/workflows/daily-crawl.yml)

## 1. 项目概述

本项目旨在构建一个自动化的优质科技信息聚合工具,专注于抓取、处理、分类和存储来自全球顶级信息源的科技资讯。当前版本主要覆盖 **AI 人工智能**、**Biotech 生物科技**、**硅谷创业 (Startup)** 和 **一级市场投资 (VC)** 四大领域。

该工具支持两种部署方式:

1. **GitHub Actions自动化**: 完全托管在GitHub,无需自己的服务器。
2. **服务器部署**: 在您自己的服务器上部署,更灵活,更强大。

## 2. 核心功能

- **多源信息聚合**: 支持从多个RSS订阅源并行抓取信息。
- **智能数据处理**: 
    - **内容去重**: 基于文章标题和链接计算哈希值,防止重复存储。
    - **跨天去重**: 维护历史爬取记录,自动过滤已爬取的文章。
    - **自动分类**: 内置关键词词典,可自动为文章打上AI、Biotech、Startup、VC等标签。
    - **质量评估**: 根据信息源权威性、标题和摘要长度等维度为每篇文章计算质量分。
    - **AI翻译总结**: 使用GPT-4模型自动翻译标题并生成中文摘要。
- **Discord推送**: 精美的Embed卡片格式,支持富文本展示。
- **自动化执行**: 支持GitHub Actions和服务器cron定时任务。

## 3. 部署方式

### 方式一: GitHub Actions (推荐,简单快捷)

**优点:**
- ✅ 完全免费
- ✅ 无需服务器
- ✅ 3分钟配置完成

**缺点:**
- ⚠️ 执行时间有限制
- ⚠️ 依赖GitHub平台稳定性

📚 **配置指南**: 查看 [QUICK_START.md](QUICK_START.md)

### 方式二: 服务器部署 (推荐,灵活强大)

**优点:**
- ✅ 完全控制执行时间和频率
- ✅ 不受平台限制,更稳定
- ✅ 方便扩展和二次开发

**缺点:**
- ⚠️ 需要一台自己的服务器
- ⚠️ 配置相对复杂

📚 **部署指南**: 查看 [SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)

## 4. 项目结构

```
/home/ubuntu/tech_info_crawler/
├── .github/workflows/daily-crawl.yml  # GitHub Actions工作流
├── run_daily.sh                       # 服务器部署执行脚本
├── config.env.example                 # 服务器部署配置文件示例
├── crawler.py                         # 核心爬虫模块
├── data_processor.py                  # 数据处理模块
├── ai_processor.py                    # AI翻译和总结模块
├── history_tracker.py                 # 历史跟踪模块
├── discord_sender.py                  # Discord推送模块
├── requirements.txt                   # Python依赖
├── README.md                          # 本文件
├── QUICK_START.md                     # GitHub Actions快速开始
├── SERVER_DEPLOYMENT.md               # 服务器部署指南
└── SOLUTION_GUIDE.md                  # 完整技术方案
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

## 6. 本地使用(开发和测试)

### 6.1 环境要求

- Python 3.10+
- OpenAI API密钥(用于AI翻译和总结)

### 6.2 安装依赖

```bash
pip install -r requirements.txt
```

### 6.3 手动执行

```bash
# 1. 复制并配置 config.env
cp config.env.example config.env
nano config.env

# 2. 执行主脚本
./run_daily.sh
```

## 7. 配置说明

### 7.1 添加新的RSS源

编辑 `crawler.py` 文件中的 `RSS_FEEDS` 字典。

### 7.2 修改推送文章数量

编辑 `discord_sender.py`,修改 `top_n` 参数。

### 7.3 禁用AI处理(节省成本)

- **服务器部署**: 在 `config.env` 中不配置 `OPENAI_API_KEY`
- **GitHub Actions**: 在工作流文件中修改 `data_processor.py` 的命令为 `python data_processor.py --no-ai`

## 8. 技术栈

- **语言**: Python 3.11, Bash
- **爬虫**: feedparser, requests
- **AI**: OpenAI GPT-4
- **自动化**: GitHub Actions, Cron
- **推送**: Discord Webhook API
- **数据处理**: JSON, hashlib

## 9. 未来工作

- **增强爬虫能力**: 支持更多信息源
- **优化AI评分**: 使用LLM评估文章质量
- **数据库存储**: 迁移到数据库
- **Web界面**: 开发Web前端
- **个性化推荐**: 根据阅读历史推荐

## 10. 贡献指南

欢迎提交Issue和Pull Request!

## 11. 许可证

MIT License

## 12. 项目地址

GitHub: https://github.com/Xiangyu-Li97/tech-info-crawler

---

**开始使用吧!** 🚀
- **GitHub Actions用户**: 查看 [QUICK_START.md](QUICK_START.md)
- **服务器用户**: 查看 [SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)
