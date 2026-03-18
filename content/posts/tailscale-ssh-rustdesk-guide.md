---
title: "Tailscale + SSH + RustDesk：打造零配置远程访问方案"
date: 2026-03-18T15:54:22+08:00
draft: false
tags: ["Tailscale", "SSH", "RustDesk", "远程访问", "WireGuard", "VPN"]
categories: ["工具"]
author: "Kevin"
description: "结合 Tailscale 组网、SSH 命令行和 RustDesk 远程桌面，实现零端口转发、端到端加密的远程访问方案"
---

> 本文介绍如何使用 Tailscale + SSH + RustDesk 三件套，实现无需公网 IP、无需端口转发、端到端加密的远程命令行与桌面访问方案。

---

## 为什么需要这套组合？

### 远程访问的常见痛点

| 痛点 | 传统方案 | 问题 |
|------|---------|------|
| **没有公网 IP** | 端口转发、DDNS | 路由器配置复杂，ISP 可能封端口 |
| **需要 CLI + GUI** | 分别配 VPN + SSH + VNC | 工具多、维护难、体验割裂 |
| **安全顾虑** | 暴露端口到公网 | 被扫描爆破，凭据泄露风险 |
| **跨平台访问** | 不同系统不同工具 | 体验不一致，学习成本高 |

### 这套方案的优势

> 核心思路：Tailscale 负责组网，SSH 负责命令行，RustDesk 负责远程桌面。各司其职，简单高效。

1. **零端口转发** - Tailscale 自动穿透 NAT，不需要碰路由器
2. **端到端加密** - 所有流量走 WireGuard 隧道，安全有保障
3. **CLI + GUI 全覆盖** - SSH 处理终端操作，RustDesk 处理图形界面
4. **全平台支持** - macOS、Linux、Windows、iOS、Android 全覆盖
5. **开源免费** - 三个工具个人使用均免费

---

## 三个工具分别是什么？

### Tailscale：零配置组网

把 Tailscale 想象成一根**虚拟网线**——它让你散布在各处的设备就像接在同一个交换机上一样，直接用内网 IP 互访。

**核心特点：**

- 基于 **WireGuard** 协议，性能好、延迟低
- **Mesh 组网**，设备之间直连（P2P），不经过中心服务器
- 每台设备自动分配一个稳定的 `100.x.x.x` 内网 IP
- 支持 **MagicDNS**，用设备名直接访问（如 `my-desktop`）
- 免费版支持最多 100 台设备，个人使用完全够

### SSH：命令行远程控制

SSH 是 Linux/macOS 世界的标配远程工具，不多介绍。在这套方案中，SSH 的角色是：

- 安全加密的终端访问通道
- 支持密钥认证，告别密码
- 文件传输（`scp`/`sftp`）、端口转发等附加能力
- 轻量级，几乎零资源开销

### RustDesk：开源远程桌面

RustDesk 是 TeamViewer/AnyDesk 的开源替代品，用 Rust 编写，支持自建中继服务器。

| 对比项 | TeamViewer | AnyDesk | RustDesk |
|--------|-----------|---------|----------|
| 开源 | ❌ | ❌ | ✅ |
| 自建服务器 | ❌ | ❌ | ✅ |
| 数据隐私 | 经第三方服务器 | 经第三方服务器 | 可完全自控 |
| 免费商用 | 受限 | 受限 | ✅ |
| 跨平台 | ✅ | ✅ | ✅ |

**核心优势**：支持自建中继服务器（hbbs/hbbr），数据不经过任何第三方，配合 Tailscale 使用安全性拉满。

---

## 架构原理：三者如何协同？

### 网络拓扑

```
                    Tailscale 虚拟网络 (100.x.x.x)
                    ┌─────────────────────────────┐
                    │                             │
┌──────────┐       │       ┌──────────────┐      │       ┌──────────┐
│  笔记本   │◄─────┼──────►│ RustDesk 中继 │◄────┼──────►│ 家里台式机│
│ 100.64.0.2│      │       │  100.64.0.10 │     │       │100.64.0.3│
└──────────┘       │       └──────────────┘     │       └──────────┘
     │              │                             │            │
     │              └─────────────────────────────┘            │
     │                                                         │
     ├── SSH (port 22) ──── 命令行访问 ────────────────────────┤
     └── RustDesk ───────── 远程桌面 ──────────────────────────┘
```

### 工作流程

1. 所有设备安装 Tailscale，加入同一个 **Tailnet**（虚拟局域网）
2. 每台设备获得一个稳定的 `100.x.x.x` 内网 IP 或 MagicDNS 主机名
3. SSH 连接走 Tailscale 隧道，**公网完全不暴露 22 端口**
4. RustDesk 中继服务器部署在 Tailnet 内部，只有网络内的设备能访问
5. 所有流量经 WireGuard 加密，即使在公共 WiFi 下也安全

### 为什么不只用其中一个？

| 只用一个 | 缺什么 |
|---------|--------|
| **只用 Tailscale** | 只有网络层，没有终端和远程桌面 |
| **只用 SSH** | 需要公网 IP 或端口转发，没有 GUI |
| **只用 RustDesk** | 公共中继慢且隐私差，没有命令行 |

三者组合：Tailscale 解决网络，SSH 解决终端，RustDesk 解决桌面。**各管一层，互不干扰**。

---

## 实战部署：Tailscale

### 步骤 1：注册与安装

1. 访问 [tailscale.com](https://tailscale.com) 注册（支持 Google/Microsoft/GitHub 登录）
2. 在每台设备上安装：

```bash
# macOS
brew install tailscale

# Ubuntu/Debian
curl -fsSL https://tailscale.com/install.sh | sh

# Arch Linux
sudo pacman -S tailscale

# Windows
# 从 https://tailscale.com/download 下载安装包
```

### 步骤 2：启动与加入网络

```bash
# 启动 Tailscale 并登录（会打开浏览器认证）
sudo tailscale up

# 查看网络状态
tailscale status

# 查看本机 Tailscale IP
tailscale ip -4
```

执行 `tailscale status` 后，你会看到类似输出：

```
100.64.0.2    my-laptop    linux   active; direct
100.64.0.3    my-desktop   linux   active; direct
100.64.0.10   relay-server linux   active; relay
```

### 步骤 3：验证连通性

```bash
# 用 Tailscale IP 测试
ping 100.64.0.3

# 用 MagicDNS 主机名测试（更方便）
ping my-desktop
```

> MagicDNS 默认开启。如果 ping 主机名不通，在 Tailscale 管理后台检查 DNS 设置。

---

## 实战部署：SSH

### 步骤 1：启用 SSH 服务

```bash
# Ubuntu/Debian
sudo apt install openssh-server
sudo systemctl enable --now sshd

# macOS
# 系统设置 → 通用 → 共享 → 打开"远程登录"

# Windows (PowerShell 管理员)
Add-WindowsCapability -Online -Name OpenSSH.Server
Start-Service sshd
Set-Service -Name sshd -StartupType Automatic
```

### 步骤 2：配置密钥认证

```bash
# 生成密钥对（如果还没有）
ssh-keygen -t ed25519 -C "your-email@example.com"

# 将公钥复制到远程机器
ssh-copy-id user@100.64.0.3
# 或用 MagicDNS
ssh-copy-id user@my-desktop
```

### 步骤 3：配置 SSH Config

编辑 `~/.ssh/config`，让连接更方便：

```
Host desktop
    HostName my-desktop        # MagicDNS 主机名
    User kevin
    IdentityFile ~/.ssh/id_ed25519

Host relay
    HostName 100.64.0.10       # Tailscale IP
    User root
    IdentityFile ~/.ssh/id_ed25519
```

配置后直接 `ssh desktop` 即可连接，不用每次输 IP 和用户名。

### 步骤 4：安全加固

编辑 `/etc/ssh/sshd_config`：

```
PasswordAuthentication no      # 禁用密码登录
PermitRootLogin no             # 禁止 root SSH 登录
PubkeyAuthentication yes       # 确保密钥认证开启
```

修改后重启 SSH 服务：

```bash
sudo systemctl restart sshd
```

> 由于 SSH 只在 Tailscale 内网可达，攻击面已经很小。但密钥认证仍然推荐开启，作为纵深防御。

### 可选：Tailscale SSH

Tailscale 提供了内置的 SSH 功能，可以**完全省去管理 SSH 密钥的麻烦**：

```bash
# 在目标机器上启用 Tailscale SSH
sudo tailscale up --ssh
```

启用后，Tailscale 自动处理认证，你可以直接：

```bash
ssh my-desktop    # 无需手动配置密钥
```

认证基于 Tailscale 账号身份，而非 SSH 密钥。适合不想折腾密钥管理的场景。

---

## 实战部署：RustDesk

### 方案选择

| 方案 | 适合场景 | 说明 |
|------|---------|------|
| **公共中继** | 快速体验 | 使用 RustDesk 默认公共服务器，开箱即用 |
| **自建中继 + Tailscale** | 长期使用（推荐） | 在 Tailnet 内自建 hbbs/hbbr，隐私安全 |

### 步骤 1：安装 RustDesk 客户端

在需要远程控制和被控制的机器上都安装 RustDesk：

- **macOS**: `brew install --cask rustdesk`
- **Linux**: 从 [GitHub Releases](https://github.com/rustdesk/rustdesk/releases) 下载
- **Windows**: 从 [rustdesk.com](https://rustdesk.com) 下载安装包

### 步骤 2：自建中继服务器（推荐）

在 Tailnet 内的一台机器上用 Docker 部署：

```bash
# 创建数据目录
mkdir -p /opt/rustdesk-server

# 启动 hbbs（ID/Rendezvous 服务器）
docker run -d \
  --name hbbs \
  --restart always \
  -p 21115:21115 \
  -p 21116:21116 \
  -p 21116:21116/udp \
  -p 21118:21118 \
  -v /opt/rustdesk-server:/root \
  rustdesk/rustdesk-server hbbs

# 启动 hbbr（Relay 中继服务器）
docker run -d \
  --name hbbr \
  --restart always \
  -p 21117:21117 \
  -p 21119:21119 \
  -v /opt/rustdesk-server:/root \
  rustdesk/rustdesk-server hbbr
```

启动后查看公钥（客户端配置需要）：

```bash
cat /opt/rustdesk-server/id_ed25519.pub
```

### 步骤 3：配置客户端连接

在每台 RustDesk 客户端中：

1. 打开 RustDesk → **设置** → **网络**
2. 填写：
   - **ID 服务器**：`100.64.0.10`（中继服务器的 Tailscale IP）
   - **中继服务器**：`100.64.0.10`
   - **Key**：粘贴上一步获取的公钥
3. 保存后重启 RustDesk

> 由于中继服务器只监听 Tailscale IP，外部网络完全无法访问，安全性有保障。

### 步骤 4：测试连接

1. 在被控机器上记下 RustDesk **ID**
2. 在控制端输入该 ID 并连接
3. 输入被控端设置的密码，即可看到远程桌面

---

## 使用场景

### 场景一：在家访问公司电脑

两台机器都装好 Tailscale，通过内网互通：

- **查看日志、跑脚本** → `ssh office-pc`
- **需要看 IDE 或浏览器** → 打开 RustDesk 连接远程桌面
- 不需要公司 IT 开通 VPN，自己搞定

### 场景二：管理家里的 NAS/服务器

- **日常维护** → SSH 连进去装软件、看状态、改配置
- **偶尔需要 GUI** → RustDesk 看一下管理面板
- 出门在外也能随时访问，手机装个 Tailscale 就行

### 场景三：远程协助家人

- 帮家人电脑上装好 Tailscale + RustDesk
- 需要帮忙时，直接 RustDesk 远程操作
- 全程走加密隧道，不用担心数据安全

---

## 最佳实践

### 网络层（Tailscale）

- 开启 **MagicDNS**，用主机名替代 IP，方便记忆
- 配置 **ACL**（访问控制列表），限制设备间的访问权限
- 定期检查设备列表，移除不再使用的设备
- 启用 **密钥过期提醒**，到期前及时续期

### SSH 层

- **必须**使用密钥认证，禁用密码登录
- 善用 `~/.ssh/config`，给常用机器配别名
- 如果不想管理密钥，考虑 Tailscale SSH
- 需要传文件时用 `scp` 或 `rsync`（通过 Tailscale IP）

### RustDesk 层

- **强烈推荐**在 Tailnet 内自建中继服务器
- 给无人值守的机器设置**强密码**
- 开启**连接加密**
- 不用时关闭 RustDesk 服务，减少攻击面

### 安全建议

> 所有流量都走 Tailscale 的 WireGuard 隧道，公网不暴露任何端口。这是这套方案最大的安全优势。

- 定期更新三个工具到最新版本
- 在 Tailscale 管理后台开启**设备审批**，新设备加入需确认
- 定期审计已连接设备
- 不要在不信任的设备上登录你的 Tailscale 账号

---

## 与其他方案对比

| 特性 | Tailscale + SSH + RustDesk | frp/ngrok + SSH | TeamViewer | ZeroTier + VNC |
|------|--------------------------|-----------------|------------|----------------|
| 端口转发 | 不需要 | 需要 | 不需要 | 不需要 |
| 数据隐私 | 完全自控 | 取决于中继 | 经第三方 | 自控 |
| 开源 | 全部开源 | 部分 | ❌ | 部分 |
| CLI 访问 | SSH（原生） | SSH | ❌ | 需额外配置 |
| GUI 访问 | RustDesk | 需额外工具 | 内置 | VNC |
| 配置复杂度 | 低 | 中高 | 低 | 中 |
| 免费使用 | ✅（个人） | 受限 | 受限 | ✅（个人） |

### 选择建议

- **需要 CLI + GUI 且重视隐私** → Tailscale + SSH + RustDesk
- **已有公网 IP，只需命令行** → 直接 SSH
- **企业有现成 VPN** → 在现有 VPN 基础上加 RustDesk
- **非技术用户，只要远程桌面** → RustDesk 或 TeamViewer 单独使用

---

## 常见问题

### Q1: Tailscale 免费版够用吗？

免费版支持最多 **100 台设备、3 个用户**，个人和小团队完全够用。如果需要更多用户或企业功能（SSO、审计日志等），可以升级付费版。

### Q2: RustDesk 不自建中继也能用吗？

可以。RustDesk 默认使用公共中继服务器，开箱即用。但公共中继可能较慢，且数据经过第三方服务器。**长期使用建议自建**。

### Q3: 连接速度如何？

Tailscale 优先建立 P2P 直连（不经过中转），延迟和你直连差不多。SSH 本身极其轻量。RustDesk 的体验取决于网络带宽，在 Tailscale 直连下表现很好。

### Q4: 移动端怎么用？

- **Tailscale**：iOS/Android 都有官方 App
- **RustDesk**：iOS/Android 都有客户端
- **SSH**：Android 用 Termux，iOS 用 Blink Shell 等终端 App

### Q5: 和 WireGuard 直接搭建有什么区别？

Tailscale 是 WireGuard 的上层封装，省去了手动管理密钥、配置路由、处理 NAT 穿透等繁琐步骤。如果你熟悉 WireGuard 且设备不多，直接用 WireGuard 也可以，但 Tailscale 的体验好很多。

---

## 总结

通过 Tailscale + SSH + RustDesk 的组合，你可以：

1. **零端口转发** - Tailscale 自动穿透 NAT，不碰路由器
2. **端到端加密** - WireGuard 隧道保护所有流量
3. **CLI + GUI** - SSH 管终端，RustDesk 管桌面
4. **开源自主** - 三个工具都开源，数据完全自己掌控

告别端口转发和公网 IP 的烦恼，享受安全便捷的远程访问吧！

---

## 参考资源

- [Tailscale 官方文档](https://tailscale.com/kb)
- [Tailscale SSH 文档](https://tailscale.com/kb/1193/tailscale-ssh)
- [RustDesk GitHub 仓库](https://github.com/rustdesk/rustdesk)
- [RustDesk 自建服务器指南](https://rustdesk.com/docs/en/self-host/)
- [WireGuard 协议官网](https://www.wireguard.com)

---

> 整理自官方文档和技术社区，如有遗漏或错误欢迎指正。
