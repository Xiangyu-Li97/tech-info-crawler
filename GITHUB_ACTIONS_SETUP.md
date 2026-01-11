# GitHub Actions 配置指南

本文档将指导您如何配置GitHub Actions,实现每天自动爬取科技资讯并推送到Discord。

## 📋 前置要求

- GitHub账号
- Discord Webhook URL
- OpenAI API Key(用于AI翻译和总结)

## 🚀 配置步骤

### 第一步:配置GitHub Secrets

GitHub Secrets用于安全地存储敏感信息(如API密钥、Webhook URL等)。

1. **打开仓库设置**
   - 访问您的GitHub仓库: https://github.com/Xiangyu-Li97/tech-info-crawler
   - 点击顶部的 `Settings` 标签

2. **进入Secrets配置页面**
   - 在左侧菜单中找到 `Secrets and variables`
   - 点击 `Actions`

3. **添加以下Secrets**

   点击 `New repository secret` 按钮,分别添加以下两个密钥:

   **Secret 1: DISCORD_WEBHOOK_URL**
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: `https://discord.com/api/webhooks/1459794905290244290/mOx2EXSlaYBvZc-X9IzTNco4eh209n_prerjg7-6MPOTcfLYWpHG2m40c8ixs0DjsOsg`
   - 点击 `Add secret`

   **Secret 2: OPENAI_API_KEY**
   - Name: `OPENAI_API_KEY`
   - Value: 您的OpenAI API密钥(从环境变量 `$OPENAI_API_KEY` 获取)
   - 点击 `Add secret`

### 第二步:启用GitHub Actions

1. **查看Actions页面**
   - 点击仓库顶部的 `Actions` 标签
   - 您应该能看到名为 `Daily Tech Info Crawler` 的工作流

2. **启用工作流**
   - 如果工作流被禁用,点击 `I understand my workflows, go ahead and enable them` 按钮

### 第三步:测试工作流

1. **手动触发测试**
   - 在 `Actions` 页面,点击左侧的 `Daily Tech Info Crawler`
   - 点击右侧的 `Run workflow` 下拉菜单
   - 点击绿色的 `Run workflow` 按钮

2. **查看执行结果**
   - 等待几分钟,工作流会自动执行
   - 点击正在运行的工作流查看详细日志
   - 检查Discord频道是否收到推送消息

### 第四步:验证定时任务

工作流已配置为每天UTC时间1:00执行(北京时间9:00)。

- **Cron表达式**: `0 1 * * *`
- **执行频率**: 每天一次
- **执行时间**: 北京时间早上9:00

您无需做任何操作,GitHub Actions会自动在指定时间运行。

## 📊 工作流执行内容

每次执行时,工作流会自动完成以下步骤:

1. ✅ **检出代码**: 从GitHub仓库拉取最新代码
2. ✅ **安装依赖**: 安装Python和所需的库
3. ✅ **爬取数据**: 从RSS源抓取最新科技资讯
4. ✅ **AI处理**: 翻译标题并生成中文摘要
5. ✅ **跨天去重**: 过滤历史已爬取的文章
6. ✅ **推送Discord**: 发送TOP 10文章到Discord频道
7. ✅ **保存记录**: 更新历史记录并归档数据

## 🔍 查看执行历史

1. 访问 `Actions` 页面
2. 查看所有执行记录
3. 点击任意记录查看详细日志
4. 下载归档的数据文件(可选)

## ⚙️ 自定义配置

### 修改执行时间

编辑 `.github/workflows/daily-crawl.yml` 文件:

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # 修改这一行
```

Cron表达式格式: `分钟 小时 日 月 星期`

示例:
- `0 1 * * *` - 每天UTC 1:00 (北京时间9:00)
- `0 13 * * *` - 每天UTC 13:00 (北京时间21:00)
- `0 */6 * * *` - 每6小时执行一次

### 修改推送文章数量

编辑 `discord_sender.py` 文件:

```python
send_daily_report_to_discord(webhook_url, top_n=10)  # 修改top_n参数
```

### 禁用AI处理(节省成本)

编辑 `.github/workflows/daily-crawl.yml`,修改数据处理步骤:

```yaml
- name: Process data without AI
  run: |
    python data_processor.py --no-ai
```

## 🔒 安全注意事项

1. **永远不要**将Webhook URL或API密钥直接写入代码
2. **始终使用**GitHub Secrets存储敏感信息
3. **定期检查**Actions执行日志,确保没有泄露敏感信息
4. **及时更新**依赖库,修复安全漏洞

## 🐛 故障排查

### 工作流执行失败

1. 查看Actions页面的错误日志
2. 检查Secrets是否正确配置
3. 确认Discord Webhook URL有效
4. 验证OpenAI API密钥有效且有余额

### Discord没有收到消息

1. 检查Webhook URL是否正确
2. 确认Discord频道权限设置
3. 查看Actions日志中的Discord推送步骤

### AI处理失败

1. 检查OpenAI API密钥是否有效
2. 确认API账户有足够余额
3. 可以临时禁用AI处理: `python data_processor.py --no-ai`

## 💡 高级功能

### 同时发送邮件

如果您想在推送Discord的同时也发送邮件,可以在工作流中添加邮件步骤。但由于Gmail MCP工具需要交互式认证,建议使用SMTP方式发送邮件。

### 数据持久化

当前配置会将历史记录提交回GitHub仓库。如果您不希望这样,可以删除工作流中的 "Commit history" 步骤。

### 多频道推送

如果您想推送到多个Discord频道,可以添加多个Webhook URL到Secrets,并在工作流中多次调用discord_sender.py。

## 📞 获取帮助

如果遇到问题,请:
1. 查看GitHub Actions执行日志
2. 检查本文档的故障排查部分
3. 在GitHub仓库提交Issue

---

**祝您使用愉快!** 🎉
