#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_SOURCE_LABEL = "GPT-5.3-codex"


def slugify(value: str) -> str:
    clean = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    while "--" in clean:
        clean = clean.replace("--", "-")
    return clean.strip("-") or "brief"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = ["date", "timezone", "title", "summary", "ideas"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")
    payload.setdefault("source_label", DEFAULT_SOURCE_LABEL)
    payload.setdefault("source_log", [])
    payload.setdefault("watchlist", [])
    payload.setdefault("market_snapshot", [])
    payload.setdefault("macro", {})
    return payload


def format_date_time(report_date: date) -> str:
    return datetime.combine(report_date, time(8, 10), SHANGHAI_TZ).isoformat()


def attachment_base(payload: dict[str, Any]) -> str:
    return (
        f"{payload['date']}-{slugify(payload['title'])}"
        f"-from-{slugify(payload.get('source_label', DEFAULT_SOURCE_LABEL))}"
    )


def render_source_links(sources: list[dict[str, str]]) -> str:
    links: list[str] = []
    for source in sources:
        title = source.get("title") or source.get("label") or "Source"
        url = source.get("url", "")
        publisher = source.get("publisher", "")
        label = f"{title}（{publisher}）" if publisher else title
        links.append(f"[{label}]({url})")
    return " · ".join(links) if links else "暂无新增一级来源。"


def render_bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def frontmatter_summary(summary: str) -> str:
    first_sentence = summary.split("。", 1)[0].strip()
    if first_sentence:
        return f"{first_sentence}。"
    return summary[:96].rstrip() + ("..." if len(summary) > 96 else "")


def render_blog_post(payload: dict[str, Any]) -> str:
    report_date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
    source_label = payload.get("source_label", DEFAULT_SOURCE_LABEL)
    summary = payload["summary"].strip()
    base_name = attachment_base(payload)
    research_json = f"{payload['date']}-{slugify(source_label)}-research.json"

    lines = [
        "---",
        f"title: {yaml_string(payload['title'])}",
        f"date: {yaml_string(format_date_time(report_date))}",
        "draft: false",
        'tags: ["投资", "晨报", "AI", "机器人", "能源", "黄金", "宏观", "监测版", "GPT-5.3-codex"]',
        'categories: ["投资观察"]',
        f"summary: {yaml_string(frontmatter_summary(summary))}",
        'author: "Kevin"',
        "---",
        "",
        f"# {payload['title']}",
        "",
        "> 自动化投资晨报，聚焦 AI、机器人、能源、黄金与相关宏观变量。以下为个人研究记录，不构成个性化投资建议。",
        "",
        "## 今日结论",
        "",
        summary,
        "",
    ]

    macro = payload.get("macro") or {}
    macro_bullets = macro.get("bullets") or []
    lines.extend(
        [
            "## 观察框架",
            "",
            f"- 宏观状态：{macro.get('regime', '暂无明确新增信号。')}",
            f"- 信息窗口：以 {payload['date']} Asia/Shanghai 早间监测为准，一级来源不足时回看最近 72 小时。",
            "- 处理方式：先看是否有新的一手披露，再决定是否改变仓位动作。",
        ]
    )
    if macro_bullets:
        lines.extend(["", "关键事实：", ""])
        lines.extend(render_bullets(macro_bullets))
    lines.append("")

    lines.extend(
        [
            "## 排序与动作",
            "",
            "| 排名 | 主题 | 资产 | 代码 | 评分 | 评级 | 动作 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for index, idea in enumerate(payload["ideas"], start=1):
        lines.append(
            "| {index} | {theme} | {asset} | {ticker} | {score} | {grade} | {action} |".format(
                index=index,
                theme=idea.get("theme", ""),
                asset=idea.get("asset", ""),
                ticker=idea.get("ticker", ""),
                score=idea.get("score", ""),
                grade=idea.get("grade", ""),
                action=idea.get("action", ""),
            )
        )
    lines.append("")

    lines.extend(["## 主题笔记", ""])
    for index, idea in enumerate(payload["ideas"], start=1):
        lines.extend(
            [
                f"### {index}. {idea.get('asset', '')}（{idea.get('ticker', '')}）",
                "",
                idea.get("thesis", "").strip(),
                "",
                f"- 当前动作：{idea.get('grade', '')} / {idea.get('action', '')} / {idea.get('score', '')} 分",
                f"- 为什么现在：{idea.get('why_now', '')}",
            ]
        )
        catalysts = idea.get("catalysts") or []
        risks = idea.get("risks") or []
        if catalysts:
            lines.extend(["", "后续催化：", ""])
            lines.extend(render_bullets(catalysts))
        if risks:
            lines.extend(["", "主要风险：", ""])
            lines.extend(render_bullets(risks))
        lines.append(f"- 一级来源：{render_source_links(idea.get('sources') or [])}")
        lines.append("")

    watchlist = payload.get("watchlist") or []
    if watchlist:
        lines.extend(["## 继续观察", ""])
        for item in watchlist:
            lines.append(
                "- {asset}（{ticker}）：{note}".format(
                    asset=item.get("asset", ""),
                    ticker=item.get("ticker", ""),
                    note=item.get("note", ""),
                )
            )
        lines.append("")

    stock_tracker = payload.get("stock_tracker")
    if stock_tracker is not False:
        tracker_html = (
            stock_tracker.get("html")
            if isinstance(stock_tracker, dict)
            else "/investment-briefs/stock-tracks/stock-history-tracker-latest.html"
        )
        tracker_md = (
            stock_tracker.get("markdown")
            if isinstance(stock_tracker, dict)
            else "/investment-briefs/stock-tracks/stock-history-tracker-latest.md"
        )
        tracker_json = (
            stock_tracker.get("json")
            if isinstance(stock_tracker, dict)
            else "/investment-briefs/stock-tracks/stock-history-tracker-latest.json"
        )
        lines.extend(
            [
                "## 指定股票曲线跟踪",
                "",
                "- 当前默认跟踪：圣泉集团（605589.SH）与 MLCC 主题篮子。",
                f"- [HTML 曲线面板]({tracker_html})",
                f"- [Markdown 摘要]({tracker_md})",
                f"- [结构化 JSON]({tracker_json})",
                "",
            ]
        )

    lines.extend(
        [
            "## 原始产物",
            "",
            f"- [Markdown 原稿](/investment-briefs/{base_name}.md)",
            f"- [HTML 面板](/investment-briefs/{base_name}.html)",
            f"- [研究 JSON](/investment-briefs/{research_json})",
            f"- [Obsidian 版本（静态镜像）](/investment-briefs/{base_name}.obsidian.md)",
            "",
        ]
    )

    source_log = payload.get("source_log") or []
    if source_log:
        lines.extend(["## 主要一级来源", ""])
        for source in source_log:
            lines.append(f"- [{source.get('label', 'Source')}]({source.get('url', '')})")
        lines.append("")

    lines.extend(
        [
            "## 说明",
            "",
            f"- 本文由 `{source_label}` 自动生成并发布。",
            "- 评分与动作是研究判断，不是交易指令；若没有个人持仓上下文，默认按组合通用视角处理。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        raise SystemExit(
            "Usage: render_investment_blog_post.py /path/to/research.json [output.md]"
        )

    input_path = Path(argv[1])
    payload = load_payload(input_path)
    output_path = (
        Path(argv[2])
        if len(argv) > 2
        else Path("content/news") / f"investment-brief-{payload['date']}-gpt-5-3-codex.md"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_blog_post(payload), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
