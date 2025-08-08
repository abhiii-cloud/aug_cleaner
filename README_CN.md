# Aug Cleaner

**简体中文 | [English](README.md)**

一个专注于隐私保护的工具，用于清除 Augment Code VSCode 扩展中的遥测和跟踪机制，同时保持完整功能。

## 项目概述

Aug Cleaner 是一个 Python 工具，通过修补 JavaScript 文件来移除 Augment Code VSCode 扩展中的遥测和跟踪机制。该工具将用户隐私放在首位，通过拦截数据收集来保护隐私，同时保持所有 AI 功能正常运行。

## 主要特性

- **完整隐私保护**：阻止所有遥测和跟踪 API 调用
- **会话匿名化**：为每个 API 调用生成随机会话 ID
- **用户代理隐藏**：移除用户代理信息以防止指纹识别
- **零性能影响**：直接源码级修补，无运行时开销
- **精准打击**：仅阻止跟踪，保留所有 AI 功能
- **使用简单**：一条命令即可修补任何 JavaScript 文件

## 快速开始

### 安装

```bash
git clone https://github.com/gmh5225/aug_cleaner.git
cd aug_cleaner
```

### 使用方法

```bash
# 直接修补 Augment 扩展文件
python aug_cleaner.py ~/.vscode/extensions/augment.vscode-augment-*/out/extension.js
```

工具会自动：
1. **创建备份**：自动创建 `extension_ori.js` 备份文件
2. **修补原文件**：直接修改原始 `extension.js` 文件
3. **启用隐私保护**：阻止所有遥测，保留 AI 功能

### 修补过程说明

- **创建备份**：`extension_ori.js`（保留原始文件）
- **修补文件**：`extension.js`（添加隐私保护）
- **安全检查**：如果备份存在或文件已修补会给出警告

## 工作原理

Aug Cleaner 的工作流程：

1. **定位目标函数**：在 JavaScript 文件中找到 `async callApi()` 方法
2. **注入隐私代码**：插入紧凑的隐私保护补丁
3. **阻止遥测**：拦截所有 `report-*` 和 `record-*` API 端点
4. **匿名化会话**：为每个 API 调用生成随机 UUID
5. **隐藏用户信息**：清除用户代理字符串

### 被阻止的内容

- `report-feature-vector` - 特征向量报告
- `report-error` - 错误报告
- `record-session-events` - 会话事件记录
- `record-request-events` - 请求事件记录
- `record-preference-sample` - 偏好采样
- 所有其他 `report-*` 和 `record-*` 端点

## 隐私保护

### 三重保护层

1. **遥测阻断**
   - 拦截所有跟踪 API 调用
   - 返回成功响应以维持功能
   - 零数据离开您的机器

2. **会话随机化**
   - 为每个 API 调用生成唯一会话 ID
   - 防止跨会话行为关联
   - 使用户跟踪变得不可能

3. **用户代理隐藏**
   - 移除系统指纹数据
   - 防止设备识别
   - 保持完全匿名

## 系统要求

- Python 3.6+
- 无需外部依赖

## 技术细节

### 补丁代码概览

注入的代码经过高度优化和压缩：

```javascript
// 拦截遥测调用
if (typeof s === "string" && (s.startsWith("report-") || s.startsWith("record-"))) { 
  return { success: true }; 
}

// 生成随机会话 ID
const chars = "0123456789abcdef"; 
let randSessionId = ""; 
for (let i = 0; i < 36; i++) { 
  randSessionId += i === 8 || i === 13 || i === 18 || i === 23 ? "-" : 
                   i === 14 ? "4" : 
                   i === 19 ? chars[8 + Math.floor(4 * Math.random())] : 
                   chars[Math.floor(16 * Math.random())]; 
}

// 应用隐私设置
this.sessionId = randSessionId;
this._userAgent = "";
```

### 为什么选择这种方法？

- **精准打击**：针对单一 API 入口点
- **100% 覆盖**：所有 HTTP 请求都通过 `callApi()`
- **代码最少**：约 15 行 vs 100+ 行的网络拦截
- **零性能影响**：无运行时开销
- **最大兼容性**：不干扰其他功能

## 重要说明

- **先备份**：修补前请务必备份原始文件
- **关闭自动更新**：在 VSCode 扩展管理中禁用 Augment Code 的自动更新，避免补丁被覆盖
- **扩展更新**：如果手动更新扩展，需要重新应用补丁
- **功能保留**：所有 AI 功能继续正常工作
- **隐私优先**：没有遥测数据离开您的机器

### 如何关闭自动更新

1. 打开 VSCode 扩展面板 (Ctrl+Shift+X)
2. 找到 Augment Code 扩展
3. 点击扩展右侧的齿轮图标
4. 选择 "禁用自动更新" 或 "Disable Auto Update"

## 贡献

欢迎贡献！请随时提交问题和拉取请求。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 为注重隐私的开发者而构建
- 受对透明 AI 工具需求的启发
- 致力于用户隐私和数据主权

---

**免责声明**：此工具仅用于教育和隐私保护目的。用户有责任遵守适用的服务条款和当地法律。
