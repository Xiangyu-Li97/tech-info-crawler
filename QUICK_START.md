# 快速开始 - GitHub Actions自动化

## 🎯 目标

配置GitHub Actions,实现每天自动:
- 🕷️ 爬取最新科技资讯
- 🤖 AI翻译标题和生成中文摘要
- 🔄 过滤历史重复内容
- 📤 推送TOP 10文章到Discord频道

## ⚡ 3分钟快速配置

### 步骤1: 配置GitHub Secrets (2分钟)

1. **打开仓库设置页面**
   
   访问: https://github.com/Xiangyu-Li97/tech-info-crawler/settings/secrets/actions

2. **添加两个Secrets**

   点击 `New repository secret`,添加:

   **Secret 1:**
   ```
   Name: DISCORD_WEBHOOK_URL
   Value: https://discord.com/api/webhooks/1459794905290244290/mOx2EXSlaYBvZc-X9IzTNco4eh209n_prerjg7-6MPOTcfLYWpHG2m40c8ixs0DjsOsg
   ```

   **Secret 2:**
   ```
   Name: OPENAI_API_KEY
   Value: [您的OpenAI API密钥]
   ```

   > 💡 如果您没有OpenAI API密钥,可以暂时跳过,工作流会自动跳过AI处理步骤

### 步骤2: 测试运行 (1分钟)

1. **访问Actions页面**
   
   https://github.com/Xiangyu-Li97/tech-info-crawler/actions

2. **手动触发测试**
   
   - 点击左侧 `Daily Tech Info Crawler`
   - 点击右侧 `Run workflow` 按钮
   - 点击绿色 `Run workflow` 确认

3. **查看执行结果**
   
   - 等待2-3分钟
   - 查看Discord频道是否收到消息
   - 点击工作流查看详细日志

### 步骤3: 完成! 🎉

配置完成后,系统会**每天早上9:00(北京时间)**自动执行,无需任何操作!

## 📊 您将收到什么?

### Discord消息格式

**消息1: 概览**
```
📊 今日科技资讯 - 2026年01月11日

✅ 共爬取 60 篇新文章
🤖 AI: 24篇 | 🧬 Biotech: 12篇 | 🚀 Startup: 4篇 | 💰 VC: 3篇

📌 精选TOP 10文章如下 ↓
```

**消息2-11: 每篇文章(Embed卡片)**
```
🤖 AI #1 - 下载速递:AI模糊效应的价值及助力CRISPR实现潜力

本期《下载速递》聚焦人工智能中的"模糊效应"现象,探讨其如何突破大众认知界限...

📰 来源: MIT Technology Review
⭐ 评分: ⭐⭐⭐⭐⭐ (24分)
🔗 [阅读原文]
```

## 🔧 常见问题

### Q: 如何修改推送时间?

编辑 `.github/workflows/daily-crawl.yml`:
```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = 北京时间 9:00
```

### Q: 如何修改推送文章数量?

编辑 `discord_sender.py`,修改 `top_n` 参数:
```python
send_daily_report_to_discord(webhook_url, top_n=20)  # 改为20篇
```

### Q: 如何禁用AI处理(节省成本)?

编辑 `.github/workflows/daily-crawl.yml`:
```yaml
- name: Process data without AI
  run: python data_processor.py --no-ai
```

### Q: 工作流执行失败怎么办?

1. 检查Secrets是否正确配置
2. 查看Actions日志找到具体错误
3. 确认Discord Webhook URL有效
4. 验证OpenAI API密钥有效(如果启用AI)

## 📚 更多信息

- 详细配置指南: `GITHUB_ACTIONS_SETUP.md`
- 完整技术方案: `SOLUTION_GUIDE.md`
- 项目README: `README.md`

---

**开始配置吧!** 🚀
