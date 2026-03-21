---
title: "Obsidian + Git 实现笔记自动同步"
date: 2026-03-03T00:00:00+08:00
draft: false
tags: ["Obsidian", "Git", "笔记同步", "效率工具"]
categories: ["技术"]
author: "Kevin"
description: "完成 GitHub 同步的完整配置指南"
---

> 本文介绍如何配置 Obsidian Git 插件，实现笔记的自动备份和同步

---

## 前置条件

- ✅ GitHub 私有仓库已创建
- ✅ 本地 Vault 已初始化并推送
- ✅ .gitignore 已配置完成

---

## 步骤 1：安装 Obsidian Git 插件

1. 打开 Obsidian
2. 点击左下角的 **设置**（齿轮图标）
3. 选择 **第三方插件**
4. 关闭 **安全模式**（点击开关）
5. 点击 **浏览** 按钮
6. 搜索 **"Git"**
7. 找到 **Obsidian Git**（作者：Vinadon）
8. 点击 **安装**
9. 安装完成后点击 **启用**

---

## 步骤 2：配置插件

1. 在设置中找到 **Obsidian Git**（在已安装插件列表中）
2. 点击打开配置页面

### 基础设置（必须）

```
Vault backup interval (minutes): 10
  └─ 每10分钟自动备份一次

Auto backup after file change: OFF
  └─ 文件更改后不立即备份（避免频繁提交）

Auto push: ON
  └─ 自动推送到 GitHub

Auto pull: ON
  └─ 自动拉取远程更新
```

### 启动/关闭设置

```
Pull on startup: ON
  └─ 启动 Obsidian 时拉取更新

Push on backup: ON
  └─ 备份时自动推送

Disable on mobile: OFF
  └─ 在移动端也启用（如果你用 iPhone/iPad）
```

### 提交设置

```
Commit message: vault backup: {{date}}
  └─ 或使用：{{hostname}}: {{numFiles}} files changed

Commit author:
  - author name: 你的名字
  - author email: 你的邮箱
```

---

## 步骤 3：测试同步

1. 在 Obsidian 中创建一个新笔记
2. 等待 10 分钟（或按 `Ctrl+P` 输入 `Git: Create backup`）
3. 检查 GitHub 仓库是否有新提交

---

## 多设备同步

### 场景：Mac + iPhone + iPad

**Mac（主力设备）**
- 完整编辑和创作
- 自动备份间隔：10 分钟

**iPhone/iPad（移动设备）**
- 查看和轻度编辑
- 自动备份间隔：30 分钟
- 注意：移动端 Git 功能有限，建议主要用来看

### 同步流程

1. **Mac 上编辑笔记**
2. **10分钟后自动备份到 GitHub**
3. **iPhone 打开 Obsidian**
4. **自动拉取最新笔记**
5. **在手机上查看**

---

## 常见问题

### Q1: 同步冲突怎么办？

**解决方案**：
1. Obsidian Git 会自动处理大部分冲突
2. 如果冲突严重，手动选择保留哪个版本
3. 建议：不要在两台设备上同时编辑同一篇笔记

### Q2: 移动端无法使用 Git？

**原因**：iOS 限制，无法运行完整的 Git 命令

**替代方案**：
- 使用 Working Copy（iOS Git 客户端）
- 或者只在移动端查看，编辑回 Mac 上进行

### Q3: 备份太频繁？

**调整**：
- 将 `Vault backup interval` 从 10 分钟改为 30 或 60 分钟
- 关闭 `Auto backup after file change`

### Q4: 如何查看历史版本？

**方法**：
1. 在 GitHub 仓库中查看提交历史
2. 或使用 Git 命令行：`git log` 和 `git show`

---

## 进阶配置

### 自定义 .gitignore

```gitignore
# 忽略 Obsidian 系统文件
.obsidian/workspace.json
.obsidian/workspaces.json

# 忽略个人配置
.obsidian/plugins/obsidian-git/data.json

# 忽略大文件
attachments/*.mp4
attachments/*.mov
```

### 使用 Git LFS（大文件存储）

如果笔记中包含大量图片：

```bash
# 安装 Git LFS
git lfs install

# 追踪图片文件
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.gif"
```

---

## 总结

通过 Obsidian + Git 的组合，你可以：

1. **自动备份** - 再也不怕笔记丢失
2. **版本历史** - 随时回滚到任意版本
3. **多设备同步** - Mac、iPhone、iPad 无缝切换
4. **免费私有** - GitHub 私有仓库完全免费

开始享受自动同步的便利吧！
