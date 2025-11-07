@echo off
chcp 65001 >nul
echo ================================================================
echo   集配计划管理系统 - JS库自动下载工具 (Windows)
echo ================================================================
echo.
echo 正在下载 xlsx.full.min.js ...
powershell -Command "Invoke-WebRequest -Uri 'https://unpkg.com/xlsx@0.18.5/dist/xlsx.full.min.js' -OutFile 'xlsx.full.min.js'"
if exist xlsx.full.min.js (
    echo [√] xlsx.full.min.js 下载成功
) else (
    echo [×] xlsx.full.min.js 下载失败，请检查网络连接
)
echo.

echo 正在下载 chart.min.js ...
powershell -Command "Invoke-WebRequest -Uri 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js' -OutFile 'chart.min.js'"
if exist chart.min.js (
    echo [√] chart.min.js 下载成功
) else (
    echo [×] chart.min.js 下载失败，请检查网络连接
)
echo.

echo ================================================================
echo 下载完成！请检查文件大小：
echo   - xlsx.full.min.js 应该约 720 KB
echo   - chart.min.js 应该约 220 KB
echo.
echo 如果文件很小（几十字节），说明下载失败，请重新运行
echo ================================================================
echo.
pause
