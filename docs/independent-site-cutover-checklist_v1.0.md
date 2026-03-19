# 独立站点切换检查清单 v1.0

## 1. 服务器准备

- 已准备独立服务器或 VPS。
- 已创建部署用户，例如 `deploy`。
- 已将部署用户 SSH 公钥写入 `authorized_keys`。
- 已执行 `scripts/deploy/bootstrap_independent_site.sh`。
- Web Server 根目录已指向 `/var/www/kevin-blog/current`。

## 2. 域名与证书

- 已准备独立域名，例如 `blog.example.com`。
- DNS 已指向独立服务器公网 IP。
- HTTP 已可访问。
- HTTPS 证书已签发并续期策略已确认。

## 3. 仓库配置

### Variables

- `INDEPENDENT_SITE_BASE_URL`
- `INDEPENDENT_SITE_HOST`
- `INDEPENDENT_SITE_USER`
- `INDEPENDENT_SITE_PORT`
- `INDEPENDENT_SITE_PATH`

### Secrets

- `INDEPENDENT_SITE_SSH_KEY`

## 4. 首次发布验证

- 手动触发 `Deploy blog to independent site` workflow。
- 构建阶段成功。
- 部署阶段成功。
- 服务器上已生成 `releases/<release_id>/`。
- `current` 软链接已切到新版本。

## 5. 线上验证

- 首页可打开。
- 任意文章页可打开。
- CSS / JS / 图片资源加载正常。
- 中文页面编码正常。
- RSS、`sitemap.xml`、`404` 页面正常。
- 手机端和桌面端都能访问。

## 6. 切换到私有仓库前

- 新站点已稳定运行至少数次发布。
- 已验证回滚步骤可执行。
- `baseURL` 已切到独立域名。
- 已确认不再依赖 GitHub Pages 子域名。
- 再决定关闭 GitHub Pages 和私有化源码仓库。
