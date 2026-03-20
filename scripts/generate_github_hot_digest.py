#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
API_VERSION = "2022-11-28"
DEFAULT_FOCUS_KEYWORDS = ["claude", "gemini", "openai", "copilot"]
DEFAULT_AI_KEYWORDS = [
    "agent",
    "agents",
    "llm",
    "gpt",
    "model",
    "prompt",
    "reasoning",
    "eval",
    "evaluation",
]
DEFAULT_PRIORITY_OWNERS = [
    "openai",
    "anthropics",
    "google-gemini",
    "github",
    "microsoft",
    "huggingface",
]
DEFAULT_ALWAYS_INCLUDE_OWNERS = ["openai", "anthropics", "google-gemini", "github"]
DEFAULT_INFLUENTIAL_PEOPLE = [
    "simonw",
    "karpathy",
    "rasbt",
    "hiyouga",
    "swyxio",
]


def dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def load_csv_env(name: str, default: list[str]) -> list[str]:
    raw = os.getenv(name, "")
    if not raw.strip():
        return default.copy()
    return dedupe_keep_order(raw.split(","))


def load_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalized_text(*chunks: str) -> str:
    lowered = " ".join(chunks).lower()
    return re.sub(r"[^a-z0-9#+.-]+", " ", lowered)


def keyword_hits(text: str, keywords: list[str]) -> list[str]:
    haystack = f" {text} "
    hits: list[str] = []
    for keyword in keywords:
        needle = keyword.lower()
        if f" {needle} " in haystack or needle in haystack:
            hits.append(needle)
    return dedupe_keep_order(hits)


@dataclass
class Settings:
    focus_keywords: list[str] = field(default_factory=lambda: DEFAULT_FOCUS_KEYWORDS.copy())
    ai_keywords: list[str] = field(default_factory=lambda: DEFAULT_AI_KEYWORDS.copy())
    priority_owners: list[str] = field(default_factory=lambda: DEFAULT_PRIORITY_OWNERS.copy())
    always_include_owners: list[str] = field(
        default_factory=lambda: DEFAULT_ALWAYS_INCLUDE_OWNERS.copy()
    )
    influential_people: list[str] = field(
        default_factory=lambda: DEFAULT_INFLUENTIAL_PEOPLE.copy()
    )
    window_days: int = 7
    minimum_stars: int = 80
    per_query_limit: int = 12
    per_owner_limit: int = 20
    top_n: int = 10
    max_per_owner: int = 2

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            focus_keywords=load_csv_env("HOT_REPOS_FOCUS_KEYWORDS", DEFAULT_FOCUS_KEYWORDS),
            ai_keywords=load_csv_env("HOT_REPOS_AI_KEYWORDS", DEFAULT_AI_KEYWORDS),
            priority_owners=load_csv_env("HOT_REPOS_PRIORITY_OWNERS", DEFAULT_PRIORITY_OWNERS),
            always_include_owners=load_csv_env(
                "HOT_REPOS_ALWAYS_INCLUDE_OWNERS", DEFAULT_ALWAYS_INCLUDE_OWNERS
            ),
            influential_people=load_csv_env(
                "HOT_REPOS_INFLUENTIAL_PEOPLE", DEFAULT_INFLUENTIAL_PEOPLE
            ),
            window_days=load_int_env("HOT_REPOS_WINDOW_DAYS", 7),
            minimum_stars=load_int_env("HOT_REPOS_MIN_STARS", 80),
            per_query_limit=load_int_env("HOT_REPOS_PER_QUERY_LIMIT", 12),
            per_owner_limit=load_int_env("HOT_REPOS_PER_OWNER_LIMIT", 20),
            top_n=load_int_env("HOT_REPOS_TOP_N", 10),
            max_per_owner=load_int_env("HOT_REPOS_MAX_PER_OWNER", 2),
        )


@dataclass
class ReleaseInfo:
    html_url: str
    published_at: datetime | None


@dataclass
class RepositorySnapshot:
    full_name: str
    html_url: str
    description: str
    owner_login: str
    owner_type: str
    owner_url: str
    stargazers_count: int
    forks_count: int
    language: str
    topics: list[str]
    homepage: str
    pushed_at: datetime | None
    focus_hits: list[str] = field(default_factory=list)
    ai_hits: list[str] = field(default_factory=list)
    priority_owner: bool = False
    influential_owner: bool = False
    latest_release: ReleaseInfo | None = None
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.token = token

    def request_json(self, url: str) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "kevin-blog-github-hot-digest",
                "X-GitHub-Api-Version": API_VERSION,
            },
        )
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            if exc.code == 403 and "rate limit" in body.lower():
                raise RuntimeError(
                    "GitHub API rate limit exceeded. Please set GITHUB_TOKEN or GH_TOKEN."
                ) from exc
            raise

    def search_repositories(
        self,
        query: str,
        *,
        sort: str = "updated",
        order: str = "desc",
        per_page: int = 10,
    ) -> list[dict[str, Any]]:
        params = urllib.parse.urlencode(
            {"q": query, "sort": sort, "order": order, "per_page": per_page}
        )
        payload = self.request_json(f"https://api.github.com/search/repositories?{params}")
        return list(payload.get("items", []))

    def latest_release(self, full_name: str) -> ReleaseInfo | None:
        try:
            payload = self.request_json(f"https://api.github.com/repos/{full_name}/releases/latest")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise
        return ReleaseInfo(
            html_url=payload.get("html_url", ""),
            published_at=parse_datetime(payload.get("published_at")),
        )


def build_queries(settings: Settings, since_date: date) -> list[tuple[str, str, str, int]]:
    since = since_date.isoformat()
    queries: list[tuple[str, str, str, int]] = []

    for keyword in settings.focus_keywords:
        queries.append(
            (
                f"focus:{keyword}",
                f"{keyword} pushed:>={since} stars:>={settings.minimum_stars} archived:false",
                "stars",
                settings.per_query_limit,
            )
        )

    for topic in ["topic:llm", "topic:generative-ai", "topic:ai-agents"]:
        queries.append(
            (
                topic,
                f"{topic} pushed:>={since} stars:>={settings.minimum_stars} archived:false",
                "updated",
                settings.per_query_limit,
            )
        )

    for owner in dedupe_keep_order(settings.priority_owners + settings.influential_people):
        per_owner_limit = settings.per_owner_limit if owner in settings.priority_owners else min(8, settings.per_owner_limit)
        queries.append(
            (
                f"owner:{owner}",
                f"user:{owner} pushed:>={since} archived:false",
                "updated",
                per_owner_limit,
            )
        )
    return queries


def to_repo_snapshot(item: dict[str, Any]) -> RepositorySnapshot:
    owner = item.get("owner") or {}
    return RepositorySnapshot(
        full_name=item.get("full_name", ""),
        html_url=item.get("html_url", ""),
        description=(item.get("description") or "").strip(),
        owner_login=(owner.get("login") or "").lower(),
        owner_type=owner.get("type") or "",
        owner_url=owner.get("html_url") or "",
        stargazers_count=int(item.get("stargazers_count", 0) or 0),
        forks_count=int(item.get("forks_count", 0) or 0),
        language=item.get("language") or "Unknown",
        topics=list(item.get("topics") or []),
        homepage=(item.get("homepage") or "").strip(),
        pushed_at=parse_datetime(item.get("pushed_at")),
    )


def enrich_repo(repo: RepositorySnapshot, settings: Settings) -> None:
    text = normalized_text(repo.full_name, repo.description, repo.owner_login, " ".join(repo.topics))
    repo.focus_hits = keyword_hits(text, settings.focus_keywords)
    repo.ai_hits = keyword_hits(text, settings.ai_keywords)
    repo.priority_owner = repo.owner_login in settings.priority_owners
    repo.influential_owner = repo.owner_login in settings.influential_people


def is_relevant(repo: RepositorySnapshot, settings: Settings) -> bool:
    if repo.stargazers_count < settings.minimum_stars and repo.owner_login not in settings.always_include_owners:
        return False
    if repo.focus_hits or repo.ai_hits:
        return True
    return repo.owner_login in settings.always_include_owners


def days_since(value: datetime | None, report_time: datetime) -> int | None:
    if value is None:
        return None
    localized = value.astimezone(SHANGHAI_TZ)
    return max((report_time - localized).days, 0)


def score_repo(repo: RepositorySnapshot, settings: Settings, report_time: datetime) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    score += min(math.log2(repo.stargazers_count + 1) * 12, 90)
    score += min(math.log2(repo.forks_count + 1) * 8, 55)

    if repo.stargazers_count >= 5000:
        reasons.append("社区关注度高")
    elif repo.stargazers_count >= 1000:
        reasons.append("星标基础扎实")

    if repo.forks_count >= 300:
        reasons.append("开发者参与度强")

    pushed_days = days_since(repo.pushed_at, report_time)
    if pushed_days is not None:
        score += max(0.0, 18.0 - (pushed_days * 2.3))
        if pushed_days <= 2:
            reasons.append("近 48 小时仍在活跃更新")
        elif pushed_days <= settings.window_days:
            reasons.append("最近一周有明显活跃度")

    if repo.priority_owner:
        score += 36
        reasons.append("来自重点官方组织")
    if repo.influential_owner:
        score += 24
        reasons.append("来自重点人物仓库")
    if repo.focus_hits:
        score += len(repo.focus_hits) * 12
        reasons.append(f"直接命中重点主题：{', '.join(repo.focus_hits)}")
    if repo.ai_hits:
        score += min(len(repo.ai_hits) * 5, 15)
        reasons.append(f"具备 AI/Agent 信号：{', '.join(repo.ai_hits[:3])}")
    if repo.latest_release and repo.latest_release.published_at:
        release_days = days_since(repo.latest_release.published_at, report_time)
        if release_days is not None and release_days <= 21:
            score += 8
            reasons.append("最近 21 天内有正式版本发布")
    if repo.homepage:
        score += 2
    if repo.owner_type == "Organization":
        score += 2

    return score, reasons[:4]


def relevance_tier(repo: RepositorySnapshot) -> int:
    if (repo.priority_owner or repo.influential_owner) and repo.focus_hits:
        return 0
    if repo.priority_owner or repo.influential_owner:
        return 1
    if repo.focus_hits:
        return 2
    if repo.ai_hits:
        return 3
    return 4


def collect_candidates(client: GitHubClient, settings: Settings, report_date: date) -> list[RepositorySnapshot]:
    since_date = report_date - timedelta(days=settings.window_days)
    repos: dict[str, RepositorySnapshot] = {}

    for _, query, sort, per_page in build_queries(settings, since_date):
        for item in client.search_repositories(query, sort=sort, per_page=per_page):
            if item.get("fork") or item.get("archived") or item.get("disabled"):
                continue
            full_name = item.get("full_name")
            if not full_name:
                continue
            repo = repos.setdefault(full_name, to_repo_snapshot(item))
            enrich_repo(repo, settings)

    relevant = [repo for repo in repos.values() if is_relevant(repo, settings)]
    prefetch = sorted(
        relevant,
        key=lambda repo: (
            -relevance_tier(repo),
            repo.stargazers_count,
            repo.forks_count,
            repo.pushed_at or datetime.min,
        ),
        reverse=True,
    )[: max(settings.top_n * 3, 30)]

    for repo in prefetch:
        repo.latest_release = client.latest_release(repo.full_name)

    return relevant


def rank_repositories(
    repositories: list[RepositorySnapshot], settings: Settings, report_date: date
) -> list[RepositorySnapshot]:
    report_time = datetime.combine(report_date, time(7, 0), SHANGHAI_TZ)
    ranked: list[RepositorySnapshot] = []
    for repo in repositories:
        if not is_relevant(repo, settings):
            continue
        repo.score, repo.reasons = score_repo(repo, settings, report_time)
        ranked.append(repo)

    ranked.sort(
        key=lambda repo: (
            relevance_tier(repo),
            -repo.score,
            -repo.stargazers_count,
            -repo.forks_count,
            -(repo.pushed_at.timestamp() if repo.pushed_at else 0),
        ),
    )

    selected: list[RepositorySnapshot] = []
    owner_counts: dict[str, int] = {}
    for repo in ranked:
        count = owner_counts.get(repo.owner_login, 0)
        if count >= settings.max_per_owner:
            continue
        owner_counts[repo.owner_login] = count + 1
        selected.append(repo)
        if len(selected) >= settings.top_n:
            break
    return selected


def render_digest(repositories: list[RepositorySnapshot], settings: Settings, report_date: date) -> str:
    report_time = datetime.combine(report_date, time(7, 0), SHANGHAI_TZ)
    summary = "聚合 GitHub 最近活跃且最具价值和影响力的 10 个 AI 热点仓库，附引用来源。"
    lines = [
        "---",
        f'title: "GitHub 热点项目日报 {report_date.isoformat()}"',
        f'date: "{report_time.isoformat()}"',
        "draft: false",
        'tags: ["GitHub", "AI", "日报", "OpenAI", "Claude", "Gemini", "Copilot"]',
        'categories: ["热点观察"]',
        f'summary: "{summary}"',
        "---",
        "",
        f"# GitHub 热点项目日报 {report_date.isoformat()}",
        "",
        "> 自动抓取 GitHub 最近活跃仓库，围绕 Claude / Gemini / OpenAI / Copilot 与重点人物仓库，筛选最具价值和影响力的 Top 10。",
        "",
        "## 筛选方法",
        "",
        f"- 时间窗口：最近 {settings.window_days} 天内仍在活跃更新的公开仓库。",
        "- 重点方向：Claude、Gemini、OpenAI、Copilot，以及重点人物相关仓库。",
        "- 评分信号：Stars、Forks、最近更新时间、关键词命中、重点 owner 加权、近期 Release。",
        "- 去重规则：同一 owner 最多保留 2 个项目，避免单一组织占满榜单。",
        "",
        "## 今日 Top 10",
        "",
    ]

    for index, repo in enumerate(repositories, start=1):
        pushed_at = repo.pushed_at.astimezone(SHANGHAI_TZ).strftime("%Y-%m-%d") if repo.pushed_at else "unknown"
        metrics = (
            f"Stars {repo.stargazers_count:,} | Forks {repo.forks_count:,} | "
            f"语言 {repo.language} | 最近更新 {pushed_at}"
        )
        source_links = [f"[仓库]({repo.html_url})", f"[Owner]({repo.owner_url})"]
        if repo.latest_release and repo.latest_release.html_url:
            source_links.append(f"[最新 Release]({repo.latest_release.html_url})")
        if repo.homepage:
            source_links.append(f"[Homepage]({repo.homepage})")
        hit_text = ", ".join(repo.focus_hits or repo.ai_hits or ["general-ai"])

        lines.extend(
            [
                f"### {index}. {repo.full_name} | 综合评分 {repo.score:.1f}",
                "",
                repo.description or "仓库描述缺失，但从元数据看具备较强关注度与活跃度。",
                "",
                f"- 关注理由：{'；'.join(repo.reasons)}",
                f"- 关键指标：{metrics}",
                f"- 命中主题：{hit_text}",
                f"- 引用来源：{' · '.join(source_links)}",
                "",
            ]
        )

    watchlist = ", ".join(settings.priority_owners + settings.influential_people)
    lines.extend(
        [
            "## 说明",
            "",
            "- 本文由 GitHub Actions 自动生成并发布。",
            f"- 当前重点观察对象：`{watchlist}`。",
            "- 数据来源为 GitHub Search API、仓库主页与 Release 页面，所有条目均附原始链接。",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    report_date = (
        datetime.strptime(argv[1], "%Y-%m-%d").date()
        if len(argv) > 1
        else datetime.now(SHANGHAI_TZ).date()
    )
    output_path = (
        Path(argv[2])
        if len(argv) > 2
        else Path("content/posts/news") / f"github-hot-{report_date.isoformat()}.md"
    )

    settings = Settings.from_env()
    client = GitHubClient(os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"))
    candidates = collect_candidates(client, settings, report_date)
    ranked = rank_repositories(candidates, settings, report_date)
    if not ranked:
        raise RuntimeError("No repositories matched the current GitHub hot digest rules.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_digest(ranked, settings, report_date), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
