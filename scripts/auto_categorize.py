#!/usr/bin/env python3
"""
自动为博客文章补全分类（categories）。

规则（按路径/文件名前缀匹配，先匹配先用）：
  content/news/ai-digest-*        → ["日报"]
  content/news/github-hot-*       → ["热点新闻"]
  content/news/investment-brief-* → ["投资观察"]
  content/posts/work/             → ["工作"]
  content/posts/life/             → ["生活"]
  content/posts/*.md（根目录）    → ["技术"]（默认）

只处理 categories 为空或缺失的文章，不会覆盖已有分类；
content/news/ 下的日报通常已由各自生成脚本写好分类，此处仅作兜底。
section/分类落地页（_index.md）会被跳过，避免被误加分类。
"""

import re
import sys
from pathlib import Path

# 路径/文件名前缀 → 分类 映射（dict 有序，靠前的优先匹配）
CATEGORY_RULES = {
    "content/news/ai-digest": '["日报"]',
    "content/news/github-hot": '["热点新闻"]',
    "content/news/investment-brief": '["投资观察"]',
    "content/posts/work/": '["工作"]',
    "content/posts/life/": '["生活"]',
}
DEFAULT_CATEGORY = '["技术"]'

# 扫描的内容目录
CONTENT_DIRS = ("content/posts", "content/news")

# 这些目录下的 markdown 是页面捆绑资源（配图提示词、大纲等），不是文章，跳过
SKIP_DIR_PARTS = {"imgs", "prompts"}


def detect_category(filepath: str) -> str:
    """根据文件路径/文件名确定分类。"""
    # 统一成正斜杠，保证 Windows / POSIX 下前缀匹配一致
    normalized = filepath.replace("\\", "/")
    for prefix, category in CATEGORY_RULES.items():
        if prefix in normalized:
            return category
    return DEFAULT_CATEGORY


def needs_category_fix(content: str) -> bool:
    """检查文章是否缺少分类或分类为空。"""
    # 提取 frontmatter
    match = re.match(r"^---\n(.*?\n)---", content, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)

    # 没有 categories 字段
    if not re.search(r"^categories:", frontmatter, re.MULTILINE):
        return True

    # categories 为空列表
    if re.search(r'^categories:\s*\[\s*\]\s*$', frontmatter, re.MULTILINE):
        return True

    return False


def fix_category(content: str, category: str) -> str:
    """补全或修复文章的分类。"""
    match = re.match(r"^---\n(.*?\n)---", content, re.DOTALL)
    if not match:
        return content

    frontmatter = match.group(1)

    if re.search(r"^categories:", frontmatter, re.MULTILINE):
        # 替换空分类
        new_frontmatter = re.sub(
            r'^categories:\s*\[\s*\]\s*\n',
            f'categories: {category}\n',
            frontmatter,
            flags=re.MULTILINE,
        )
    else:
        # 在 tags 后面插入 categories，如果没有 tags 则在 draft 后面
        if re.search(r"^tags:", frontmatter, re.MULTILINE):
            new_frontmatter = re.sub(
                r'^(tags:.*\n)',
                rf'\1categories: {category}\n',
                frontmatter,
                flags=re.MULTILINE,
            )
        else:
            new_frontmatter = re.sub(
                r'^(draft:.*\n)',
                rf'\1categories: {category}\n',
                frontmatter,
                flags=re.MULTILINE,
            )

    return content.replace(frontmatter, new_frontmatter, 1)


def main():
    fixed_files = []

    for base in CONTENT_DIRS:
        content_dir = Path(base)
        if not content_dir.exists():
            continue

        for md_file in content_dir.rglob("*.md"):
            # 跳过 section / 分类落地页
            if md_file.name == "_index.md":
                continue
            # 跳过页面捆绑里的资源型 markdown（imgs/ 配图提示词、大纲等）
            if SKIP_DIR_PARTS & set(md_file.parts):
                continue

            filepath = str(md_file)
            content = md_file.read_text(encoding="utf-8")

            if not needs_category_fix(content):
                continue

            category = detect_category(filepath)
            new_content = fix_category(content, category)

            if new_content != content:
                md_file.write_text(new_content, encoding="utf-8")
                fixed_files.append(f"  {filepath} → {category}")

    if fixed_files:
        print(f"Auto-categorized {len(fixed_files)} file(s):")
        for f in fixed_files:
            print(f)
    else:
        print("All posts already have categories, nothing to fix.")

    # 返回非零表示有修改（供 CI 判断是否需要 commit）
    sys.exit(0 if not fixed_files else 2)


if __name__ == "__main__":
    main()
