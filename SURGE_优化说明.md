# Surge 配置优化说明 - Claude Code 连接稳定性专项优化

## 📋 优化概述

本次优化专门针对 **Claude Code 网页版连接断线问题**，已完成以下关键改进：

---

## ✅ 主要优化内容

### 1. **订阅地址更新**
- ✅ 已更新为新的机场订阅地址
- 📍 位置：`[Proxy Group]` → `📡 所有节点`
- 🔗 新地址：`https://45.137.181.25/api/getData/Authorize?token=4fdac984107929eae94d7e7322e611ec`

### 2. **Claude 专用策略优化** ⭐ 核心改进
```
🧠 Claude = url-test (自动测速选择最优美国节点)
```

**改进点：**
- 从手动 `select` 改为自动 `url-test`
- 仅选择美国节点（Claude 服务器位于美国）
- 每 5 分钟自动测速（interval=300）
- 容差 50ms，超时 3 秒
- 自动切换到最快节点，减少断线

### 3. **连接超时优化**
```
test-timeout = 10  # 从 5 秒增加到 10 秒
```
- 避免因网络波动导致的误判断线
- 给 Claude WebSocket 连接更多时间建立

### 4. **DNS 解析优化**
在 `[Host]` 部分添加 Claude 专用 DNS：
```
claude.ai = server:1.1.1.1
*.claude.ai = server:1.1.1.1
anthropic.com = server:1.1.1.1
*.anthropic.com = server:1.1.1.1
api.anthropic.com = server:1.1.1.1
*.claudeusercontent.com = server:1.1.1.1
```

**作用：**
- 使用 Cloudflare 1.1.1.1 解析（全球最快）
- 防止 DNS 污染导致连接失败
- 确保正确解析到 Claude 服务器

### 5. **规则优先级调整**
Claude 相关规则移到最顶部（最高优先级）：
```
# === Claude Code 专用规则（最高优先级）===
DOMAIN-SUFFIX,anthropic.com,🧠 Claude
DOMAIN-SUFFIX,claude.ai,🧠 Claude
DOMAIN,api.anthropic.com,🧠 Claude
DOMAIN-SUFFIX,claudeusercontent.com,🧠 Claude
DOMAIN-KEYWORD,anthropic,🧠 Claude
DOMAIN-KEYWORD,claude,🧠 Claude
```

**确保：**
- 所有 Claude 流量100%走专用策略
- 不会被其他规则误拦截
- WebSocket 连接稳定

### 6. **MITM 排除优化**
在 `hostname` 中完全排除 Claude 域名：
```
hostname = ..., -*.anthropic.com, -anthropic.com, -*.claude.ai, -claude.ai, -api.anthropic.com, -*.claudeusercontent.com
```

**重要性：**
- 保护 TLS 指纹完整性
- 避免 MITM 解密导致连接问题
- 确保 WebSocket 握手成功

### 7. **美国节点优化**
```
🇺🇸 美国节点 = url-test (自动测速)
```
- 改为 url-test 模式
- 每 10 分钟测速（interval=600）
- 为 Claude 提供最稳定的节点池

---

## 🚀 使用方法

### 步骤 1: 导入配置文件
1. 打开 Surge
2. 点击右上角 "+" → "从文件导入"
3. 选择 `surge_optimized.conf`
4. 或者直接复制配置内容到 Surge

### 步骤 2: 更新订阅节点
1. 打开 Surge
2. 进入"策略组"
3. 找到 **📡 所有节点**
4. 点击右侧刷新按钮 🔄
5. 等待节点更新完成（可能需要 10-30 秒）

⚠️ **注意：** 机场订阅链接 10 分钟后失效，如果无法更新请：
- 访问机场官网获取新链接
- 替换配置文件中的 `policy-path` 链接

### 步骤 3: 验证 Claude 策略
1. 进入"策略组"
2. 找到 **🧠 Claude**
3. 确认显示为 `url-test` 模式
4. 查看当前选中的节点（应该是美国节点）

### 步骤 4: 测试连接
1. 访问 https://claude.ai
2. 登录账号
3. 开始对话测试
4. 观察是否还有 "retry connection" 错误

---

## 🔍 故障排查

### 如果仍然出现断线：

#### 检查 1: 节点是否正常
```
策略组 → 🧠 Claude → 查看选中节点
策略组 → 🇺🇸 美国节点 → 手动测试各节点
```
- 如果所有美国节点都无法使用，联系机场客服
- 尝试手动切换到其他地区节点（新加坡、日本）

#### 检查 2: DNS 是否污染
在终端运行：
```bash
nslookup claude.ai 1.1.1.1
```
应该返回 Cloudflare IP（104.18.x.x）

#### 检查 3: 规则是否生效
```
Surge → 最近请求 → 搜索 "claude.ai"
```
查看是否走了 🧠 Claude 策略

#### 检查 4: MITM 是否干扰
```
Surge → MITM → 查看拦截域名
```
确保 `claude.ai` 和 `anthropic.com` **不在** MITM 列表中

---

## 📊 对比说明

### 优化前 vs 优化后

| 项目 | 优化前 | 优化后 | 改进 |
|-----|--------|--------|------|
| Claude 策略 | 手动 select | 自动 url-test | ✅ 自动选择最快节点 |
| 节点选择 | 全球节点 | 仅美国节点 | ✅ 减少跨区延迟 |
| 测速间隔 | 无 | 5分钟 | ✅ 持续监控节点质量 |
| 超时设置 | 5秒 | 10秒 | ✅ 减少误判 |
| DNS | 通用 DNS | Cloudflare 1.1.1.1 | ✅ 最快解析 |
| 规则优先级 | 普通 | 最高 | ✅ 100% 命中 |
| MITM | 可能解密 | 完全排除 | ✅ 保护连接 |

---

## ⚙️ 高级配置

### 如果还需要进一步优化：

#### 方案 A: 手动指定节点
如果某个美国节点特别稳定，可以改为手动模式：

```
🧠 Claude = select, 美国节点1, 美国节点2, 美国节点3
```

#### 方案 B: 调整测速参数
在 `🧠 Claude` 策略中调整：
- `interval=300` → 改为 `180`（3分钟测速一次，更频繁）
- `tolerance=50` → 改为 `30`（更敏感，快速切换）
- `timeout=3` → 改为 `5`（给节点更多时间）

#### 方案 C: 添加备用策略
创建备用 Claude 策略：
```
🧠 Claude备用 = select, 🇸🇬 新加坡节点, 🇯🇵 日本节点
```

---

## 📝 订阅更新说明

### 当前订阅地址：
```
https://45.137.181.25/api/getData/Authorize?token=4fdac984107929eae94d7e7322e611ec
```

### 更新步骤（订阅失效时）：

1. **获取新订阅链接**
   - 访问机场官网
   - 登录账号
   - 复制 Surge 订阅链接

2. **更新配置文件**
   - 打开 `surge_optimized.conf`
   - 找到 `📡 所有节点` 部分
   - 替换 `policy-path=` 后面的链接

3. **重新加载**
   - Surge → 策略组 → 📡 所有节点 → 刷新

---

## 🎯 核心原理

### 为什么会断线？

1. **节点不稳定**
   - Claude 服务器在美国
   - 使用其他地区节点延迟高、丢包多
   - WebSocket 长连接容易断开

2. **DNS 解析问题**
   - 国内 DNS 可能污染
   - 解析到错误的 IP
   - 导致连接失败

3. **MITM 干扰**
   - 中间人解密破坏 TLS 指纹
   - Claude 检测到异常拒绝连接

4. **规则不匹配**
   - 流量走了错误的策略
   - 被广告拦截误杀

### 本次优化如何解决？

✅ **自动选择最优美国节点** → 解决节点不稳定
✅ **专用 Cloudflare DNS** → 解决 DNS 污染
✅ **MITM 完全排除** → 解决 TLS 干扰
✅ **最高优先级规则** → 解决规则匹配

---

## 📞 技术支持

### 如果问题仍未解决：

1. **导出日志**
   ```
   Surge → 设置 → 日志级别 → verbose
   Surge → 最近请求 → 导出
   ```

2. **检查机场状态**
   - 访问机场官网
   - 查看是否有维护公告
   - 测试其他应用是否正常

3. **尝试备用方案**
   - 使用其他科学上网工具测试
   - 确认是配置问题还是机场问题

---

## 📌 重要提醒

1. ⏰ **订阅链接 10 分钟失效**
   - 请及时更新节点
   - 建议保存机场网站地址

2. 🔒 **保护个人信息**
   - 不要分享订阅链接
   - Token 是你的唯一凭证

3. 🔄 **定期更新配置**
   - Surge 规则集会更新
   - 建议每月重新下载一次

4. 💡 **合理使用**
   - 遵守当地法律法规
   - 不用于违法用途

---

## ✨ 配置文件位置

- **优化配置**: `surge_optimized.conf`
- **说明文档**: `SURGE_优化说明.md`

---

## 📄 版本信息

- **配置版本**: v2.0 (Claude Code 专项优化版)
- **优化日期**: 2025-11-12
- **适用平台**: Surge iOS / Surge Mac
- **核心改进**: Claude Code 连接稳定性

---

祝使用愉快！🎉
