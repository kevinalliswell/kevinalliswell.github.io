# Kevin's Blog 维护手册

## 技术栈

- **静态站点生成器**: Hugo 0.157.0
- **主题**: PaperMod (git submodule)
- **托管**: GitHub Pages (自动部署)
- **仓库**: https://github.com/kevinalliswell/kevinalliswell.github.io
- **语言**: 简体中文 (zh-cn)，技术术语保留英文

## 目录结构

```
content/
├── posts/              # 博客文章
│   ├── *.md            # 手动撰写的文章
│   ├── news/           # 自动生成的日报/热榜
│   ├── work/           # 工作笔记
│   └── life/           # 生活随笔
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

### 分类约定（共 4 个，每篇文章只归一类）

| 分类 | 用途 |
|------|------|
| `["技术"]` | 技术教程、工具指南、深度解析、自动化 |
| `["日报"]` | AI 日报、GitHub 热榜、投资晨报等每日汇总 |
| `["工作"]` | 项目实战、协作复盘、工作笔记 |
| `["生活"]` | 个人随笔、读书笔记 |

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

## 自动化

- **GitHub Hot Digest**: 每日 UTC 23:00 自动运行 (`.github/workflows/github-hot-digest.yml`)
- **部署**: push 到 main 分支自动构建部署 (`.github/workflows/hugo.yml`)

## 维护检查清单

- [ ] Hugo 版本更新（当前 0.157.0，对比 https://github.com/gohugoio/hugo/releases）
- [ ] PaperMod 主题更新（`git submodule update --remote themes/PaperMod`）
- [ ] 检查 GitHub Actions 运行状态
- [ ] 清理过期的自动生成内容（如有需要）
