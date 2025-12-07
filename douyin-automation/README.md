# 🎬 抖音自动化脚本 Douyin Automation Bot

一个基于 Python + uiautomator2 的抖音自动化脚本，支持自动刷视频、观看直播、点赞、评论等功能。

## ⚠️ 免责声明

本项目仅供学习研究使用，请勿用于商业用途或违反抖音平台规则的行为。使用本脚本可能违反抖音的服务条款，造成的任何后果由使用者自行承担。

## ✨ 功能特性

### 视频功能
- ✅ 自动刷视频（上下滑动）
- ✅ 随机点赞
- ✅ 随机评论
- ✅ 随机分享/收藏
- ✅ 模拟真人观看时长

### 直播功能
- ✅ 自动进入直播间
- ✅ 随机点赞
- ✅ 发送弹幕评论
- ✅ 滚动查看评论区
- ✅ 自动切换直播间

### 防检测机制
- ✅ 随机化操作间隔
- ✅ 模拟人类操作延迟
- ✅ 随机坐标偏移
- ✅ 定期休息机制
- ✅ 多样化评论内容

## 📋 环境要求

### 系统要求
- Windows 10/11（推荐）
- Python 3.7+

### 软件要求
- Android 模拟器（推荐以下任一）：
  - [雷电模拟器](https://www.ldmnq.com/) - 默认端口 `127.0.0.1:5555`
  - [夜神模拟器](https://www.yeshen.com/) - 默认端口 `127.0.0.1:62001`
  - [MuMu模拟器](https://mumu.163.com/) - 默认端口 `127.0.0.1:7555`
  - [逍遥模拟器](https://www.xyaz.cn/) - 默认端口 `127.0.0.1:21503`

### 依赖库
```
uiautomator2>=2.16.23
PyYAML>=6.0
Pillow>=10.0.0
numpy>=1.24.0
opencv-python>=4.8.0
requests>=2.31.0
colorlog>=6.7.0
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd douyin-automation
pip install -r requirements.txt
```

### 2. 安装 ADB（如果未安装）

Windows 用户可以下载 [ADB 工具包](https://developer.android.com/studio/releases/platform-tools) 并添加到环境变量。

验证 ADB 安装：
```bash
adb version
```

### 3. 配置模拟器

#### 方案一：使用模拟器（推荐）

1. **安装并启动模拟器**
   - 下载并安装雷电/夜神/MuMu等模拟器
   - 启动模拟器

2. **在模拟器中安装抖音**
   - 打开模拟器自带的应用商店
   - 搜索"抖音"并安装
   - 登录你的抖音账号

3. **确认 ADB 连接**
   ```bash
   # 查看已连接的设备
   adb devices
   ```

   如果没有设备，需要手动连接：
   ```bash
   # 雷电模拟器
   adb connect 127.0.0.1:5555

   # 夜神模拟器
   adb connect 127.0.0.1:62001

   # MuMu模拟器
   adb connect 127.0.0.1:7555
   ```

4. **初始化 uiautomator2**
   ```bash
   python -m uiautomator2 init
   ```

#### 方案二：使用真机

1. 开启手机的 USB 调试模式
2. 用 USB 线连接电脑
3. 允许 USB 调试授权
4. 运行 `adb devices` 查看设备 ID

### 4. 修改配置文件

编辑 `config/config.yaml`：

```yaml
# 修改设备ID（根据你的模拟器）
adb:
  device_id: "127.0.0.1:5555"  # 雷电模拟器默认

# 调整运行参数
video:
  duration: 300  # 刷视频总时长（秒）
  watch_time_min: 10  # 每个视频最少观看时间
  watch_time_max: 30  # 每个视频最多观看时间
  like_probability: 0.3  # 点赞概率（0-1）

live:
  duration: 600  # 看直播总时长（秒）
  watch_time_min: 60  # 每个直播间最少观看时间
  watch_time_max: 300  # 每个直播间最多观看时间

# 自定义评论内容
comments:
  - "主播厉害👍"
  - "666"
  - "学到了"
  # 添加更多评论...
```

### 5. 运行脚本

```bash
# 方式1：刷视频 + 看直播（默认）
python main.py

# 方式2：仅刷视频
python main.py --mode video

# 方式3：仅看直播
python main.py --mode live

# 方式4：指定设备ID
python main.py --device 127.0.0.1:5555

# 方式5：启用调试模式
python main.py --debug
```

## 📖 使用说明

### 命令行参数

```
-m, --mode          运行模式：video/live/both（默认both）
-c, --config        配置文件路径（默认：config/config.yaml）
-d, --device        设备ID（覆盖配置文件）
--duration          运行时长（秒）
--debug             启用调试模式
```

### 配置说明

#### ADB 配置
```yaml
adb:
  device_id: "127.0.0.1:5555"  # 设备ID或IP:端口
```

#### 视频配置
```yaml
video:
  enabled: true              # 是否启用视频功能
  duration: 300              # 总运行时长（秒）
  watch_time_min: 10         # 每个视频最少观看时间（秒）
  watch_time_max: 30         # 每个视频最多观看时间（秒）
  like_probability: 0.3      # 点赞概率（0-1）
  comment_probability: 0.1   # 评论概率（0-1）
  share_probability: 0.05    # 分享概率（0-1）
```

#### 直播配置
```yaml
live:
  enabled: true              # 是否启用直播功能
  duration: 600              # 总运行时长（秒）
  watch_time_min: 60         # 每个直播间最少观看时间（秒）
  watch_time_max: 300        # 每个直播间最多观看时间（秒）
  like_probability: 0.5      # 点赞概率（0-1）
  comment_probability: 0.3   # 评论概率（0-1）
  gift_probability: 0.0      # 送礼概率（建议保持0）
```

#### 防检测配置
```yaml
randomization:
  swipe_duration_min: 300    # 滑动最短时间（毫秒）
  swipe_duration_max: 800    # 滑动最长时间（毫秒）
  action_interval_min: 1     # 操作间隔最小值（秒）
  action_interval_max: 5     # 操作间隔最大值（秒）
  human_like_delay: true     # 启用类人延迟

safety:
  max_continuous_actions: 50 # 最大连续操作次数
  rest_interval: 300         # 休息间隔（秒）
  rest_duration: 60          # 休息时长（秒）
```

## 🔧 常见问题

### 1. 设备连接失败
**问题**：`设备连接失败: Cannot connect to ...`

**解决方案**：
- 确认模拟器已启动
- 检查端口号是否正确
- 运行 `adb devices` 确认设备可见
- 尝试 `adb kill-server` 后再 `adb start-server`

### 2. 找不到抖音应用
**问题**：`启动抖音失败`

**解决方案**：
- 确认已在模拟器中安装抖音
- 检查包名是否正确（默认：`com.ss.android.ugc.aweme`）
- 可以运行 `adb shell pm list packages | grep douyin` 查看

### 3. 无法点击/滑动
**问题**：操作没有反应

**解决方案**：
- 运行 `python -m uiautomator2 init` 初始化
- 检查屏幕分辨率设置
- 确认模拟器开启了 USB 调试

### 4. 被检测为自动化
**问题**：账号被限制或提示异常

**解决方案**：
- 降低操作频率（减少 probability 值）
- 增加随机延迟时间
- 减少连续操作次数
- 使用小号测试

### 5. 导入错误
**问题**：`ModuleNotFoundError: No module named 'uiautomator2'`

**解决方案**：
```bash
pip install -r requirements.txt
```

## 🎯 最佳实践

### 1. 模拟真人操作
- 设置合理的观看时长（不要太短）
- 降低互动概率（不要每个视频都点赞）
- 增加随机性和延迟

### 2. 账号安全
- 建议使用小号测试
- 避免长时间连续运行
- 定期手动操作，保持账号活跃度

### 3. 性能优化
- 模拟器分配足够的内存（建议4GB+）
- 关闭不必要的后台应用
- 使用有线网络保证稳定性

### 4. 调试技巧
- 使用 `--debug` 参数查看详细日志
- 检查 `logs/` 目录下的日志文件
- 使用 `uiautomator2` 的 `app_current()` 查看当前应用信息

## 📁 项目结构

```
douyin-automation/
├── config/
│   └── config.yaml          # 配置文件
├── logs/                    # 日志目录（自动生成）
├── scripts/
│   ├── __init__.py
│   ├── video_bot.py         # 视频自动化脚本
│   └── live_bot.py          # 直播自动化脚本
├── utils/
│   ├── __init__.py
│   ├── logger.py            # 日志工具
│   ├── config_loader.py     # 配置加载器
│   ├── device_manager.py    # 设备管理器
│   └── anti_detection.py    # 防检测工具
├── main.py                  # 主程序
├── requirements.txt         # 依赖列表
└── README.md               # 说明文档
```

## 🔄 工作流程

### 视频模式
1. 连接设备并启动抖音
2. 随机观看视频（10-30秒）
3. 根据概率执行互动（点赞/评论/分享）
4. 滑动到下一个视频
5. 达到次数限制后休息
6. 重复直到达到设定时长

### 直播模式
1. 连接设备并启动抖音
2. 进入直播区域
3. 点击进入直播间
4. 观看直播（60-300秒）
5. 随机互动（点赞/评论）
6. 退出直播间，寻找下一个
7. 重复直到达到设定时长

## ⚙️ 技术栈

- **Python 3.7+**: 主要编程语言
- **uiautomator2**: Android 自动化框架
- **ADB**: Android 调试桥
- **PyYAML**: 配置文件解析
- **colorlog**: 彩色日志输出

## 📝 开发说明

### 添加新功能

1. 在 `scripts/` 目录下创建新的 bot 模块
2. 继承基本功能，实现特定逻辑
3. 在 `main.py` 中注册新模块
4. 更新 `config.yaml` 添加相关配置

### 调试技巧

```python
# 获取当前应用信息
d = u2.connect('127.0.0.1:5555')
print(d.app_current())

# 截图查看
d.screenshot('screenshot.png')

# 查看UI层级
d.dump_hierarchy()
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## ⚠️ 风险提示

1. **账号风险**：使用自动化脚本可能导致账号被限制或封禁
2. **违规风险**：可能违反抖音平台服务条款
3. **法律风险**：请确保使用行为符合当地法律法规

**建议**：
- 仅在测试账号上使用
- 不要用于商业目的
- 遵守平台规则
- 合理控制使用频率

## 📞 支持

如有问题，请提交 Issue 或查看文档。

---

**最后更新**: 2025-12-07

**祝使用愉快！**
