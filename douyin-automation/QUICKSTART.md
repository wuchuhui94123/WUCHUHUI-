# ⚡ 快速开始

5 分钟快速上手抖音自动化脚本！

## 🚀 三步启动

### 1️⃣ 准备环境（首次）

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化 uiautomator2
python -m uiautomator2 init
```

### 2️⃣ 启动模拟器

- 打开雷电模拟器（或其他 Android 模拟器）
- 在模拟器中打开抖音并登录
- 确保抖音在首页

### 3️⃣ 运行脚本

#### Windows 用户
```bash
# 双击 start.bat
# 或在命令行运行：
python main.py
```

#### Linux/Mac 用户
```bash
# 运行启动脚本
./start.sh

# 或直接运行
python3 main.py
```

## 🎮 运行模式

| 命令 | 说明 |
|------|------|
| `python main.py` | 默认：刷视频 + 看直播 |
| `python main.py --mode video` | 仅刷视频 |
| `python main.py --mode live` | 仅看直播 |
| `python main.py --debug` | 调试模式 |

## ⚙️ 快速配置

编辑 `config/config.yaml`：

```yaml
# 模拟器端口（根据你的模拟器选择）
adb:
  device_id: "127.0.0.1:5555"  # 雷电
  # device_id: "127.0.0.1:62001"  # 夜神
  # device_id: "127.0.0.1:7555"   # MuMu

# 运行时长
video:
  duration: 300  # 刷视频 5 分钟

live:
  duration: 600  # 看直播 10 分钟

# 互动频率（0-1）
video:
  like_probability: 0.3    # 30% 点赞
  comment_probability: 0.1  # 10% 评论
```

## 🔍 检查连接

```bash
# 查看已连接设备
adb devices

# 如果没有设备，手动连接
adb connect 127.0.0.1:5555
```

## 📊 查看日志

```bash
# 日志文件位置
logs/douyin_bot_*.log

# 或使用调试模式查看实时日志
python main.py --debug
```

## ❓ 常见问题

### 连接失败？
```bash
# 重启 ADB
adb kill-server
adb start-server
adb connect 127.0.0.1:5555
```

### 找不到抖音？
- 确认模拟器中已安装抖音
- 检查包名是否正确

### 操作没反应？
```bash
# 重新初始化
python -m uiautomator2 init
```

## 📖 详细文档

- [完整安装指南](INSTALL.md)
- [详细使用说明](README.md)

## ⚠️ 注意事项

1. **建议使用测试账号**，避免主账号被限制
2. **不要长时间连续运行**，每天使用 1-2 小时即可
3. **调整互动频率**，降低被检测风险
4. **定期手动操作**，保持账号正常活跃度

## 🎯 推荐配置

**保守模式**（安全）：
```yaml
video:
  duration: 180           # 3 分钟
  like_probability: 0.2   # 20% 点赞
  comment_probability: 0.05  # 5% 评论

safety:
  max_continuous_actions: 30  # 30 个视频后休息
  rest_duration: 120     # 休息 2 分钟
```

**正常模式**（推荐）：
```yaml
video:
  duration: 300           # 5 分钟
  like_probability: 0.3   # 30% 点赞
  comment_probability: 0.1   # 10% 评论

safety:
  max_continuous_actions: 50  # 50 个视频后休息
  rest_duration: 60      # 休息 1 分钟
```

**激进模式**（高风险）：
```yaml
video:
  duration: 600           # 10 分钟
  like_probability: 0.5   # 50% 点赞
  comment_probability: 0.2   # 20% 评论

safety:
  max_continuous_actions: 100  # 100 个视频后休息
  rest_duration: 30       # 休息 30 秒
```

## 🛡️ 安全建议

✅ **推荐做法**：
- 使用小号测试
- 每天运行 1-2 次
- 每次运行 5-15 分钟
- 混合手动和自动操作
- 定期更换评论内容

❌ **避免做法**：
- 24 小时不间断运行
- 在主账号上使用
- 过高的互动频率
- 重复相同的评论
- 异常时间段运行（凌晨）

---

**准备好了吗？开始你的抖音自动化之旅！** 🚀
