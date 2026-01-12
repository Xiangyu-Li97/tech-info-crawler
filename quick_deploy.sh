#!/bin/bash

###############################################################################
# 优质科技信息爬取系统 - 一键部署脚本
# 
# 功能:
# 1. 自动检测系统环境
# 2. 安装必要的依赖
# 3. 配置系统
# 4. 设置定时任务
# 
# 使用方法:
#   bash quick_deploy.sh
###############################################################################

set -e  # 遇到错误立即退出

echo "=========================================="
echo "优质科技信息爬取系统 - 一键部署"
echo "=========================================="
echo ""

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    echo "✅ 检测到操作系统: $PRETTY_NAME"
else
    echo "❌ 无法检测操作系统"
    exit 1
fi

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  建议使用root用户运行此脚本"
    echo "   如果遇到权限问题,请使用: sudo bash quick_deploy.sh"
    echo ""
fi

# 安装依赖
echo "步骤1: 安装系统依赖..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    apt update -qq
    apt install -y git python3-pip python3-venv > /dev/null 2>&1
    echo "✅ 依赖安装完成"
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    yum install -y git python3-pip > /dev/null 2>&1
    echo "✅ 依赖安装完成"
else
    echo "⚠️  未知的操作系统,请手动安装 git 和 python3-pip"
fi

# 获取当前目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 安装Python依赖
echo ""
echo "步骤2: 安装Python依赖..."
pip3 install -r requirements.txt -q
echo "✅ Python依赖安装完成"

# 创建配置文件
echo ""
echo "步骤3: 创建配置文件..."
if [ ! -f "config.env" ]; then
    cp config.env.example config.env
    echo "✅ 配置文件已创建: config.env"
    echo ""
    echo "⚠️  请编辑 config.env 文件,填写您的配置:"
    echo "   - DISCORD_WEBHOOK_URL (必需)"
    echo "   - OPENAI_API_KEY (可选)"
    echo ""
    echo "   编辑方法:"
    echo "   nano config.env"
    echo ""
    read -p "按回车键继续..." 
else
    echo "✅ 配置文件已存在"
fi

# 设置脚本权限
echo ""
echo "步骤4: 设置脚本权限..."
chmod +x run_daily.sh
echo "✅ 脚本权限设置完成"

# 测试运行
echo ""
echo "步骤5: 测试运行..."
read -p "是否现在测试运行一次? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./run_daily.sh
    echo ""
    echo "✅ 测试运行完成,请检查Discord频道是否收到消息"
fi

# 设置定时任务
echo ""
echo "步骤6: 设置定时任务..."
read -p "是否设置每天早上9:00自动执行? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 检查是否已经存在定时任务
    if crontab -l 2>/dev/null | grep -q "run_daily.sh"; then
        echo "⚠️  定时任务已存在,跳过设置"
    else
        # 添加定时任务
        (crontab -l 2>/dev/null; echo "0 9 * * * $SCRIPT_DIR/run_daily.sh") | crontab -
        echo "✅ 定时任务设置完成"
        echo ""
        echo "查看定时任务:"
        crontab -l | grep run_daily.sh
    fi
fi

# 完成
echo ""
echo "=========================================="
echo "🎉 部署完成!"
echo "=========================================="
echo ""
echo "📝 接下来的步骤:"
echo "   1. 编辑配置文件: nano config.env"
echo "   2. 手动测试运行: ./run_daily.sh"
echo "   3. 查看日志: tail -f logs/crawler_*.log"
echo ""
echo "📚 更多信息:"
echo "   - 详细文档: cat SERVER_DEPLOYMENT.md"
echo "   - FinalShell教程: cat FINALSHELL_DEPLOYMENT.md"
echo ""
echo "❓ 如有问题,请访问:"
echo "   https://github.com/Xiangyu-Li97/tech-info-crawler"
echo ""
