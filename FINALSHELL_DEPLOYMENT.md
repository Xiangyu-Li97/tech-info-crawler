# FinalShell + VPS 部署指南 (保姆级教程)

本文档将手把手教您如何使用FinalShell在您的VPS上部署优质科技信息爬取系统。每一步都有详细的截图说明和命令,您只需要跟着操作即可。

## 准备工作

在开始之前,请确保您已经准备好:

1. **一台VPS**: 已经购买并获得IP地址、用户名(通常是`root`)和密码。
2. **FinalShell**: 已经在您的电脑上安装好。
3. **Discord Webhook URL**: 已经创建好并复制。
4. **OpenAI API Key**: (可选)您的OpenAI API密钥。

---

## 步骤一: 连接到您的VPS

1. **打开FinalShell**, 点击左上角的"文件夹"图标,打开连接管理器。

2. **选择"SSH连接(Linux)"**, 然后点击"新建"按钮。

3. **填写连接信息**:
   - **名称**: 随意填写,例如 "我的VPS"
   - **主机**: 填写您的VPS IP地址
   - **端口**: 默认是 `22`
   - **认证方法**: 选择 "密码"
   - **用户名**: 填写您的VPS用户名 (通常是 `root`)
   - **密码**: 填写您的VPS密码

4. **点击"确定"保存**, 然后双击刚刚创建的连接,即可登录到您的VPS。

成功登录后,您会看到一个黑色的命令行窗口。

---

## 步骤二: 准备服务器环境

> 💡 **小提示**: 您可以直接复制下面的命令,在FinalShell的黑色窗口中右键粘贴,然后按回车执行。

### 1. 更新系统 (Ubuntu/Debian)

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. 安装必要工具 (Git 和 Pip)

```bash
sudo apt install git python3-pip -y
```

### 3. 验证安装

```bash
git --version
python3 --version
pip3 --version
```
如果都显示了版本号,说明环境准备好了!

---

## 步骤三: 部署爬虫项目

### 1. 克隆代码仓库

```bash
git clone https://github.com/Xiangyu-Li97/tech-info-crawler.git
```

### 2. 进入项目目录

```bash
cd tech-info-crawler
```

### 3. 安装Python依赖

```bash
pip3 install -r requirements.txt
```

> ⏳ 这一步可能需要几分钟,请耐心等待。

---

## 步骤四: 配置您的系统

### 1. 创建配置文件

```bash
cp config.env.example config.env
```

### 2. 编辑配置文件

您可以使用FinalShell的图形化界面来编辑文件,非常方便:

1. 在FinalShell的右侧文件浏览器中,导航到 `/root/tech-info-crawler` 目录。
2. **双击 `config.env` 文件**, FinalShell会自动打开一个文本编辑器。

在编辑器中,填写您的配置:

```bash
# Discord Webhook URL (必需)
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/1459794905290244290/mOx2EXSlaYBvZc-X9IzTNco4eh209n_prerjg7-6MPOTcfLYWpHG2m40c8ixs0DjsOsg"

# OpenAI API Key (可选)
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> 💡 **重要**: 将上面的URL和API Key替换为您自己的。

编辑完成后,按 `Ctrl + S` 保存,然后关闭编辑器。

---

## 步骤五: 测试运行

### 1. 手动执行一次

回到黑色的命令行窗口,执行下面的命令:

```bash
./run_daily.sh
```

### 2. 观察输出

您会看到类似下面的输出:

```
[2026-01-12 10:30:00] 开始执行每日科技信息爬取任务
[2026-01-12 10:30:00] 加载配置文件: config.env
[2026-01-12 10:30:00] 步骤1: 开始爬取科技资讯...
[2026-01-12 10:30:15] ✅ 爬取完成
[2026-01-12 10:30:15] 步骤2: 开始处理数据(AI翻译和总结)...
[2026-01-12 10:31:05] ✅ 数据处理完成
[2026-01-12 10:31:05] 步骤3: 开始推送到Discord...
[2026-01-12 10:31:10] ✅ Discord推送完成
[2026-01-12 10:31:10] 每日科技信息爬取任务执行完成
```

### 3. 检查Discord

同时,您的Discord频道应该已经收到了推送的消息!

如果一切正常,说明部署成功了! 🎉

---

## 步骤六: 设置定时任务 (每天自动运行)

### 1. 获取脚本的完整路径

```bash
pwd
```
您会得到类似 `/root/tech-info-crawler` 的路径,复制下来。

### 2. 编辑定时任务

```bash
crontab -e
```

第一次执行会让你选择编辑器,直接按回车选择 `nano` 即可。

### 3. 添加定时任务

在文件的最下方,添加一行:

```bash
0 9 * * * /root/tech-info-crawler/run_daily.sh
```

> 💡 **重要**: 将 `/root/tech-info-crawler` 替换为您上一步复制的实际路径。

这行代码的意思是: **每天早上9点**, 自动执行 `run_daily.sh` 脚本。

### 4. 保存并退出

- 按 `Ctrl + X`
- 按 `Y` 确认保存
- 按 `Enter` 退出

### 5. 验证定时任务

```bash
crontab -l
```
如果能看到您刚刚添加的那一行,说明定时任务设置成功了!

---

## 恭喜您! 🎉

您已经成功在您的VPS上部署了全自动的科技信息爬取系统! 从现在开始,它会每天早上9点自动为您抓取、分析并推送到您的Discord频道。

## 日常维护

### 查看日志

您可以使用FinalShell的文件浏览器,双击打开 `logs` 目录下的日志文件查看。

或者使用命令:
```bash
# 查看今天的实时日志
tail -f logs/crawler_$(date +%Y%m%d).log
```

### 更新项目

如果我想为您增加了新功能,您可以随时更新:

```bash
# 进入项目目录
cd tech-info-crawler

# 拉取最新代码
git pull origin main

# 更新依赖(如果需要)
pip3 install -r requirements.txt --upgrade
```

---

**祝您使用愉快! 如果遇到任何问题,随时可以问我!**
