# 独立站点发布链路设计 v1.0

## 1. 目标

- 博客源码仓库可切为私有。
- 博客站点继续公开访问。
- 内容仍然通过 `git push` 触发自动构建和发布。
- 发布链路不依赖 GitHub Pages，可迁移到独立服务器。

## 2. 推荐架构

```text
私有博客仓库
  └─ GitHub Actions
      ├─ checkout
      ├─ hugo build
      ├─ 打包 public/
      └─ 通过 SSH 发布到独立服务器
            ├─ releases/<release_id>/
            ├─ current -> releases/<release_id>
            └─ Web Server 指向 current
```

## 3. 为什么选这条链路

- 源码和草稿可保持私有。
- 独立服务器只接收静态产物，暴露面更小。
- 使用 `current` 软链接切换版本，回滚简单。
- 后续从单机迁到对象存储/CDN 时，构建侧基本不用重写。

## 4. 前置条件

### 4.1 独立站点地址

- 如果未来不再使用 GitHub Pages，就不能继续依赖 `kevinalliswell.github.io` 这个 GitHub 子域名。
- 推荐准备一个自有域名，例如 `blog.yourdomain.com` 或 `kevinalliswell.com`。
- Hugo 的 `baseURL` 需要切到你的独立站点域名。

### 4.2 服务器目录

推荐目录结构：

```text
/var/www/kevin-blog/
  ├─ current -> /var/www/kevin-blog/releases/20260319-abc1234
  └─ releases/
```

Web Server 根目录指向：

```text
/var/www/kevin-blog/current
```

### 4.3 仓库变量与密钥

在 GitHub 仓库中配置：

- `Variables`
- `INDEPENDENT_SITE_BASE_URL`
- `INDEPENDENT_SITE_HOST`
- `INDEPENDENT_SITE_USER`
- `INDEPENDENT_SITE_PORT`
- `INDEPENDENT_SITE_PATH`

在 GitHub 仓库中配置：

- `Secrets`
- `INDEPENDENT_SITE_SSH_KEY`

说明：

- `INDEPENDENT_SITE_BASE_URL`：例如 `https://blog.example.com`
- `INDEPENDENT_SITE_HOST`：服务器地址，例如 `1.2.3.4`
- `INDEPENDENT_SITE_USER`：部署用户，例如 `deploy`
- `INDEPENDENT_SITE_PORT`：SSH 端口，默认 `22`
- `INDEPENDENT_SITE_PATH`：远端发布目录，例如 `/var/www/kevin-blog`
- `INDEPENDENT_SITE_SSH_KEY`：仅用于部署的私钥

## 5. 发布流程

1. 向 `main` 推送文章或配置变更。
2. GitHub Actions 安装 Hugo 并构建 `public/`。
3. 工作流将 `public/` 打包为 `site.tar.gz`。
4. 工作流通过 SSH 将压缩包传到独立服务器。
5. 服务器解压到 `releases/<release_id>/`。
6. 服务器将 `current` 软链接切换到新版本。
7. 保留最近 5 个版本，旧版本自动清理。

## 6. 回滚方式

在服务器执行：

```bash
cd /var/www/kevin-blog
ls -1 releases
ln -sfn /var/www/kevin-blog/releases/<旧版本目录> current
```

回滚不需要重新构建。

## 7. 切换建议

### 阶段 1：平行验证

- 先保留现有 GitHub Pages 站点。
- 在新域名上部署独立站点。
- 连续验证几次发布、回滚、缓存刷新。

### 阶段 2：域名切换

- 将自有域名 DNS 切到独立服务器。
- 更新 `INDEPENDENT_SITE_BASE_URL`。
- 再执行一次正式发布。

### 阶段 3：仓库私有化

- 确认独立站点稳定。
- 关闭 GitHub Pages。
- 将博客源码仓库改为私有。

## 8. 当前分支内已提供的落地文件

- `.github/workflows/deploy-independent-site.yml`
- `scripts/deploy/deploy_independent_site.sh`
- `scripts/deploy/bootstrap_independent_site.sh`
- `scripts/deploy/examples/nginx-independent-site.conf.example`
- `docs/independent-site-cutover-checklist_v1.0.md`

当前已经具备：

- GitHub Actions 构建并 SSH 发布骨架
- 服务器目录初始化脚本
- Nginx 站点配置模板
- 切换前检查清单

后续只需补齐独立站点域名、服务器目录和部署密钥。
