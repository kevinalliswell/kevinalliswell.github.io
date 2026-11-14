#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import re
import sys
import time as time_module
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
REPO_ROOT = Path(__file__).resolve().parent.parent
STARS_SNAPSHOT_PATH = REPO_ROOT / "data" / "github_hot_stars.json"
FEATURED_LEDGER_PATH = REPO_ROOT / "data" / "github_hot_featured.json"
TRENDING_URL = "https://github.com/trending?since=daily"
SNAPSHOT_KEEP_DAYS = 14
LEDGER_BOOTSTRAP_DAYS = 30
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
    top_n: int = 5
    max_per_owner: int = 1
    cooldown_days: int = 30
    watch_n: int = 5
    new_repo_days: int = 30

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
            top_n=load_int_env("HOT_REPOS_TOP_N", 5),
            max_per_owner=load_int_env("HOT_REPOS_MAX_PER_OWNER", 1),
            cooldown_days=load_int_env("HOT_REPOS_COOLDOWN_DAYS", 30),
            watch_n=load_int_env("HOT_REPOS_WATCH_N", 5),
            new_repo_days=load_int_env("HOT_REPOS_NEW_REPO_DAYS", 30),
        )


@dataclass
class ReleaseInfo:
    html_url: str
    published_at: datetime | None
    tag_name: str = ""


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
    created_at: datetime | None = None
    license_name: str = ""
    focus_hits: list[str] = field(default_factory=list)
    ai_hits: list[str] = field(default_factory=list)
    priority_owner: bool = False
    influential_owner: bool = False
    latest_release: ReleaseInfo | None = None
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    sources: set[str] = field(default_factory=set)
    trending_stars_today: int | None = None
    daily_gain: float | None = None  # stars gained per day (best available estimate)
    daily_gain_source: str = ""  # trending | snapshot | average
    weekly_gain: int | None = None  # stars gained over the snapshot window (up to 7 days)
    weekly_gain_days: int = 0
    last_featured: date | None = None  # most recent digest (before today) that featured it
    times_featured: int = 0
    refeature_reason: str = ""  # set when a cooled-down repo is let back in


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.token = token

    def request_json(self, url: str, *, retry_rate_limit: bool = True) -> dict[str, Any]:
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
            if exc.code in (403, 429) and "rate limit" in body.lower():
                if retry_rate_limit:
                    # The search API allows 30 requests a minute; wait out the window once.
                    reset = exc.headers.get("X-RateLimit-Reset", "")
                    wait = int(reset) - int(time_module.time()) + 2 if reset.isdigit() else 62
                    time_module.sleep(min(max(wait, 5), 70))
                    return self.request_json(url, retry_rate_limit=False)
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
            tag_name=payload.get("tag_name") or "",
        )

    def repository(self, full_name: str) -> dict[str, Any] | None:
        try:
            return self.request_json(f"https://api.github.com/repos/{full_name}")
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 404, 451):
                return None
            raise

    def readme(self, full_name: str) -> str:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{full_name}/readme",
            headers={
                "Accept": "application/vnd.github.raw+json",
                "User-Agent": "kevin-blog-github-hot-digest",
                "X-GitHub-Api-Version": API_VERSION,
            },
        )
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read(200_000).decode("utf-8", errors="ignore")
        except (urllib.error.URLError, TimeoutError):
            return ""

    def trending(self) -> dict[str, int]:
        """Scrape github.com/trending (no official API). Returns {full_name: stars_today}.

        Any failure returns {} so the digest still works from the other sources.
        """
        request = urllib.request.Request(
            TRENDING_URL, headers={"User-Agent": "Mozilla/5.0 (kevin-blog-github-hot-digest)"}
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except (urllib.error.URLError, TimeoutError):
            return {}
        return parse_trending_html(html)


def parse_trending_html(html: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for article in re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL):
        name = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"/]+/[^"/]+)"', article, re.DOTALL)
        if not name:
            continue
        stars = re.search(r"([\d,]+)\s+stars?\s+today", article)
        result[name.group(1)] = int(stars.group(1).replace(",", "")) if stars else 0
    return result


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )


# ── Star snapshots: measure flow (stars gained), not stock (total stars) ──────


def load_snapshots(path: Path) -> dict[str, dict[str, int]]:
    """{"YYYY-MM-DD": {"owner/repo": stars}}"""
    payload = load_json(path, {})
    return payload if isinstance(payload, dict) else {}


def update_snapshots(
    snapshots: dict[str, dict[str, int]], report_date: date, repositories: list["RepositorySnapshot"]
) -> dict[str, dict[str, int]]:
    cutoff = (report_date - timedelta(days=SNAPSHOT_KEEP_DAYS)).isoformat()
    kept = {day: stars for day, stars in snapshots.items() if cutoff <= day < report_date.isoformat()}
    kept[report_date.isoformat()] = {repo.full_name: repo.stargazers_count for repo in repositories}
    return kept


def apply_star_gains(
    repo: "RepositorySnapshot",
    snapshots: dict[str, dict[str, int]],
    report_date: date,
    new_repo_days: int,
) -> None:
    """Fill repo.daily_gain / weekly_gain from the best signal available."""
    previous: list[tuple[int, int]] = []  # (days_ago, stars)
    for offset in range(1, 8):
        day = (report_date - timedelta(days=offset)).isoformat()
        stars = snapshots.get(day, {}).get(repo.full_name)
        if stars is not None:
            previous.append((offset, stars))

    if previous:
        oldest_offset, oldest_stars = previous[-1]
        repo.weekly_gain = repo.stargazers_count - oldest_stars
        repo.weekly_gain_days = oldest_offset

    if repo.trending_stars_today:
        repo.daily_gain, repo.daily_gain_source = float(repo.trending_stars_today), "trending"
    elif previous:
        nearest_offset, nearest_stars = previous[0]
        repo.daily_gain = max(repo.stargazers_count - nearest_stars, 0) / nearest_offset
        repo.daily_gain_source = "snapshot"
    elif repo.created_at is not None:
        age_days = max((report_date - repo.created_at.astimezone(SHANGHAI_TZ).date()).days, 1)
        if age_days <= new_repo_days:
            # No history yet: a young repo's lifetime average is a fair stand-in.
            repo.daily_gain, repo.daily_gain_source = repo.stargazers_count / age_days, "average"


# ── Featured ledger: a repo is not featured again within the cooldown ─────────


def bootstrap_ledger(digest_dir: Path, report_date: date) -> dict[str, dict[str, Any]]:
    """Seed the ledger from already-published digests so day one does not repeat them."""
    ledger: dict[str, dict[str, Any]] = {}
    for offset in range(LEDGER_BOOTSTRAP_DAYS, 0, -1):
        day = report_date - timedelta(days=offset)
        path = digest_dir / f"github-hot-{day.isoformat()}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"^### \d+\. ([^|\s]+/[^|\s]+) \|", text, re.MULTILINE):
            entry = ledger.setdefault(name, {"dates": [], "release_tag": ""})
            entry["dates"].append(day.isoformat())
    return ledger


def load_ledger(path: Path, digest_dir: Path, report_date: date) -> dict[str, dict[str, Any]]:
    """{"owner/repo": {"dates": ["YYYY-MM-DD", ...], "release_tag": "v1.2.0"}}"""
    if not path.exists():
        ledger = bootstrap_ledger(digest_dir, report_date)
    else:
        payload = load_json(path, {})
        ledger = payload if isinstance(payload, dict) else {}
    # Re-running the same day must give the same answer: forget today's earlier run.
    today = report_date.isoformat()
    for name in list(ledger):
        dates = [day for day in ledger[name].get("dates", []) if day < today]
        if dates:
            ledger[name]["dates"] = dates[-10:]
        else:
            del ledger[name]
    return ledger


def record_featured(
    ledger: dict[str, dict[str, Any]], featured: list["RepositorySnapshot"], report_date: date
) -> None:
    for repo in featured:
        entry = ledger.setdefault(repo.full_name, {"dates": [], "release_tag": ""})
        entry["dates"] = (entry.get("dates", []) + [report_date.isoformat()])[-10:]
        if repo.latest_release and repo.latest_release.tag_name:
            entry["release_tag"] = repo.latest_release.tag_name


def parse_version(tag: str) -> tuple[int, int] | None:
    """(major, minor) from tags like v1.2.3 or @scope/pkg@0.22.0."""
    matches = re.findall(r"(\d+)\.(\d+)", tag or "")
    if not matches:
        return None
    major, minor = matches[-1]
    return int(major), int(minor)


def major_release_since(repo: "RepositorySnapshot", entry: dict[str, Any], last_featured: date) -> bool:
    """True when the repo shipped a new major/minor version after it was last featured."""
    release = repo.latest_release
    if release is None or release.published_at is None:
        return False
    if release.published_at.astimezone(SHANGHAI_TZ).date() <= last_featured:
        return False
    current, recorded = parse_version(release.tag_name), parse_version(entry.get("release_tag", ""))
    if current is None or recorded is None:
        return False
    return current[0] > recorded[0] or (current[0] == recorded[0] == 0 and current[1] > recorded[1])


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

    # Fresh repos: the ones a star-total ranking can never surface.
    month_ago = (since_date + timedelta(days=settings.window_days - settings.new_repo_days)).isoformat()
    queries.append(("new:month", f"created:>={month_ago} stars:>=300 archived:false", "stars", 30))
    queries.append(("new:week", f"created:>={since} stars:>=100 archived:false", "stars", 30))
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
        created_at=parse_datetime(item.get("created_at")),
        license_name=((item.get("license") or {}).get("spdx_id") or "").replace("NOASSERTION", ""),
    )


def enrich_repo(repo: RepositorySnapshot, settings: Settings) -> None:
    text = normalized_text(repo.full_name, repo.description, repo.owner_login, " ".join(repo.topics))
    repo.focus_hits = keyword_hits(text, settings.focus_keywords)
    repo.ai_hits = keyword_hits(text, settings.ai_keywords)
    repo.priority_owner = repo.owner_login in settings.priority_owners
    repo.influential_owner = repo.owner_login in settings.influential_people


def is_relevant(repo: RepositorySnapshot, settings: Settings) -> bool:
    if repo.sources & {"trending", "new"}:
        # Momentum is its own justification, but a repo that does not say
        # what it is cannot be recommended.
        return bool(repo.description)
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
    """Momentum first. Total stars, owner and keywords only nudge the order."""
    score = 0.0
    reasons: list[str] = []

    gain = repo.daily_gain or 0.0
    if gain > 0:
        # A lifetime average is weaker evidence than a measured one-day gain:
        # the repo may already be past its peak.
        measured = gain if repo.daily_gain_source != "average" else gain * 0.5
        score += min(math.log2(measured + 1) * 10, 130)
        # Relative growth lifts small repos that are taking off.
        score += min(measured / max(repo.stargazers_count, 1) * 100, 10)
        label = {
            "trending": f"GitHub Trending 今日 +{gain:,.0f} Stars",
            "snapshot": f"近 24 小时 +{gain:,.0f} Stars",
            "average": f"创建以来日均 +{gain:,.0f} Stars",
        }[repo.daily_gain_source]
        reasons.append(label)
    if repo.weekly_gain and repo.weekly_gain > 0 and repo.weekly_gain_days >= 2:
        reasons.append(f"近 {repo.weekly_gain_days} 天 +{repo.weekly_gain:,} Stars")

    age_days = days_since(repo.created_at, report_time)
    if age_days is not None and age_days <= 7:
        score += 8
        reasons.append(f"创建仅 {age_days} 天的新项目")
    elif age_days is not None and age_days <= settings.new_repo_days:
        score += 5
        reasons.append(f"创建 {age_days} 天的新项目")

    score += min(math.log2(repo.stargazers_count + 1) * 2, 30)

    if repo.latest_release and repo.latest_release.published_at:
        release_days = days_since(repo.latest_release.published_at, report_time)
        if release_days is not None and release_days <= 7:
            score += 8
            reasons.append(f"近 7 天发布 {repo.latest_release.tag_name or '新版本'}")
    if repo.priority_owner:
        score += 10
        reasons.append("来自重点官方组织")
    if repo.influential_owner:
        score += 10
        reasons.append("来自重点人物仓库")
    if repo.focus_hits:
        score += min(len(repo.focus_hits) * 4, 8)
    if repo.ai_hits:
        score += min(len(repo.ai_hits) * 2, 6)

    return score, reasons[:4]


def collect_candidates(client: GitHubClient, settings: Settings, report_date: date) -> list[RepositorySnapshot]:
    since_date = report_date - timedelta(days=settings.window_days)
    repos: dict[str, RepositorySnapshot] = {}

    def add(item: dict[str, Any], source: str) -> RepositorySnapshot | None:
        if item.get("fork") or item.get("archived") or item.get("disabled"):
            return None
        full_name = item.get("full_name")
        if not full_name:
            return None
        repo = repos.setdefault(full_name, to_repo_snapshot(item))
        repo.sources.add(source)
        enrich_repo(repo, settings)
        return repo

    for label, query, sort, per_page in build_queries(settings, since_date):
        for item in client.search_repositories(query, sort=sort, per_page=per_page):
            add(item, label.split(":")[0])

    for full_name, stars_today in client.trending().items():
        item = client.repository(full_name)
        if item is None:
            continue
        repo = add(item, "trending")
        if repo is not None:
            repo.trending_stars_today = stars_today

    return [repo for repo in repos.values() if is_relevant(repo, settings)]


@dataclass
class Selection:
    featured: list[RepositorySnapshot]  # featured[0] is today's deep pick
    watching: list[RepositorySnapshot]  # in cooldown but still moving: one line each


def rank_repositories(
    client: GitHubClient,
    repositories: list[RepositorySnapshot],
    settings: Settings,
    report_date: date,
    snapshots: dict[str, dict[str, int]],
    ledger: dict[str, dict[str, Any]],
) -> Selection:
    report_time = datetime.combine(report_date, time(7, 0), SHANGHAI_TZ)

    for repo in repositories:
        apply_star_gains(repo, snapshots, report_date, settings.new_repo_days)
        repo.score, repo.reasons = score_repo(repo, settings, report_time)
        dates = ledger.get(repo.full_name, {}).get("dates", [])
        if dates:
            repo.last_featured = date.fromisoformat(dates[-1])
            repo.times_featured = len(dates)

    ranked = sorted(repositories, key=lambda repo: (-repo.score, -repo.stargazers_count, repo.full_name))

    # Releases cost one API call each, so only look at repos that can still make the cut.
    for repo in ranked[: max((settings.top_n + settings.watch_n) * 4, 40)]:
        repo.latest_release = client.latest_release(repo.full_name)
        repo.score, repo.reasons = score_repo(repo, settings, report_time)
    ranked.sort(key=lambda repo: (-repo.score, -repo.stargazers_count, repo.full_name))

    featured: list[RepositorySnapshot] = []
    watching: list[RepositorySnapshot] = []
    owner_counts: dict[str, int] = {}
    for repo in ranked:
        cooling = (
            repo.last_featured is not None
            and (report_date - repo.last_featured).days <= settings.cooldown_days
        )
        if cooling and major_release_since(repo, ledger[repo.full_name], repo.last_featured):
            repo.refeature_reason = f"发布新版本 {repo.latest_release.tag_name}"
            cooling = False
        if cooling:
            if len(watching) < settings.watch_n and (repo.daily_gain or 0) > 0:
                watching.append(repo)
            continue
        if len(featured) >= settings.top_n:
            continue
        count = owner_counts.get(repo.owner_login, 0)
        if count >= settings.max_per_owner:
            continue
        owner_counts[repo.owner_login] = count + 1
        featured.append(repo)
    return Selection(featured=featured, watching=watching)


# ── Optional LLM commentary (OpenAI-compatible endpoint, e.g. a relay) ────────

LLM_PROMPT = """你是一名资深开源技术编辑，为中文开发者博客撰写 GitHub 仓库点评。
只依据下面提供的仓库信息和 README 写作，不要编造 README 里没有的功能、数据或对比结论；
信息不足的字段写"README 未说明"。语言：简体中文，技术术语保留英文，不要营销腔。

只输出一个 JSON 对象，不要任何其他文字，字段如下：
- "one_liner": 一句话点评（40 字以内），说清它是什么、为什么值得看
- "problem": 它解决什么问题（1-2 句）
- "difference": 与同类方案相比的特点或取舍（1-2 句）
- "audience": 适合谁用、不适合谁（1 句）
- "quickstart": 最短上手方式，优先给 README 里的安装/运行命令（纯文本，命令用换行分隔，不超过 4 行）
- "risks": 采用前要注意的风险，如许可证、项目成熟度、依赖或成本（1-2 句）

仓库：{full_name}
描述：{description}
语言：{language} | License：{license} | Stars：{stars} | 创建于：{created}
Topics：{topics}

README（可能被截断）：
{readme}
"""
LLM_FIELDS = ("one_liner", "problem", "difference", "audience", "quickstart", "risks")


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str

    @classmethod
    def from_env(cls) -> "LLMConfig | None":
        api_key = os.getenv("HOT_REPOS_LLM_API_KEY", "").strip()
        base_url = os.getenv("HOT_REPOS_LLM_BASE_URL", "").strip().rstrip("/")
        model = os.getenv("HOT_REPOS_LLM_MODEL", "").strip()
        if not (api_key and base_url and model):
            return None
        return cls(api_key=api_key, base_url=base_url, model=model)


def parse_llm_json(content: str) -> dict[str, str] | None:
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    result = {key: str(payload.get(key) or "").strip() for key in LLM_FIELDS}
    return result if result["one_liner"] or result["problem"] else None


def llm_commentary(config: LLMConfig, repo: RepositorySnapshot, readme: str) -> dict[str, str] | None:
    """Ask the model for a structured review. Returns None on any failure."""
    prompt = LLM_PROMPT.format(
        full_name=repo.full_name,
        description=repo.description or "（无）",
        language=repo.language,
        license=repo.license_name or "未声明",
        stars=f"{repo.stargazers_count:,}",
        created=repo.created_at.date().isoformat() if repo.created_at else "未知",
        topics=", ".join(repo.topics) or "（无）",
        readme=readme[:8000] or "（README 获取失败）",
    )
    body = json.dumps(
        {
            "model": config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{config.base_url}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "kevin-blog-github-hot-digest",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return parse_llm_json(payload["choices"][0]["message"]["content"] or "")
    except Exception as exc:  # noqa: BLE001 - a broken relay must never block the digest
        print(f"LLM commentary failed for {repo.full_name}: {type(exc).__name__}", file=sys.stderr)
        return None


# ── README fallbacks used when no LLM is configured ───────────────────────────

INSTALL_HINTS = (
    "pip install", "pipx install", "uv ", "uvx ", "npm i", "npm install", "npx ", "pnpm ", "yarn add",
    "brew install", "cargo install", "go install", "docker run", "docker pull", "git clone", "curl ",
)


def readme_excerpt(readme: str, limit: int = 240) -> str:
    """First prose paragraph of a README, stripped of markup."""
    text = re.sub(r"```.*?```", "", readme, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    for block in re.split(r"\n\s*\n", text):
        block = " ".join(line.strip() for line in block.strip().splitlines())
        if not block or block[0] in "#|>![-*=" or len(block) < 60:
            continue
        block = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", block)
        block = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", block)
        block = re.sub(r"[*_`]", "", block).strip()
        if len(block) < 60:
            continue
        return block if len(block) <= limit else block[:limit].rstrip() + "…"
    return ""


def readme_install_command(readme: str) -> str:
    for block in re.findall(r"```[^\n]*\n(.*?)```", readme, flags=re.DOTALL):
        lines = [line.strip().lstrip("$ ").strip() for line in block.strip().splitlines()]
        hits = [line for line in lines if line.startswith(INSTALL_HINTS) and len(line) <= 160]
        if hits:
            return "\n".join(hits[:3])
    return ""


# ── Rendering: 1 deep pick + short takes + a one-line watchlist ───────────────


def format_gain(repo: RepositorySnapshot) -> str:
    if not repo.daily_gain:
        return "—"
    prefix = {"trending": "今日", "snapshot": "近 24h", "average": "日均"}[repo.daily_gain_source]
    return f"{prefix} +{repo.daily_gain:,.0f}"


def metrics_line(repo: RepositorySnapshot) -> str:
    parts = [f"⭐ {repo.stargazers_count:,}", f"📈 {format_gain(repo)}", f"🍴 {repo.forks_count:,}", repo.language]
    if repo.license_name:
        parts.append(repo.license_name)
    if repo.created_at:
        parts.append(f"创建于 {repo.created_at.astimezone(SHANGHAI_TZ).date().isoformat()}")
    return " · ".join(parts)


def source_links(repo: RepositorySnapshot) -> str:
    links = [f"[仓库]({repo.html_url})"]
    if repo.latest_release and repo.latest_release.html_url:
        links.append(f"[最新 Release]({repo.latest_release.html_url})")
    if repo.homepage:
        links.append(f"[Homepage]({repo.homepage})")
    return " · ".join(links)


def short_text(value: str, limit: int) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[:limit].rstrip() + "…"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_deep_pick(repo: RepositorySnapshot, review: dict[str, str] | None, readme: str) -> list[str]:
    lines = [f"## 今日主推：[{repo.full_name}]({repo.html_url})", ""]
    lead = (review or {}).get("one_liner") or repo.description or "仓库未填写描述。"
    lines += [f"> {lead}", "", metrics_line(repo), ""]
    if repo.refeature_reason:
        lines += [f"*{repo.last_featured.isoformat()} 推荐过，因{repo.refeature_reason}再次上榜。*", ""]
    lines += ["**为什么是今天**", ""] + [f"- {reason}" for reason in repo.reasons] + [""]

    if review:
        for label, key in (("它解决什么问题", "problem"), ("和同类相比", "difference"), ("适合谁", "audience")):
            if review[key]:
                lines += [f"**{label}**", "", review[key], ""]
        if review["quickstart"]:
            lines += ["**最短上手**", "", "```bash", review["quickstart"], "```", ""]
        if review["risks"]:
            lines += ["**采用前留意**", "", review["risks"], ""]
        if repo.description and repo.description != lead:
            lines += [f"官方描述：{repo.description}", ""]
    else:
        excerpt = readme_excerpt(readme)
        if excerpt:
            lines += ["**README 摘录**", "", f"> {excerpt}", ""]
        command = readme_install_command(readme)
        if command:
            lines += ["**最短上手**", "", "```bash", command, "```", ""]
    if repo.topics:
        lines += ["Topics：" + " ".join(f"`{topic}`" for topic in repo.topics[:8]), ""]
    lines += [f"链接：{source_links(repo)}", ""]
    return lines


def render_brief(index: int, repo: RepositorySnapshot, review: dict[str, str] | None) -> list[str]:
    lines = [f"### {index}. {repo.full_name}", ""]
    lines += [(review or {}).get("one_liner") or repo.description or "仓库未填写描述。", ""]
    lines.append(f"- 指标：{metrics_line(repo)}")
    lines.append(f"- 上榜理由：{'；'.join(repo.reasons) or '综合热度靠前'}")
    if review and review["audience"]:
        lines.append(f"- 适合谁：{review['audience']}")
    if review and review["risks"]:
        lines.append(f"- 留意：{review['risks']}")
    if repo.refeature_reason:
        lines.append(f"- 再次上榜：{repo.last_featured.isoformat()} 推荐过，{repo.refeature_reason}")
    lines += [f"- 链接：{source_links(repo)}", ""]
    return lines


def render_digest(
    selection: Selection,
    settings: Settings,
    report_date: date,
    reviews: dict[str, dict[str, str]] | None = None,
    readmes: dict[str, str] | None = None,
) -> str:
    reviews, readmes = reviews or {}, readmes or {}
    report_time = datetime.combine(report_date, time(7, 0), SHANGHAI_TZ)
    featured = selection.featured
    names = "、".join(repo.full_name.split("/")[1] for repo in featured[1:4])

    if featured:
        top = featured[0]
        hook = reviews.get(top.full_name, {}).get("one_liner") or top.description
        title = f"GitHub 热点 {report_date.isoformat()}｜{top.full_name.split('/')[1]}"
        if hook:
            title += f"：{short_text(hook, 36)}"
        summary = f"今日主推 {top.full_name}（{format_gain(top)} Stars），速览 {len(featured) - 1} 个：{names} 等。"
    else:
        title = f"GitHub 热点 {report_date.isoformat()}｜今日无新上榜项目"
        summary = "今天没有通过筛选的新项目，仅更新持续关注列表。"

    tags = ["GitHub", "开源", "日报"]
    for repo in featured[:1]:
        if repo.language and repo.language != "Unknown":
            tags.append(repo.language)
    lines = [
        "---",
        f"title: {yaml_string(title)}",
        f'date: "{report_time.isoformat()}"',
        "draft: false",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        'categories: ["日报"]',
        f"summary: {yaml_string(summary)}",
        "---",
        "",
        f"> {summary}",
        "",
    ]

    if featured:
        top = featured[0]
        lines += render_deep_pick(top, reviews.get(top.full_name), readmes.get(top.full_name, ""))
        if len(featured) > 1:
            lines += ["---", "", "## 速览", ""]
            for index, repo in enumerate(featured[1:], start=1):
                lines += render_brief(index, repo, reviews.get(repo.full_name))

    if selection.watching:
        lines += [
            "---",
            "",
            "## 持续关注",
            "",
            f"近 {settings.cooldown_days} 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：",
            "",
            "| 项目 | Stars | 增长 | 上次推荐 |",
            "|------|-------|------|----------|",
        ]
        for repo in selection.watching:
            lines.append(
                f"| [{repo.full_name}]({repo.html_url}) | {repo.stargazers_count:,} | "
                f"{format_gain(repo)} | {repo.last_featured.isoformat()} |"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 筛选方法",
        "",
        "- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。",
        "- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。",
        f"- 去重规则：推荐过的仓库 {settings.cooldown_days} 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 {settings.max_per_owner} 个。",
        "- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。"
        if reviews
        else "- 本文由脚本根据 GitHub 公开数据自动生成，描述取自仓库原文。",
        "- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。",
    ]
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
        else Path("content/news") / f"github-hot-{report_date.isoformat()}.md"
    )

    settings = Settings.from_env()
    client = GitHubClient(os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"))
    snapshots = load_snapshots(STARS_SNAPSHOT_PATH)
    ledger = load_ledger(FEATURED_LEDGER_PATH, output_path.parent, report_date)

    candidates = collect_candidates(client, settings, report_date)
    if not candidates:
        raise RuntimeError("No repositories matched the current GitHub hot digest rules.")
    selection = rank_repositories(client, candidates, settings, report_date, snapshots, ledger)

    llm = LLMConfig.from_env()
    readmes: dict[str, str] = {}
    reviews: dict[str, dict[str, str]] = {}
    for index, repo in enumerate(selection.featured):
        if index == 0 or llm:
            readmes[repo.full_name] = client.readme(repo.full_name)
        if llm:
            review = llm_commentary(llm, repo, readmes[repo.full_name])
            if review:
                reviews[repo.full_name] = review

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_digest(selection, settings, report_date, reviews, readmes), encoding="utf-8"
    )
    record_featured(ledger, selection.featured, report_date)
    save_json(FEATURED_LEDGER_PATH, ledger)
    save_json(STARS_SNAPSHOT_PATH, update_snapshots(snapshots, report_date, candidates))
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
