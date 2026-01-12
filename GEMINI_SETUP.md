# Google Gemini API 配置指南

本文档将指导您如何获取并配置Google Gemini API密钥,实现**免费的AI翻译和总结功能**!

## 🎉 为什么选择Gemini?

### 优势对比

| 特性 | Google Gemini | OpenAI GPT |
|------|---------------|------------|
| **免费额度** | ✅ 每天1500次请求 | ❌ 无免费额度 |
| **成本** | 🆓 完全免费(在免费额度内) | 💰 约$0.001/篇文章 |
| **速度** | ⚡ 非常快 | ⚡ 快 |
| **质量** | 🌟 优秀 | 🌟 优秀 |
| **中文支持** | ✅ 原生支持 | ✅ 支持 |

**结论**: 对于每天爬取60-100篇文章的需求,Gemini的免费额度完全够用!

---

## 📝 获取Gemini API密钥

### 步骤1: 访问Google AI Studio

打开浏览器,访问: https://makersuite.google.com/app/apikey

或者访问: https://aistudio.google.com/app/apikey

### 步骤2: 登录Google账号

使用您的Google账号登录(Gmail账号即可)。

### 步骤3: 创建API密钥

1. 点击页面上的 **"Create API Key"** 或 **"获取API密钥"** 按钮
2. 选择一个Google Cloud项目(如果没有,系统会自动创建一个)
3. 点击 **"Create API key in new project"**
4. 等待几秒钟,API密钥就生成了!

### 步骤4: 复制API密钥

API密钥格式类似: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

**重要**: 复制后请妥善保管,不要泄露给他人!

---

## ⚙️ 配置到爬虫系统

### 方法一: 使用FinalShell图形界面(最简单)

1. **在FinalShell右侧文件浏览器中**,找到 `tech-info-crawler` 目录
2. **双击 `config.env` 文件**
3. **在文件中添加**:
   ```bash
   GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```
4. **按 `Ctrl+S` 保存**

### 方法二: 使用命令行

```bash
# 进入项目目录
cd tech-info-crawler

# 编辑配置文件
nano config.env

# 添加以下内容:
GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# 保存: Ctrl+X, 然后按 Y, 最后按 Enter
```

### 完整配置示例

```bash
# Discord Webhook URL (必需)
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/1459794905290244290/mOx2EXSlaYBvZc-X9IzTNco4eh209n_prerjg7-6MPOTcfLYWpHG2m40c8ixs0DjsOsg"

# Google Gemini API Key (推荐)
GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

---

## 🧪 测试Gemini集成

### 1. 安装Gemini依赖

```bash
pip3 install google-generativeai
```

### 2. 测试运行

```bash
./run_daily.sh
```

### 3. 查看输出

您应该看到类似这样的输出:

```
🤖 使用 Google Gemini API
开始AI处理文章(翻译标题和生成中文摘要)...
处理进度: 1/60 - OpenAI Launches GPT-5 with Revolutionary...
处理进度: 2/60 - Google Announces Gemini 2.0...
...
✅ AI处理完成,共处理 60 篇文章
```

### 4. 检查Discord

您的Discord频道应该收到了带有**中文标题和中文摘要**的文章卡片!

---

## 📊 免费额度说明

### Gemini API免费限制

- **每分钟**: 15次请求
- **每天**: 1500次请求
- **每月**: 无限制(只要不超过每天限制)

### 我们的使用量

- **每天爬取**: 约60-100篇文章
- **每篇文章**: 1次API请求
- **每天总计**: 约60-100次请求

**结论**: 完全在免费额度内,不会产生任何费用! 🎉

---

## 🔄 Gemini vs OpenAI 切换

系统支持同时配置两个API,优先级如下:

1. **优先使用Gemini**: 如果配置了 `GEMINI_API_KEY`
2. **备用OpenAI**: 如果没有Gemini但配置了 `OPENAI_API_KEY`
3. **跳过AI**: 如果都没配置,使用原始英文内容

### 配置示例

```bash
# 同时配置两个(优先使用Gemini)
GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# 只配置Gemini(推荐)
GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# 只配置OpenAI
OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

---

## ❓ 常见问题

### Q1: Gemini API密钥在哪里获取?

访问 https://makersuite.google.com/app/apikey 或 https://aistudio.google.com/app/apikey

### Q2: Gemini真的免费吗?

是的!在免费额度内(每天1500次请求)完全免费,不需要绑定信用卡。

### Q3: 如果超过免费额度会怎样?

系统会返回错误,但不会扣费。您可以等到第二天额度重置后继续使用。

### Q4: Gemini的翻译质量如何?

非常好!Gemini 2.0对中文的支持非常出色,翻译质量和GPT-4相当。

### Q5: 可以同时使用Gemini和OpenAI吗?

可以!系统会优先使用Gemini,如果Gemini失败或超额度,会自动切换到OpenAI。

### Q6: 如何查看API使用量?

访问 https://console.cloud.google.com/apis/dashboard 查看详细的API使用统计。

---

## 🔒 安全建议

1. **不要分享API密钥**: API密钥是您的私人凭证,不要泄露给他人
2. **不要提交到Git**: `config.env` 已在 `.gitignore` 中,不会被提交
3. **定期检查使用量**: 确保没有异常的API调用

---

## 🎊 开始使用!

配置完成后,运行:

```bash
./run_daily.sh
```

享受**免费的AI翻译和中文摘要**吧! 🚀

---

**有问题?** 随时在GitHub提Issue或联系我!
