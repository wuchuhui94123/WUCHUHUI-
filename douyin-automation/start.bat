@echo off
chcp 65001 >nul
title 抖音自动化脚本

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║           🎬 抖音自动化脚本 Douyin Bot 🎬                  ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo [1] 刷视频 + 看直播（默认）
echo [2] 仅刷视频
echo [3] 仅看直播
echo [4] 调试模式
echo [5] 退出
echo.

set /p choice=请选择运行模式 [1-5]:

if "%choice%"=="1" (
    echo.
    echo 启动：刷视频 + 看直播模式
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo 启动：仅刷视频模式
    python main.py --mode video
) else if "%choice%"=="3" (
    echo.
    echo 启动：仅看直播模式
    python main.py --mode live
) else if "%choice%"=="4" (
    echo.
    echo 启动：调试模式
    python main.py --debug
) else if "%choice%"=="5" (
    exit
) else (
    echo.
    echo 无效选择，启动默认模式
    python main.py
)

echo.
pause
