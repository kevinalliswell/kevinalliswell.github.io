#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "data" / "ai_digest_sources.json"
DEFAULT_TIMEZONE = "Asia/Shanghai"
USER_AGENT = "Mozilla/5.0 (compatible; AIDigestBot/1.0; +https://kevinalliswell.github.io/)"
AI_KEYWORDS = {
    "agent",
    "ai",
    "anthropic",
    "chatgpt",
    "claude",
    "codex",
    "cursor",
    "gemini",
    "gpt",
    "llm",
    "openai",
    "人工智能",
    "大模型",
    "模型",
    "智能体",
}


@dataclass
class SourceConfig:
    name: str
    site_url: str
    feed_url: str
    mode: str
    category: str = "行业观察"
    include_keywords: list[str] = field(default_factory=list)


@dataclass
class Citation:
    title: str
    url: str


@dataclass
class CandidateItem:
    source_name: str
    source_category: str
    title: str
    url: str
    summary: str
    published_at: datetime
    citations: list[Citation]
    score: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the daily AI digest post.")
    parser.add_argument("publish_date", help="Target date for the output file, formatted as YYYY-MM-DD.")
    parser.add_argument("output_path", help="Markdown file to write.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--days", type=int, default=10)
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE)
    parser.add_argument("--title-prefix", default="AI 信息源日报")
    return parser.parse_args()


def load_sources(config_path: Path) -> list[SourceConfig]:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return [SourceConfig(**item) for item in raw["sources"]]


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_datetime(raw: str | None, tz: ZoneInfo) -> datetime:
    if not raw:
        return datetime.now(tz)
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(tz)


def strip_html(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def trim_summary(text: str, limit: int = 110) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.casefold()).strip()


def canonical_url(url: str) -> str:
    raw = (url or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    path = parts.path or ""
    if path.endswith("/") and path != "/":
        path = path[:-1]
    return urlunsplit((scheme, netloc, path, parts.query, ""))


def keyword_hits(text: str, extra_keywords: Iterable[str]) -> int:
    haystack = text.casefold()
    return sum(1 for keyword in set(extra_keywords) | AI_KEYWORDS if keyword.casefold() in haystack)


def base_score(published_at: datetime, text: str, extra_keywords: Iterable[str], now: datetime) -> float:
    age_days = max((now - published_at).total_seconds() / 86400, 0.0)
    return keyword_hits(text, extra_keywords) * 10.0 - age_days


def parse_feed_items(feed_xml: str, source: SourceConfig, tz: ZoneInfo, now: datetime) -> list[CandidateItem]:
    root = ET.fromstring(feed_xml)
    items: list[CandidateItem] = []
    for node in root.iter():
        if local_name(node.tag) not in {"item", "entry"}:
            continue
        entry = {local_name(child.tag): child for child in list(node)}
        title = (entry.get("title").text if entry.get("title") is not None else "").strip()
        link = entry.get("link")
        if link is not None and link.text:
            url = link.text.strip()
        elif link is not None and link.attrib.get("href"):
            url = link.attrib["href"].strip()
        else:
            url = ""
        description_node = entry.get("description")
        if description_node is None:
            description_node = entry.get("summary")
        description = description_node.text if description_node is not None and description_node.text else ""
        published = parse_datetime(
            (entry.get("pubDate").text if entry.get("pubDate") is not None else None)
            or (entry.get("published").text if entry.get("published") is not None else None)
            or (entry.get("updated").text if entry.get("updated") is not None else None),
            tz,
        )
        text_blob = f"{title} {description}"
        if source.include_keywords and keyword_hits(text_blob, source.include_keywords) == 0:
            continue
        items.append(
            CandidateItem(
                source_name=source.name,
                source_category=source.category,
                title=title,
                url=url,
                summary=trim_summary(strip_html(description)),
                published_at=published,
                citations=[Citation(title=source.name, url=url)],
                score=base_score(published, text_blob, source.include_keywords, now),
            )
        )
    return items


def extract_first_matching(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""


def parse_ai_digest_sections(
    feed_xml: str, source: SourceConfig, tz: ZoneInfo, now: datetime
) -> list[CandidateItem]:
    root = ET.fromstring(feed_xml)
    items: list[CandidateItem] = []
    for node in root.findall(".//item"):
        title = (node.findtext("title") or "").strip()
        url = (node.findtext("link") or "").strip()
        published = parse_datetime(node.findtext("pubDate"), tz)
        content_html = ""
        for child in list(node):
            if local_name(child.tag) == "encoded":
                content_html = child.text or ""
                break
        sections = re.findall(r"<h2>(.*?)</h2>\s*(.*?)(?=(?:<hr>\s*<h2>)|$)", content_html, flags=re.S)
        for raw_heading, raw_body in sections:
            heading = re.sub(r"^\d+\.\s*", "", strip_html(raw_heading))
            if heading == "快讯":
                continue
            importance = extract_first_matching(r"为什么重要：</strong>\s*(.*?)</p>", raw_body)
            paragraphs = re.findall(r"<p>(.*?)</p>", raw_body, flags=re.S)
            paragraph_texts: list[str] = []
            for paragraph in paragraphs:
                plain = strip_html(paragraph)
                if plain.startswith("Sources:") or "为什么重要：" in plain:
                    continue
                if plain:
                    paragraph_texts.append(plain)
            summary_source = importance or " ".join(paragraph_texts[:2])
            citations: list[Citation] = []
            blockquote = extract_first_matching(r"<blockquote>\s*<p>(.*?)</p>\s*</blockquote>", raw_body)
            for href, label in re.findall(r'<a href="(.*?)">(.*?)</a>', blockquote, flags=re.S):
                citations.append(Citation(title=strip_html(label), url=html.unescape(href)))
            items.append(
                CandidateItem(
                    source_name=source.name,
                    source_category=source.category,
                    title=heading,
                    url=url,
                    summary=trim_summary(summary_source),
                    published_at=published,
                    citations=citations or [Citation(title=source.name, url=url)],
                    score=base_score(published, f"{title} {heading} {summary_source}", source.include_keywords, now),
                )
            )
    return items


def collect_candidates(sources: list[SourceConfig], tz: ZoneInfo, now: datetime) -> list[CandidateItem]:
    candidates: list[CandidateItem] = []
    for source in sources:
        feed_xml = fetch_text(source.feed_url)
        if source.mode == "ai_digest_sections":
            candidates.extend(parse_ai_digest_sections(feed_xml, source, tz, now))
        else:
            candidates.extend(parse_feed_items(feed_xml, source, tz, now))
    return candidates


def extract_markdown_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text)]


def load_historical_citation_urls(posts_dir: Path, current_slug: str) -> set[str]:
    historical: set[str] = set()
    if not posts_dir.exists():
        return historical
    for post in posts_dir.glob("ai-digest-*.md"):
        if post.name == current_slug:
            continue
        try:
            content = post.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in content.splitlines():
            if not line.strip().startswith("- 引用来源："):
                continue
            for link in extract_markdown_links(line):
                normalized = canonical_url(link)
                if normalized:
                    historical.add(normalized)
    return historical


def select_items(
    candidates: list[CandidateItem],
    count: int,
    days: int,
    now: datetime,
    historical_citations: set[str],
) -> list[CandidateItem]:
    blocked_citations = set(historical_citations)
    cutoff = now - timedelta(days=days)
    filtered = [item for item in candidates if item.published_at >= cutoff]
    if len(filtered) < count:
        filtered = sorted(candidates, key=lambda item: (item.published_at, item.score), reverse=True)

    deduped: list[CandidateItem] = []
    seen_titles: set[str] = set()
    for item in filtered:
        title_key = normalize_title(item.title)
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        deduped.append(item)

    ranked = sorted(deduped, key=lambda item: (item.published_at, item.score), reverse=True)
    by_source: dict[str, list[CandidateItem]] = {}
    by_category: dict[str, list[CandidateItem]] = {}
    for item in ranked:
        by_source.setdefault(item.source_name, []).append(item)
        by_category.setdefault(item.source_category, []).append(item)

    selected: list[CandidateItem] = []
    selected_titles: set[str] = set()
    selected_source_urls: set[str] = set()
    selected_citation_urls: set[str] = set()

    def try_pick(item: CandidateItem) -> bool:
        title_key = normalize_title(item.title)
        if title_key in selected_titles:
            return False

        source_url_key = canonical_url(item.url)
        if source_url_key and source_url_key in selected_source_urls:
            return False

        remaining: list[Citation] = []
        for citation in item.citations:
            citation_key = canonical_url(citation.url)
            if not citation_key:
                continue
            if citation_key in blocked_citations or citation_key in selected_citation_urls:
                continue
            remaining.append(citation)
        if not remaining:
            return False

        selected.append(replace(item, citations=remaining))
        selected_titles.add(title_key)
        if source_url_key:
            selected_source_urls.add(source_url_key)
        for citation in remaining:
            citation_key = canonical_url(citation.url)
            if citation_key:
                selected_citation_urls.add(citation_key)
        return True

    for category in sorted(by_category):
        for candidate in by_category[category]:
            if try_pick(candidate):
                break
        if len(selected) >= count:
            break

    while len(selected) < count and by_source:
        exhausted: list[str] = []
        for source_name in list(by_source):
            if not by_source[source_name]:
                exhausted.append(source_name)
                continue
            while by_source[source_name]:
                if try_pick(by_source[source_name].pop(0)):
                    break
            if not by_source[source_name]:
                exhausted.append(source_name)
            if len(selected) >= count:
                break
        for source_name in exhausted:
            by_source.pop(source_name, None)

    return sorted(selected[:count], key=lambda item: (item.published_at, item.score), reverse=True)


def escape_yaml_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render_sections(items: list[CandidateItem]) -> str:
    lines: list[str] = []
    for index, item in enumerate(items, start=1):
        lines.append(f"### {index}. {item.title}")
        lines.append("")
        lines.append(item.summary)
        lines.append("")
        lines.append(
            f"- 来源站点：[{item.source_name}]({item.url}) | 发布时间：{item.published_at.strftime('%Y-%m-%d')}"
        )
        citation_links = "、".join(f"[{citation.title}]({citation.url})" for citation in item.citations)
        lines.append(f"- 引用来源：{citation_links}")
        lines.append("")
    return "\n".join(lines).rstrip()


def build_markdown(items: list[CandidateItem], sources: list[SourceConfig], title_prefix: str, generated_at: datetime) -> str:
    post_title = f"{title_prefix} {generated_at.strftime('%Y-%m-%d')}"
    source_names = "、".join(source.name for source in sources)
    summary = trim_summary(f"汇总来自 {source_names} 的 {len(items)} 条 AI 相关动态，附引用来源。", 80)
    return "\n".join(
        [
            "---",
            f'title: "{escape_yaml_string(post_title)}"',
            f'date: "{generated_at.isoformat(timespec="seconds")}"',
            "draft: false",
            'tags: ["AI", "日报", "自动化"]',
            'categories: ["热点新闻"]',
            f'summary: "{escape_yaml_string(summary)}"',
            "---",
            "",
            f"# {post_title}",
            "",
            "> 自动抓取厂商发布、行业大事与 KOL 观点，筛选并整理为 10 条 AI 动态。",
            "",
            "## 今日要点",
            "",
            render_sections(items),
            "",
            "## 说明",
            "",
            "- 本文由自动化流程生成，方便每天快速浏览重点信息。",
            "- 已对历史日报中的“引用来源”执行去重，尽量避免重复引用旧链接。",
            "",
        ]
    )


def normalize_markdown_for_comparison(markdown: str) -> str:
    return re.sub(r'^date:\s*".*?"\s*$', 'date: "__NORMALIZED__"', markdown, flags=re.M)


def main() -> int:
    args = parse_args()
    tz = ZoneInfo(args.timezone)
    output_path = (ROOT / args.output_path).resolve() if not Path(args.output_path).is_absolute() else Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    publish_day = datetime.fromisoformat(args.publish_date).date()
    now = datetime.now(tz).replace(year=publish_day.year, month=publish_day.month, day=publish_day.day)

    sources = load_sources(args.config)
    candidates = collect_candidates(sources, tz, now)
    historical_citations = load_historical_citation_urls(output_path.parent, output_path.name)
    items = select_items(candidates, args.count, args.days, now, historical_citations)
    if len(items) < args.count:
        raise RuntimeError(f"Only found {len(items)} items, fewer than requested {args.count}.")

    markdown = build_markdown(items, sources, args.title_prefix, now)
    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")
        if normalize_markdown_for_comparison(existing) == normalize_markdown_for_comparison(markdown):
            print(f"No content change for {output_path}")
            return 0

    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
