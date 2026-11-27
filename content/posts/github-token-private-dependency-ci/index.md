---
title: "CI 怎么安全地读另一个私有仓库：细粒度令牌、仓库密钥与构建密钥"
date: 2026-11-27T20:24:55+08:00
draft: false
tags: ["工程实践", "自动化", "教程", "GitHubActions", "安全"]
categories: ["技术"]
author: "Kevin"
description: "核心代码放在一个私有仓库里，被多个项目按版本引用。这时 CI 要怎么拿到它？本文讲清细粒度个人访问令牌、Actions 仓库密钥和 Docker BuildKit secret 三者如何配合，以及几个常见场景的做法和坑。"
---

> 把核心代码单独放进私有仓库是好习惯，但从那一刻起，你的 CI 就多了一个问题：它凭什么能读那个仓库？

## 先讲结论

1. **CI 自带的 `GITHUB_TOKEN` 只对运行它的那个仓库有效。**要读另一个私有仓库，必须另配一把钥匙，最常用的是**细粒度个人访问令牌**（fine-grained personal access token，下文简称 PAT）。
2. **钥匙要放进保险箱，不能写进代码。**PAT 存成仓库的 **Actions secret**，运行时由 GitHub 注入，网页上看不到值，日志里自动打码。
3. **构建 Docker 镜像时用 BuildKit secret 传令牌**，令牌只在一个构建步骤里存在，不会留在任何镜像层里。用 `ARG`、`ENV` 或写 git 配置文件都会留下痕迹。

---

## 一、问题从哪来：私有依赖

很多团队会这样组织代码：

- 一个私有仓库 `private-lib`，放核心算法、公共组件或内部 SDK，按版本打 tag，比如 `v1.2.0`；
- 若干业务仓库，比如 `app-repo`，在依赖清单里按 tag 引用它。

以 Python 的 uv 为例，`pyproject.toml` 里会写：

```toml
[tool.uv.sources]
# 按 tag 引用私有仓库里的子包。注意：这里的地址不带任何凭据
private-lib = { git = "https://github.com/example-org/private-lib", tag = "v1.2.0" }
```

在自己电脑上，这毫无问题：git 用的是你本机登录过的凭据，你有权读 `private-lib`，`uv sync` 就能装上。

但到了 CI 上，代码在 GitHub 的服务器上运行。那台机器上没有你的登录状态，它只有 GitHub 每次运行自动发的一张临时通行证：`GITHUB_TOKEN`。而这张通行证有一条硬限制：**只能访问运行它的那个仓库**。

于是 CI 在“安装依赖”这一步失败，报错通常是 `Repository not found` 或 `Authentication failed`。仓库明明存在，只是 CI 没有权限看见它。

把依赖代码复制进业务仓库可以绕开这个问题，但那等于放弃了“单一来源、按版本引用”的初衷：同一份代码出现多个副本，改一处忘一处。正确的做法是给 CI 一把**只开这一扇门**的钥匙。

---

## 二、三个角色：通行证、钥匙和保险箱

![CI 访问另一个私有仓库：两种令牌的权限范围](imgs/01.jpg)

整个机制里有三个角色，各管一件事。

| 角色 | 是什么 | 谁签发 | 能访问什么 | 有效期 |
|------|--------|--------|------------|--------|
| `GITHUB_TOKEN` | 每次工作流运行自动生成的令牌 | GitHub | 只有当前仓库 | 这次运行结束即失效 |
| 细粒度 PAT | 你用自己账号签发的令牌 | 你 | 你勾选的仓库、你勾选的权限 | 你设定的到期日 |
| Actions secret | 仓库里的加密变量 | 你存进去 | 本身不是权限，只负责保管 | 一直保存，直到你覆盖或删除 |

### 细粒度 PAT：只开一扇门的钥匙

经典 PAT 的问题是权限太粗：勾一个 `repo`，就能读写你账号下**所有**私有仓库。细粒度 PAT 把范围收到了仓库和权限两个维度：

- **Repository access** 选 *Only select repositories*，只勾 `private-lib`；
- **Permissions** 里只把 *Contents* 设为 *Read-only*，*Metadata* 会自动带上只读，其余一概不开；
- **Expiration** 设一个到期日，到期自动作废。

生成后你会得到一串以 `github_pat_` 开头的字符，**它只显示这一次**。谁拿到这串字符，谁就拥有上面这点权限，所以它应该直接进入下一个角色：保险箱。

### Actions secret：保险箱

在 `app-repo` 的 *Settings → Secrets and variables → Actions* 里新建一条 repository secret，比如叫 `LIB_READ_TOKEN`，值就是刚才那串字符。它有几个特性：

- **写入后不可读**：网页上再也看不到它的值，包括你自己，只能覆盖或删除；
- **运行时注入**：工作流里通过 `${{ secrets.LIB_READ_TOKEN }}` 取用，通常再赋给一个环境变量；
- **日志自动打码**：这串字符如果出现在日志里，会显示成 `***`；
- **不给 fork**：从别人 fork 出去的仓库发来的 PR，默认拿不到这里的密钥，防止有人改工作流把它打印出去。

也可以用命令行存，交互式输入、不进 shell 历史：

```bash
gh secret set LIB_READ_TOKEN -R example-org/app-repo
```

> 每个仓库的 secret 是各存各的。两个仓库都要读 `private-lib`，就要在两边各存一次，值可以是同一个 PAT。组织账号可以用 organization secret 一次授权给多个仓库。

---

## 三、一次 CI 运行里，令牌是怎么被用掉的

![一次 CI 运行里令牌怎么被用掉](imgs/02.jpg)

关键在于：**依赖清单和锁文件里只写不带凭据的地址，令牌只在运行时由 git 的地址改写规则补上。**

```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      # ① 不保留 checkout 留下的认证头，原因见下文
      - uses: actions/checkout@v4
        with:
          persist-credentials: false

      # ② 让 git 访问 private-lib 时自动带上令牌
      - name: 私有依赖的只读令牌
        env:
          TOKEN: ${{ secrets.LIB_READ_TOKEN }}
        run: |
          if [ -z "$TOKEN" ]; then
            echo "::error::缺少密钥 LIB_READ_TOKEN"   # 没配密钥时给出明确提示
            exit 1
          fi
          git config --global \
            "url.https://x-access-token:${TOKEN}@github.com/example-org/private-lib.insteadOf" \
            "https://github.com/example-org/private-lib"

      # ③ 照常安装依赖，uv/pip 底层调用 git 时就带上了令牌
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --locked
```

`insteadOf` 是 git 的一个老功能：遇到以某个前缀开头的地址，就替换成另一个前缀。这里把“裸地址”替换成“带令牌的地址”，而且**只对 `private-lib` 这一个仓库生效**，不影响其他 GitHub 访问。

这样做有三个好处：

1. 锁文件里的地址和开发者本机一致，不用为 CI 维护两套配置；
2. 令牌只存在于运行器的内存和临时的全局 git 配置里，运行结束机器就销毁了；
3. 换令牌只需更新 secret，代码一行不改。

### 一个隐蔽的坑：checkout 留下的认证头

`actions/checkout` 默认会把 `GITHUB_TOKEN` 写成一个 HTTP 认证头，作用于所有 `github.com` 的请求，方便后续步骤 `git push`。问题是**这个认证头的优先级高于地址里的凭据**，结果 git 访问 `private-lib` 时用的还是 `GITHUB_TOKEN`，照样 `Repository not found`。

解决办法就是上面第 ① 步的 `persist-credentials: false`。如果后续步骤确实需要用 `GITHUB_TOKEN` 推送，就显式地为那一步单独配置。

---

## 四、构建镜像：令牌只进一步，不进镜像

![BuildKit secret：令牌只进一步、不进镜像](imgs/03.jpg)

服务端项目通常还要打 Docker 镜像，镜像构建时同样要装 `private-lib`。这里最容易犯的错，是把令牌当成普通构建参数：

```dockerfile
# 错误示范：令牌会永久留在镜像里
ARG GH_TOKEN
RUN git config --global url."https://x-access-token:${GH_TOKEN}@github.com/".insteadOf "https://github.com/" \
 && pip install -r requirements.txt
```

问题有两处：

- `ARG` 的值会记录在镜像的构建历史里，`docker history --no-trunc` 就能看到；
- `git config --global` 把令牌写进了 `/root/.gitconfig`，这个文件就留在那一层里，拿到镜像的人都能读出来。

即使后面再 `RUN rm`，也只是在新的一层里“标记删除”，旧层里的内容依然在。

正确做法是 **BuildKit secret mount**：

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /app
COPY pyproject.toml uv.lock ./
# 密钥只挂在这一个 RUN 里：作为环境变量 GH_TOKEN 出现，步骤结束即消失。
# git 的改写规则也用环境变量 GIT_CONFIG_* 传，不写任何配置文件。
RUN --mount=type=secret,id=gh_token,env=GH_TOKEN,required=true \
    GIT_CONFIG_COUNT=1 \
    GIT_CONFIG_KEY_0="url.https://x-access-token:${GH_TOKEN}@github.com/example-org/private-lib.insteadOf" \
    GIT_CONFIG_VALUE_0="https://github.com/example-org/private-lib" \
    uv sync --locked --no-dev

# 多阶段：运行镜像只复制装好的依赖，不带 git、不带构建过程
FROM python:3.12-slim
COPY --from=build /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
```

构建时从外部传入：

```bash
# 本机：用自己的 gh 登录凭据
GH_TOKEN=$(gh auth token) docker buildx build --secret id=gh_token,env=GH_TOKEN -t app:dev .
```

在 GitHub Actions 里用 `docker/build-push-action`：

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    secrets: |
      gh_token=${{ secrets.LIB_READ_TOKEN }}
```

Docker Compose 也支持构建密钥：

```yaml
services:
  api:
    build:
      context: .
      secrets: [gh_token]
secrets:
  gh_token:
    environment: GH_TOKEN   # 从宿主机环境变量读取
```

### 怎么确认镜像里真的没有令牌

不要只凭“写法正确”就放心，构建完验证一遍：

```bash
# 1. 构建历史里不应出现令牌
docker history --no-trunc app:dev | grep -c "$GH_TOKEN"        # 应为 0

# 2. 以 root 扫一遍整个文件系统
docker run --rm -u 0 -e T="$GH_TOKEN" app:dev \
  sh -c 'grep -rlF "$T" / --exclude-dir=proc --exclude-dir=sys 2>/dev/null | head'   # 应无输出
```

---

## 五、几个典型场景

### 场景 1：多个服务共用一个私有算法库

算法库单独一个仓库、按 tag 发版，三四个服务按版本引用。每个服务仓库各存一条只读 secret（或用组织级 secret），CI 和镜像构建都按上面的方式取依赖。升级算法库时，只改服务仓库里的 tag 和锁文件，一目了然地知道哪个服务用的是哪个版本。

### 场景 2：私有 git 子模块

如果用的是 git submodule 而不是包管理器，可以直接把 PAT 交给 checkout：

```yaml
- uses: actions/checkout@v4
  with:
    submodules: true
    token: ${{ secrets.LIB_READ_TOKEN }}   # 用这个令牌拉主仓库和子模块
```

注意这时主仓库也是用这个 PAT 拉的，所以 PAT 要同时对主仓库有读权限，或者主仓库是公开的。

### 场景 3：CI 要写另一个仓库

比如源码仓库私有、安装包发布到一个公开的发布仓库（做法见 [源码私有、安装包公开](/posts/private-source-public-releases/)）。这时 PAT 的权限要开 *Contents: Read and write*，范围仍然只勾那一个发布仓库。**读和写最好用两个不同的令牌**，各自最小化。

### 场景 4：服务器拉私有镜像

镜像推到 GHCR 等私有镜像仓库后，服务器拉镜像也需要凭据。这是另一把钥匙：只给 `read:packages`。这样服务器上只有“拉镜像”的权限，**拿不到源码仓库**，即使服务器被攻破，泄露的也只是已经发布出去的镜像，而不是全部代码。

### 场景 5：团队或长期项目

PAT 是绑在**个人账号**上的：人离职、账号停用，所有依赖这个 PAT 的 CI 一起失败。团队项目更适合以下两种：

| 方式 | 适合 | 特点 |
|------|------|------|
| 部署密钥（deploy key） | 只读一个仓库的 SSH 访问 | 绑在仓库上不绑人；一把密钥只能用于一个仓库；要改用 SSH 地址 |
| GitHub App | 组织内长期自动化 | 不绑人，令牌按次签发、约 1 小时过期，权限可细到单仓库单权限；配置稍复杂 |
| 细粒度 PAT | 个人项目、小团队起步 | 配置最简单；绑人、有到期日，要记得续期 |

我的建议是：个人项目用细粒度 PAT 起步，等到有第二个人需要维护 CI，就换成 GitHub App。

---

## 六、日常运维：令牌的一生

令牌不是配好就忘的东西，至少要管住这几件事：

- **到期**：PAT 到期那天，CI 会在安装依赖这一步集体失败。在日历里提前一周提醒自己，新建令牌后覆盖 secret 即可，代码不用动。
- **吊销**：怀疑泄露、或者不再需要，立刻到 *Settings → Developer settings → Fine-grained tokens* 里吊销。吊销即时生效。
- **一个用途一个令牌**：不同项目、不同权限各用各的，命名写清用途，比如 `app-repo-ci-read-lib`。出问题时只需吊销一个，不会牵连其他。
- **不要发给任何人**：包括 AI 助手和同事。需要别人帮你配置时，让对方告诉你步骤，值由你自己粘贴进 secret。
- **提示要明确**：在工作流里检查 secret 是否为空，为空就输出一句能看懂的错误（上文第 ② 步），省得下一个人对着 `Repository not found` 猜半天。

SSH 密钥的管理思路和这里一样，也是“按用途分钥匙、权限给最小、随时可吊销”，可以对照 [SSH 密钥登录完全指南](/posts/ssh-key-login-config-guide/) 一起看。

---

## 总结

- `GITHUB_TOKEN` 只管自己的仓库；跨仓库读取需要另一把钥匙，个人项目最省事的是**细粒度 PAT**，只勾一个仓库、只开 Contents 只读、设到期日。
- 钥匙放进 **Actions secret**：写入后不可读、运行时注入、日志打码、fork 拿不到。
- 依赖清单只写裸地址，CI 里用 git 的 **`insteadOf`** 在运行时补上令牌；别忘了 `persist-credentials: false`。
- 镜像构建用 **BuildKit secret mount**，配合 `GIT_CONFIG_*` 环境变量和多阶段构建，令牌只活在一个 `RUN` 里；构建完用 `docker history` 和全盘扫描验证一次。
- 团队和长期项目，换成部署密钥或 GitHub App，避免把 CI 绑在某个人身上。

### 参考阅读

- GitHub Docs：Managing your personal access tokens（细粒度令牌的创建与权限说明）
- GitHub Docs：Using secrets in GitHub Actions
- GitHub Docs：Automatic token authentication（`GITHUB_TOKEN` 的权限范围）
- Docker Docs：Build secrets（`RUN --mount=type=secret` 与 `env=` 选项）
- Git 文档：`git config` 中 `url.<base>.insteadOf` 与 `GIT_CONFIG_COUNT` 环境变量
