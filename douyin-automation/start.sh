#!/bin/bash

# 抖音自动化脚本启动器

clear

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           🎬 抖音自动化脚本 Douyin Bot 🎬                  ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

echo "[1] 刷视频 + 看直播（默认）"
echo "[2] 仅刷视频"
echo "[3] 仅看直播"
echo "[4] 调试模式"
echo "[5] 退出"
echo ""

read -p "请选择运行模式 [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "启动：刷视频 + 看直播模式"
        python3 main.py
        ;;
    2)
        echo ""
        echo "启动：仅刷视频模式"
        python3 main.py --mode video
        ;;
    3)
        echo ""
        echo "启动：仅看直播模式"
        python3 main.py --mode live
        ;;
    4)
        echo ""
        echo "启动：调试模式"
        python3 main.py --debug
        ;;
    5)
        exit 0
        ;;
    *)
        echo ""
        echo "无效选择，启动默认模式"
        python3 main.py
        ;;
esac

echo ""
read -p "按回车键退出..."
