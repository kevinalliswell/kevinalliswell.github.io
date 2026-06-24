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

> 分类配色定义在 `content/categories/<分类名>/_index.md`。

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

## 图片生成（第三方中转 qhaigc）

文章配图默认用 `kevin-blog-post` skill 调 `baoyu-image-gen`。本仓库另配了一个第三方中转
（`api.qhaigc.net`，OpenAI 兼容，借道 openrouter provider），用包装脚本调用：

```bash
# 默认模型 gemini-2.5-flash-image（该站当前可用，已实测）
.baoyu-skills/qhaigc-gen.sh --prompt "..." --image out.png --ar 16:9
.baoyu-skills/qhaigc-gen.sh --promptfiles p.md --image out.png --ar 16:9

# 切换模型（如 3.1 恢复供货 / 其它可用模型）
.baoyu-skills/qhaigc-gen.sh --prompt "..." --image out.png \
    --model gemini-3.1-flash-image-preview --ar 16:9
# 其它同站可用模型：nano-banana-pro | seedream-5
```

要点：
- key 与端点写在 `.baoyu-skills/qhaigc-gen.sh` 内（含密钥，已被 `.gitignore` 忽略，勿提交/分享）。
- 该站模型名**不带 `google/` 前缀**（用裸名 `gemini-2.5-flash-image`）。
- `gemini-3.1-flash-image-preview` 该站常报 503「模型暂时不可用」，恢复供货后再用 `--model` 切回。
- 配套补丁：`~/.claude/skills/baoyu-image-gen/scripts/providers/openrouter.ts` 已扩展以解析该站
  「markdown 包裹 data URL」的响应（同目录有 `.bak` 备份可回滚）。
- **不要**把 `OPENROUTER_*` 写进 `.baoyu-skills/.env`：脚本会先加载全局 `~/.baoyu-skills/.env`
  且不覆盖，导致真 key 被误发往第三方。务必用包装脚本。

## 自动化

- **GitHub Hot Digest**: 每日 UTC 23:00 自动运行 (`.github/workflows/github-hot-digest.yml`)
- **部署**: push 到 main 分支自动构建部署 (`.github/workflows/hugo.yml`)

## 维护检查清单

- [ ] Hugo 版本更新（当前 0.157.0，对比 https://github.com/gohugoio/hugo/releases）
- [ ] Stack 主题更新（`git submodule update --remote themes/stack`）
- [ ] 检查 GitHub Actions 运行状态
- [ ] 清理过期的自动生成内容（如有需要）
