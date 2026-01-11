#!/bin/bash

###############################################################################
# 优质科技信息爬取系统 - 每日执行脚本
# 
# 功能:
# 1. 爬取最新科技资讯
# 2. AI处理(翻译和总结)
# 3. 推送到Discord
# 
# 使用方法:
#   ./run_daily.sh
# 
# 配置文件:
#   config.env - 包含所有配置项(Discord Webhook, OpenAI API Key等)
###############################################################################

# 脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 日志文件
LOG_FILE="$SCRIPT_DIR/logs/crawler_$(date +%Y%m%d).log"
mkdir -p "$SCRIPT_DIR/logs"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始执行每日科技信息爬取任务"
log "=========================================="

# 加载配置文件
if [ -f "$SCRIPT_DIR/config.env" ]; then
    log "加载配置文件: config.env"
    source "$SCRIPT_DIR/config.env"
else
    log "错误: 配置文件 config.env 不存在"
    log "请复制 config.env.example 为 config.env 并填写配置"
    exit 1
fi

# 检查必需的配置
if [ -z "$DISCORD_WEBHOOK_URL" ]; then
    log "错误: DISCORD_WEBHOOK_URL 未配置"
    exit 1
fi

# 激活Python虚拟环境(如果存在)
if [ -d "$SCRIPT_DIR/venv" ]; then
    log "激活Python虚拟环境"
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# 步骤1: 爬取数据
log "步骤1: 开始爬取科技资讯..."
python3 "$SCRIPT_DIR/crawler.py" >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    log "✅ 爬取完成"
else
    log "❌ 爬取失败"
    exit 1
fi

# 步骤2: 处理数据
log "步骤2: 开始处理数据(AI翻译和总结)..."
if [ -n "$OPENAI_API_KEY" ]; then
    export OPENAI_API_KEY
    python3 "$SCRIPT_DIR/data_processor.py" >> "$LOG_FILE" 2>&1
else
    log "警告: OPENAI_API_KEY 未配置,跳过AI处理"
    python3 "$SCRIPT_DIR/data_processor.py" --no-ai >> "$LOG_FILE" 2>&1
fi

if [ $? -eq 0 ]; then
    log "✅ 数据处理完成"
else
    log "❌ 数据处理失败"
    exit 1
fi

# 步骤3: 推送到Discord
log "步骤3: 开始推送到Discord..."
python3 "$SCRIPT_DIR/discord_sender.py" "$DISCORD_WEBHOOK_URL" >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    log "✅ Discord推送完成"
else
    log "❌ Discord推送失败"
    exit 1
fi

# 清理旧日志(保留最近7天)
log "清理旧日志文件..."
find "$SCRIPT_DIR/logs" -name "crawler_*.log" -mtime +7 -delete

# 清理旧数据文件(保留最近7天)
log "清理旧数据文件..."
find "$SCRIPT_DIR" -name "crawled_data_*.json" -mtime +7 -delete
find "$SCRIPT_DIR" -name "processed_data_*.json" -mtime +7 -delete

log "=========================================="
log "每日科技信息爬取任务执行完成"
log "=========================================="

exit 0
