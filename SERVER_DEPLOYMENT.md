# 服务器部署指南

本文档将指导您如何在自己的服务器上部署优质科技信息爬取系统。

## 📋 前置要求

### 服务器环境
- **操作系统**: Linux (Ubuntu 20.04+, CentOS 7+, Debian 10+等)
- **Python**: 3.10或更高版本
- **内存**: 至少512MB
- **磁盘**: 至少1GB可用空间
- **网络**: 能够访问外网(RSS源、Discord、OpenAI API)

### 必需的配置
- Discord Webhook URL
- OpenAI API Key (可选,用于AI翻译和总结)

## 🚀 快速部署

### 步骤1: 克隆仓库

```bash
# SSH方式
git clone git@github.com:Xiangyu-Li97/tech-info-crawler.git

# 或HTTPS方式
git clone https://github.com/Xiangyu-Li97/tech-info-crawler.git

# 进入项目目录
cd tech-info-crawler
```

### 步骤2: 安装依赖

```bash
# 安装Python依赖
pip3 install -r requirements.txt

# 或使用虚拟环境(推荐)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 步骤3: 配置系统

```bash
# 复制配置文件示例
cp config.env.example config.env

# 编辑配置文件
nano config.env  # 或使用 vim, vi 等编辑器
```

在 `config.env` 中填写:

```bash
# Discord Webhook URL (必需)
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# OpenAI API Key (可选)
OPENAI_API_KEY="sk-your-openai-api-key-here"
```

### 步骤4: 测试运行

```bash
# 手动执行一次完整流程
./run_daily.sh
```

执行成功后:
- 查看日志: `tail -f logs/crawler_YYYYMMDD.log`
- 检查Discord频道是否收到消息
- 确认数据文件已生成: `ls -lh processed_data_*.json`

### 步骤5: 配置定时任务

使用cron配置每天自动执行:

```bash
# 编辑crontab
crontab -e

# 添加以下行(每天早上9:00执行)
0 9 * * * /path/to/tech-info-crawler/run_daily.sh

# 保存并退出
```

**重要**: 将 `/path/to/tech-info-crawler` 替换为实际的项目路径。

查看完整路径:
```bash
cd tech-info-crawler
pwd
```

### 步骤6: 验证定时任务

```bash
# 查看已配置的定时任务
crontab -l

# 查看cron日志(Ubuntu/Debian)
grep CRON /var/log/syslog

# 查看cron日志(CentOS/RHEL)
grep CRON /var/log/cron
```

## 📊 Cron时间配置

### 常用时间示例

```bash
# 每天早上9:00
0 9 * * *

# 每天晚上21:00
0 21 * * *

# 每天早上9:00和晚上21:00
0 9,21 * * *

# 每6小时执行一次
0 */6 * * *

# 每周一早上9:00
0 9 * * 1

# 工作日(周一到周五)早上9:00
0 9 * * 1-5
```

### Cron表达式格式

```
分钟(0-59) 小时(0-23) 日(1-31) 月(1-12) 星期(0-6,0=周日)
```

## 🔧 高级配置

### 使用虚拟环境

推荐使用Python虚拟环境,避免依赖冲突:

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 虚拟环境会被 run_daily.sh 自动检测和激活
```

### 配置环境变量

如果不想使用 `config.env` 文件,可以在系统环境变量中配置:

```bash
# 编辑 ~/.bashrc 或 ~/.profile
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export OPENAI_API_KEY="sk-..."

# 重新加载配置
source ~/.bashrc
```

### 修改推送文章数量

编辑 `discord_sender.py`:

```python
# 找到这一行并修改 top_n 参数
send_daily_report_to_discord(webhook_url, top_n=20)  # 改为20篇
```

### 禁用AI处理(节省成本)

如果不需要AI翻译和总结:

1. 不配置 `OPENAI_API_KEY`
2. 或在 `run_daily.sh` 中强制禁用:
   ```bash
   python3 "$SCRIPT_DIR/data_processor.py" --no-ai
   ```

## 📝 日志管理

### 查看日志

```bash
# 查看今天的日志
tail -f logs/crawler_$(date +%Y%m%d).log

# 查看最近的日志
ls -lt logs/ | head -10

# 搜索错误信息
grep "错误\|失败\|Error" logs/crawler_*.log
```

### 日志自动清理

`run_daily.sh` 会自动清理7天前的日志和数据文件。

如需修改保留天数,编辑脚本中的这一行:

```bash
find "$SCRIPT_DIR/logs" -name "crawler_*.log" -mtime +7 -delete
# 将 +7 改为其他天数,如 +30 表示保留30天
```

## 🔒 安全建议

### 1. 保护配置文件

```bash
# 设置配置文件权限,只有所有者可读写
chmod 600 config.env

# 确保不会被Git跟踪
echo "config.env" >> .gitignore
```

### 2. 使用非root用户

不要使用root用户运行爬虫:

```bash
# 创建专用用户
sudo useradd -m -s /bin/bash crawler

# 切换到该用户
sudo su - crawler

# 在该用户下部署项目
```

### 3. 定期更新

```bash
# 定期拉取最新代码
cd tech-info-crawler
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade
```

## 🐛 故障排查

### 问题1: 脚本没有执行

**检查cron是否运行**:
```bash
sudo systemctl status cron  # Ubuntu/Debian
sudo systemctl status crond  # CentOS/RHEL
```

**检查脚本权限**:
```bash
ls -l run_daily.sh
# 应该显示 -rwxr-xr-x (可执行权限)
```

**检查cron日志**:
```bash
grep CRON /var/log/syslog  # Ubuntu/Debian
```

### 问题2: Discord推送失败

**检查网络连接**:
```bash
curl -I https://discord.com
```

**检查Webhook URL**:
```bash
# 手动测试Webhook
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content": "测试消息"}'
```

### 问题3: AI处理失败

**检查OpenAI API密钥**:
```bash
# 测试API密钥
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**检查API余额**:
访问 https://platform.openai.com/account/usage

### 问题4: Python依赖问题

**重新安装依赖**:
```bash
pip3 install -r requirements.txt --force-reinstall
```

**检查Python版本**:
```bash
python3 --version
# 应该是 3.10 或更高
```

## 📊 监控和告警

### 使用systemd服务(可选)

创建systemd服务文件:

```bash
sudo nano /etc/systemd/system/tech-crawler.service
```

内容:
```ini
[Unit]
Description=Tech Info Crawler Daily Job
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/tech-info-crawler
ExecStart=/path/to/tech-info-crawler/run_daily.sh

[Install]
WantedBy=multi-user.target
```

配置定时器:
```bash
sudo nano /etc/systemd/system/tech-crawler.timer
```

内容:
```ini
[Unit]
Description=Run Tech Crawler Daily at 9 AM

[Timer]
OnCalendar=09:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用:
```bash
sudo systemctl daemon-reload
sudo systemctl enable tech-crawler.timer
sudo systemctl start tech-crawler.timer
```

## 🔄 更新和维护

### 更新代码

```bash
cd tech-info-crawler
git pull origin main
pip install -r requirements.txt --upgrade
```

### 备份配置

```bash
# 备份配置文件
cp config.env config.env.backup

# 备份历史记录
cp crawled_history.json crawled_history.json.backup
```

### 清理数据

```bash
# 清理所有临时数据(保留历史记录)
rm -f crawled_data_*.json processed_data_*.json daily_report_*.md

# 清理所有日志
rm -f logs/*.log
```

## 📞 获取帮助

如果遇到问题:
1. 查看日志文件: `logs/crawler_YYYYMMDD.log`
2. 查看本文档的故障排查部分
3. 在GitHub仓库提交Issue: https://github.com/Xiangyu-Li97/tech-info-crawler/issues

---

**祝您部署顺利!** 🎉
