# Kevin's Blog 维护手册

## 技术栈

- **静态站点生成器**: Hugo 0.157.0
- **主题**: Stack (git submodule, `themes/stack`)
- **托管**: GitHub Pages (自动部署)
- **仓库**: https://github.com/kevinalliswell/kevinalliswell.github.io
- **语言**: 简体中文 (zh-cn)，技术术语保留英文

## 目录结构

```
content/
├── posts/              # 手写文章（首页与归档只展示这里，保持清爽）
│   ├── *.md            # 手动撰写的文章
│   ├── work/           # 工作笔记
│   └── life/           # 生活随笔
├── news/               # 自动生成内容（独立 section，菜单「日报」入口 /news/）
│   ├── ai-digest-*.md      # AI 信息源日报
│   ├── github-hot-*.md     # GitHub 热榜
│   └── investment-brief-*.md  # 投资观察
├── about.md            # 关于页面
└── archives.md         # 归档页面
scripts/
└── generate_github_hot_digest.py  # GitHub 热榜生成脚本
```

## 文章规范

### Frontmatter 格式

```yaml
---
title: "文章标题"
date: 2026-03-18T20:00:00+08:00   # ISO 8601 + 东八区
draft: false
tags: ["标签1", "标签2"]
categories: ["分类"]
author: "Kevin"
description: "SEO 描述"
---
```

### 分类约定（每篇文章只归一类）

**手写文章**（首页/归档展示）：

| 分类 | 徽章色 | 用途 |
|------|--------|------|
| `["技术"]` | `#1d3461` | 技术教程、工具指南、深度解析、自动化 |
| `["思考"]` | `#6d597a` | 思维模型、方法论、认知随笔 |
| `["工作"]` | `#e76f51` | 项目实战、协作复盘、工作笔记 |
| `["生活"]` | `#457b9d` | 个人随笔、读书笔记 |

**自动内容**（写入 `content/news/`，菜单「日报」入口）：

| 分类 | 徽章色 | 来源 |
|------|--------|------|
| `["日报"]` | `#2a9d8f` | AI 信息源日报 |
| `["热点新闻"]` | `#c75146` | GitHub 热榜 |
| `["投资观察"]` | `#b08968` | 投资简报 |

> 分类配色定义在 `content/categories/<分类名>/_index.md`，`style.background` 为该分类的**基色**。
> 页面上徽章渲染为浅底 tint 胶囊：`custom.scss` 用 `color-mix` 从基色自动派生浅色/深色两态配色
> （details.html fork 只输出 `--cat-color` 变量），新增分类只需给一个基色即可。
> 布局约定：列表卡片不显示 tags（`showTags = false`），首页右栏无 tag-cloud widget（与分类云重复），
> 主题默认的 Google Fonts Lato 已用空 `layouts/_partials/head/custom-font.html` 覆盖移除。

### 文件命名

- 手动文章: `kebab-case.md`（如 `tailscale-ssh-rustdesk-guide.md`）
- 自动日报: `{type}-YYYY-MM-DD.md`（如 `github-hot-2026-03-21.md`）

### 写作风格

- 语言: 简体中文为主，技术术语保留英文
- 开头: blockquote 一句话总结
- 结构: `---` 分隔各大章节
- 善用: 表格对比、代码块（带注释）、blockquote 提示
- 结尾: 总结核心要点 + 参考资源链接

## 常用命令

```bash
# 本地预览
hugo server

# 构建（部署前验证）
hugo --gc --minify

# 新建文章
hugo new posts/my-new-post.md

# 部署（push 到 main 自动触发 GitHub Pages）
git add content/posts/xxx.md
git commit -m "feat: add xxx article"
git push origin main
```

## 图片生成（第三方中转 xingwan）

文章配图用 `kevin-blog-post` skill 调 `baoyu-image-gen`。本仓库配了一个第三方中转
（`xingwan.store`，OpenAI 兼容，借道 openai provider 的 `/v1/images/generations`），用包装脚本调用：

```bash
# 默认模型 gpt-image-2（该站当前唯一可用图像模型，已实测中文清晰）
.baoyu-skills/xingwan-gen.sh --prompt "..." --image out.png --ar 16:9
.baoyu-skills/xingwan-gen.sh --promptfiles p.md --image out.png --ar 16:9
```

要点：
- key 与端点写在 `.baoyu-skills/xingwan-gen.sh` 内（含密钥，已被 `.gitignore` 忽略，勿提交/分享）。
- **必须绕过本机代理**：本机 `127.0.0.1:7897` 代理对长连接有 ~20s 超时，而 gpt-image-2 出一张详细
  中文信息图约需 60~90s，走代理必被重置（表现为 `Error in the HTTP2 framing layer` / `socket closed` /
  `HTTP 000`）。包装脚本已 `unset HTTP(S)_PROXY` 并设 `NO_PROXY=xingwan.store`，**务必用包装脚本**，
  别直接 `bun main.ts`（会走代理而失败）。
- gpt-image-2 出图慢（约 60~90s/张），`--ar 16:9` 映射为 `1536x1024`，实测返回约 `1672x941`（≈16:9）横图。
- 中文渲染质量优秀（标题、表格、多行说明都清晰），且会自动补全合理内容，很适合信息图；比之前的
  gemini flash 更细致。
- 该站 `/v1/models` 目前只列出 `gpt-image-2` 一个模型；换模型用 `--model <id>`（需该站支持）。
- **不要**把 `OPENAI_*` 写进 `.baoyu-skills/.env`：脚本会先加载全局 `~/.baoyu-skills/.env` 且不覆盖，
  可能把真 OpenAI key 误发往第三方。务必用包装脚本（脚本里已 `export` 覆盖）。

## 自动化

- **GitHub Hot Digest**: 每日 UTC 23:00 自动运行 (`.github/workflows/github-hot-digest.yml`)
- **部署**: push 到 main 分支自动构建部署 (`.github/workflows/hugo.yml`)

## 维护检查清单

- [ ] Hugo 版本更新（当前 0.157.0，对比 https://github.com/gohugoio/hugo/releases）
- [ ] Stack 主题更新（`git submodule update --remote themes/stack`）
- [ ] 检查 GitHub Actions 运行状态
- [ ] 清理过期的自动生成内容（如有需要）
