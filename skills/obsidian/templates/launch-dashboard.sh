#!/bin/bash
# 启动工作台 - 本地HTTP服务器 + 自动打开浏览器
# 用法: 双击运行 或终端执行 bash 启动工作台.sh
#
# 为什么需要这个脚本：
# 浏览器从 file:// 协议打开 HTML 时，会阻止 obsidian:// 自定义协议。
# 通过 localhost HTTP 服务后，obsidian:// 链接才能正常跳转。

PORT=8088
VAULT_DIR="/Users/wbaoc/Documents/Obsidian/wbaoc-wiki"

# 启动HTTP服务器（后台）
cd "$VAULT_DIR"
echo "🗺️ 启动工作台服务器 http://localhost:$PORT"
python3 -m http.server "$PORT" &>/dev/null &
SERVER_PID=$!

# 等服务器就绪
sleep 1

# 打开浏览器
open "http://localhost:$PORT/工作台.html"

echo "✅ 工作台已打开"
echo "   关闭终端或按 Ctrl+C 不会停止服务器"
echo "   要停止服务器: kill $SERVER_PID"
echo ""
echo "   服务器PID: $SERVER_PID"
echo "   停止命令: kill $SERVER_PID"
