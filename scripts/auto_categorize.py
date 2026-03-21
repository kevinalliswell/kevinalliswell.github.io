#!/usr/bin/env python3
"""
自动为博客文章补全分类（categories）。

规则：
  content/posts/news/     → ["日报"]
  content/posts/work/     → ["工作"]
  content/posts/life/     → ["生活"]
  content/posts/*.md      → ["技术"]  (根目录默认)

只处理 categories 为空或缺失的文章，不会覆盖已有分类。
"""

import re
import sys
from pathlib import Path

# 路径 → 分类 映射
CATEGORY_RULES = {
    "content/posts/news/": '["日报"]',
    "content/posts/work/": '["工作"]',
    "content/posts/life/": '["生活"]',
}
DEFAULT_CATEGORY = '["技术"]'


def detect_category(filepath: str) -> str:
    """根据文件路径确定分类。"""
    for prefix, category in CATEGORY_RULES.items():
        if prefix in filepath:
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
    content_dir = Path("content/posts")
    if not content_dir.exists():
        print("content/posts not found, skipping.")
        return

    fixed_files = []

    for md_file in content_dir.rglob("*.md"):
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
