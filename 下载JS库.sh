#!/bin/bash

echo "================================================================"
echo "  集配计划管理系统 - JS库自动下载工具 (Linux/Mac)"
echo "================================================================"
echo ""

echo "正在下载 xlsx.full.min.js ..."
if curl -L "https://unpkg.com/xlsx@0.18.5/dist/xlsx.full.min.js" -o "xlsx.full.min.js" --fail --silent --show-error; then
    echo "[√] xlsx.full.min.js 下载成功"
else
    echo "[×] xlsx.full.min.js 下载失败，尝试备用地址..."
    curl -L "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js" -o "xlsx.full.min.js"
fi
echo ""

echo "正在下载 chart.min.js ..."
if curl -L "https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js" -o "chart.min.js" --fail --silent --show-error; then
    echo "[√] chart.min.js 下载成功"
else
    echo "[×] chart.min.js 下载失败，尝试备用地址..."
    curl -L "https://unpkg.com/chart.js@3.9.1/dist/chart.min.js" -o "chart.min.js"
fi
echo ""

echo "================================================================"
echo "下载完成！请检查文件大小："
ls -lh xlsx.full.min.js chart.min.js 2>/dev/null || echo "文件未找到"
echo ""
echo "参考大小："
echo "  - xlsx.full.min.js 应该约 720 KB"
echo "  - chart.min.js 应该约 220 KB"
echo ""
echo "如果文件很小（几十字节），说明下载失败，请检查网络"
echo "================================================================"
