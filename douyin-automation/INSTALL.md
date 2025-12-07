# 📦 安装指南

本文档详细介绍如何在 Windows 11 系统上安装和配置抖音自动化脚本。

## 📋 系统要求

- ✅ Windows 11（或 Windows 10）
- ✅ 至少 8GB 内存
- ✅ 20GB 可用磁盘空间
- ✅ 稳定的网络连接

## 🔧 安装步骤

### 步骤 1：安装 Python

1. **下载 Python**
   - 访问 [Python 官网](https://www.python.org/downloads/)
   - 下载 Python 3.8 或更高版本

2. **安装 Python**
   - 运行下载的安装程序
   - ⚠️ **重要**：勾选 "Add Python to PATH"
   - 点击 "Install Now"

3. **验证安装**
   ```bash
   # 打开命令提示符（Win+R，输入 cmd）
   python --version
   # 应该显示：Python 3.x.x
   ```

### 步骤 2：安装 Android 模拟器

#### 推荐：雷电模拟器（最稳定）

1. **下载雷电模拟器**
   - 访问 [雷电模拟器官网](https://www.ldmnq.com/)
   - 下载最新版本

2. **安装模拟器**
   - 运行安装程序
   - 按默认选项安装

3. **配置模拟器**
   - 启动雷电模拟器
   - 设置 → 性能设置：
     - CPU：4核
     - 内存：4096MB（4GB）
     - 分辨率：1080x1920（竖屏）
   - 重启模拟器使设置生效

4. **安装抖音**
   - 在模拟器中打开应用商店（如豌豆荚、应用宝）
   - 搜索"抖音"
   - 下载并安装
   - 登录你的抖音账号（建议使用测试账号）

#### 其他模拟器选择

| 模拟器 | 默认端口 | 优点 | 缺点 |
|--------|---------|------|------|
| 雷电模拟器 | 5555 | 稳定性好，兼容性强 | 占用资源较多 |
| 夜神模拟器 | 62001 | 轻量化，速度快 | 偶尔不稳定 |
| MuMu模拟器 | 7555 | 网易出品，优化好 | 广告较多 |
| 逍遥模拟器 | 21503 | 多开性能好 | 界面复杂 |

### 步骤 3：安装 ADB 工具

#### 方法一：使用模拟器自带的 ADB

大多数模拟器已经包含 ADB，可以直接使用：

```bash
# 雷电模拟器的 ADB 路径（根据实际安装路径调整）
cd "C:\LDPlayer\LDPlayer4.0"
adb.exe devices
```

#### 方法二：安装独立的 ADB 工具（推荐）

1. **下载 Platform Tools**
   - 访问 [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - 下载 Windows 版本

2. **解压并配置**
   ```bash
   # 解压到 C:\platform-tools
   # 添加到系统环境变量：
   # 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   # 在 Path 中添加：C:\platform-tools
   ```

3. **验证安装**
   ```bash
   adb version
   # 应该显示 ADB 版本信息
   ```

### 步骤 4：连接模拟器

1. **启动模拟器**
   - 打开雷电模拟器（或你选择的模拟器）

2. **连接 ADB**
   ```bash
   # 雷电模拟器
   adb connect 127.0.0.1:5555

   # 夜神模拟器
   adb connect 127.0.0.1:62001

   # MuMu模拟器
   adb connect 127.0.0.1:7555
   ```

3. **验证连接**
   ```bash
   adb devices
   # 应该显示：
   # List of devices attached
   # 127.0.0.1:5555    device
   ```

### 步骤 5：安装项目依赖

1. **下载项目**
   ```bash
   # 如果你有 git
   git clone <repository-url>

   # 或者直接下载 ZIP 并解压
   ```

2. **进入项目目录**
   ```bash
   cd douyin-automation
   ```

3. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

   如果下载速度慢，可以使用国内镜像：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. **初始化 uiautomator2**
   ```bash
   python -m uiautomator2 init
   ```

   这会在模拟器上安装必要的服务。

### 步骤 6：配置脚本

1. **编辑配置文件**
   - 打开 `config/config.yaml`
   - 修改设备 ID（如果使用雷电模拟器，默认配置已正确）

2. **自定义设置**
   ```yaml
   # 根据需要调整
   video:
     duration: 300  # 刷视频时长（秒）
     like_probability: 0.3  # 点赞概率

   live:
     duration: 600  # 看直播时长（秒）

   comments:
     - "你的自定义评论"
   ```

### 步骤 7：测试运行

1. **首次测试**
   ```bash
   python main.py --mode video --debug
   ```

   这会启动调试模式，只刷视频，便于观察。

2. **检查输出**
   - 观察命令行输出
   - 检查模拟器中的操作是否正常
   - 查看 `logs/` 目录下的日志文件

## ✅ 验证清单

在正式运行前，请确认以下项目：

- [ ] Python 已安装并添加到 PATH
- [ ] 模拟器已启动
- [ ] 模拟器中已安装并登录抖音
- [ ] ADB 可以连接到模拟器（`adb devices` 显示设备）
- [ ] Python 依赖已安装（`pip list` 可以看到 uiautomator2）
- [ ] uiautomator2 已初始化（模拟器中有 ATX 应用）
- [ ] 配置文件已根据需要修改
- [ ] 测试运行成功

## 🐛 常见安装问题

### 问题 1：Python 未添加到 PATH

**症状**：命令行运行 `python` 提示"不是内部或外部命令"

**解决**：
1. 找到 Python 安装目录（通常是 `C:\Users\用户名\AppData\Local\Programs\Python\Python3x`）
2. 手动添加到系统环境变量 PATH

### 问题 2：pip 安装依赖失败

**症状**：`pip install` 报错或超时

**解决**：
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者单独安装
pip install uiautomator2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 3：ADB 无法连接模拟器

**症状**：`adb devices` 显示空列表或 offline

**解决**：
```bash
# 重启 ADB 服务
adb kill-server
adb start-server

# 重新连接
adb connect 127.0.0.1:5555
```

### 问题 4：uiautomator2 初始化失败

**症状**：`python -m uiautomator2 init` 报错

**解决**：
1. 确认 ADB 已连接（`adb devices`）
2. 检查网络连接
3. 尝试手动安装 APK：
   ```bash
   # 下载并安装 app-uiautomator.apk 和 app-uiautomator-test.apk
   ```

### 问题 5：模拟器卡顿

**症状**：模拟器运行缓慢

**解决**：
1. 增加分配给模拟器的内存（推荐 4GB）
2. 启用 VT 虚拟化（进入 BIOS 开启）
3. 关闭其他占用内存的程序

### 问题 6：权限错误

**症状**：运行脚本时提示权限不足

**解决**：
```bash
# Windows：以管理员身份运行命令提示符

# 或者检查模拟器的开发者选项
# 设置 → 开发者选项 → USB 调试（开启）
```

## 🎯 下一步

安装完成后，可以：

1. 阅读 [README.md](README.md) 了解使用方法
2. 运行测试：`python main.py --debug`
3. 自定义配置：编辑 `config/config.yaml`
4. 查看日志：检查 `logs/` 目录

## 📞 获取帮助

如果遇到问题：

1. 检查本文档的"常见安装问题"部分
2. 查看项目的 README.md
3. 启用调试模式运行：`python main.py --debug`
4. 查看日志文件：`logs/douyin_bot_*.log`

---

**祝安装顺利！**
