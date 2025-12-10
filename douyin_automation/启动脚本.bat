@echo off
chcp 65001 >nul
title 抖音自动化脚本

echo ================================================
echo           抖音自动化脚本 v1.0
echo ================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] Python版本:
python --version
echo.

REM 检查ADB是否可用
adb version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到ADB工具
    echo 请确保已配置ADB路径或在config.json中指定完整路径
    echo.
)

REM 检查配置文件
if not exist config.json (
    echo [错误] 未找到config.json配置文件
    pause
    exit /b 1
)

REM 显示菜单
:menu
echo 请选择运行模式:
echo.
echo   1. 刷视频模式
echo   2. 看直播模式
echo   3. 混合模式 (刷视频+看直播)
echo   4. 测试连接
echo   5. 退出
echo.
set /p choice=请输入选择 (1-5):

if "%choice%"=="1" (
    echo.
    echo [启动] 刷视频模式...
    python douyin_bot.py video
    goto end
)

if "%choice%"=="2" (
    echo.
    echo [启动] 看直播模式...
    python douyin_bot.py live
    goto end
)

if "%choice%"=="3" (
    echo.
    echo [启动] 混合模式...
    python douyin_bot.py both
    goto end
)

if "%choice%"=="4" (
    echo.
    echo [测试] 正在测试ADB连接...
    adb devices
    echo.
    echo 如果上方显示了设备列表，说明连接正常
    echo.
    pause
    cls
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 再见！
    exit /b 0
)

echo [错误] 无效的选择，请重新输入
echo.
goto menu

:end
echo.
echo ================================================
echo           脚本执行完成
echo ================================================
pause
