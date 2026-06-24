#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import math
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, time as datetime_time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_SOURCE_LABEL = "GPT-5.3-codex"
EASTMONEY_KLINE_URL = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
EASTMONEY_PROVIDER_URL = "https://quote.eastmoney.com/"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart"
YAHOO_PROVIDER_URL = "https://finance.yahoo.com/"


@dataclass(frozen=True)
class OutputPaths:
    json_path: Path
    markdown_path: Path
    html_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate configured stock/theme historical curve tracking artifacts."
    )
    parser.add_argument(
        "--config",
        default="data/investment_stock_tracks.json",
        help="JSON config containing stock and basket definitions.",
    )
    parser.add_argument(
        "--output-dir",
        default="static/investment-briefs/stock-tracks",
        help="Directory for generated JSON/Markdown/HTML artifacts.",
    )
    parser.add_argument(
        "--date",
        default=datetime.now(SHANGHAI_TZ).date().isoformat(),
        help="Report date in YYYY-MM-DD. Defaults to current Asia/Shanghai date.",
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=None,
        help="Calendar-day lookback override. Defaults to config lookback_days.",
    )
    parser.add_argument(
        "--source-label",
        default=None,
        help="Source label in filenames and metadata. Defaults to config or GPT-5.3-codex.",
    )
    parser.add_argument(
        "--no-latest",
        action="store_true",
        help="Only write dated artifacts; skip stock-history-tracker-latest.* copies.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    clean = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    while "--" in clean:
        clean = clean.replace("--", "-")
    return clean.strip("-") or "stock-tracker"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_eastmoney_klines(secid: str, start: date, end: date) -> list[dict[str, Any]]:
    params = {
        "secid": secid,
        "klt": "101",
        "fqt": "1",
        "beg": start.strftime("%Y%m%d"),
        "end": end.strftime("%Y%m%d"),
        "lmt": "1000000",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
    }
    url = f"{EASTMONEY_KLINE_URL}?{urllib.parse.urlencode(params)}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 Chrome/126 Safari/537.36"
        ),
        "Referer": EASTMONEY_PROVIDER_URL,
    }
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=12) as response:
            data = json.load(response)
        rows = ((data or {}).get("data") or {}).get("klines") or []
        return [parse_kline(row) for row in rows]
    except Exception as exc:  # noqa: BLE001 - fallback source is intentional.
        raise RuntimeError(f"Eastmoney kline fetch failed for {secid}: {exc}") from exc


def fetch_yahoo_chart(symbol: str, start: date, end: date) -> list[dict[str, Any]]:
    period1 = int(datetime.combine(start, datetime_time.min, SHANGHAI_TZ).timestamp())
    period2 = int(
        datetime.combine(end + timedelta(days=1), datetime_time.min, SHANGHAI_TZ).timestamp()
    )
    params = {
        "period1": str(period1),
        "period2": str(period2),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    url = f"{YAHOO_CHART_URL}/{urllib.parse.quote(symbol)}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
            chart = data.get("chart") or {}
            if chart.get("error"):
                raise RuntimeError(chart["error"])
            result = (chart.get("result") or [None])[0]
            if not result:
                return []
            timestamps = result.get("timestamp") or []
            quote = ((result.get("indicators") or {}).get("quote") or [{}])[0]
            adjclose = ((result.get("indicators") or {}).get("adjclose") or [{}])[0].get(
                "adjclose"
            ) or []
            records: list[dict[str, Any]] = []
            for index, timestamp in enumerate(timestamps):
                close = value_at(adjclose, index) or value_at(quote.get("close") or [], index)
                if close is None:
                    continue
                open_value = value_at(quote.get("open") or [], index) or close
                high_value = value_at(quote.get("high") or [], index) or close
                low_value = value_at(quote.get("low") or [], index) or close
                volume = value_at(quote.get("volume") or [], index) or 0
                day = datetime.fromtimestamp(timestamp, SHANGHAI_TZ).date().isoformat()
                records.append(
                    {
                        "date": day,
                        "open": float(open_value),
                        "close": float(close),
                        "high": float(high_value),
                        "low": float(low_value),
                        "volume": int(volume),
                        "amount": None,
                        "amplitude_pct": None,
                        "change_pct": None,
                        "change": None,
                        "turnover_pct": None,
                    }
                )
            return records
        except Exception as exc:  # noqa: BLE001 - keep automation resilient.
            last_error = exc
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"Yahoo chart fetch failed for {symbol}: {last_error}")


def value_at(values: list[Any], index: int) -> Any:
    if index >= len(values):
        return None
    return values[index]


def fetch_price_history(entry: dict[str, Any], start: date, end: date) -> tuple[list[dict[str, Any]], str, str]:
    errors: list[str] = []
    if entry.get("secid"):
        try:
            return fetch_eastmoney_klines(entry["secid"], start, end), "Eastmoney", EASTMONEY_PROVIDER_URL
        except Exception as exc:  # noqa: BLE001 - fallback source is intentional.
            errors.append(str(exc))
    if entry.get("yahoo_symbol"):
        try:
            return fetch_yahoo_chart(entry["yahoo_symbol"], start, end), "Yahoo Finance", YAHOO_PROVIDER_URL
        except Exception as exc:  # noqa: BLE001 - report both failures.
            errors.append(str(exc))
    raise RuntimeError("; ".join(errors) or "No market data source configured")


def parse_kline(row: str) -> dict[str, Any]:
    fields = row.split(",")
    return {
        "date": fields[0],
        "open": float(fields[1]),
        "close": float(fields[2]),
        "high": float(fields[3]),
        "low": float(fields[4]),
        "volume": int(float(fields[5])),
        "amount": float(fields[6]),
        "amplitude_pct": float(fields[7]),
        "change_pct": float(fields[8]),
        "change": float(fields[9]),
        "turnover_pct": float(fields[10]),
    }


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return []
    base = records[0]["close"]
    if not base:
        return records
    normalized: list[dict[str, Any]] = []
    for item in records:
        copy = dict(item)
        copy["normalized"] = round(copy["close"] / base * 100, 4)
        normalized.append(copy)
    return normalized


def make_basket_records(member_series: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_dates = sorted(
        {row["date"] for member in member_series for row in member.get("records", [])}
    )
    latest_by_member: dict[str, float] = {}
    records_by_member = {
        member["ticker"]: {row["date"]: row for row in member.get("records", [])}
        for member in member_series
    }
    basket: list[dict[str, Any]] = []
    for day in all_dates:
        values: list[float] = []
        active_members: list[str] = []
        for ticker, rows in records_by_member.items():
            row = rows.get(day)
            if row:
                latest_by_member[ticker] = row["normalized"]
            if ticker in latest_by_member:
                values.append(latest_by_member[ticker])
                active_members.append(ticker)
        if values:
            avg = sum(values) / len(values)
            basket.append(
                {
                    "date": day,
                    "close": round(avg, 4),
                    "normalized": round(avg, 4),
                    "member_count": len(values),
                    "members": active_members,
                }
            )
    return basket


def pct_change(records: list[dict[str, Any]], sessions: int) -> float | None:
    if len(records) <= sessions:
        return None
    current = records[-1]["close"]
    prior = records[-sessions - 1]["close"]
    if prior == 0:
        return None
    return current / prior - 1


def moving_average(records: list[dict[str, Any]], window: int) -> float | None:
    if len(records) < window:
        return None
    values = [row["close"] for row in records[-window:]]
    return sum(values) / window


def max_drawdown_from_high(records: list[dict[str, Any]], sessions: int = 120) -> float | None:
    if not records:
        return None
    window = records[-sessions:] if len(records) >= sessions else records
    high = max(row.get("high", row["close"]) for row in window)
    if high == 0:
        return None
    return records[-1]["close"] / high - 1


def trend_label(records: list[dict[str, Any]]) -> str:
    if not records:
        return "无数据"
    close = records[-1]["close"]
    ma20 = moving_average(records, 20)
    ma60 = moving_average(records, 60)
    ma120 = moving_average(records, 120)
    if ma20 and ma60 and close > ma20 > ma60:
        return "强趋势"
    if ma20 and ma60 and close < ma20 < ma60:
        return "弱趋势"
    if ma120 and close > ma120:
        return "中期上方"
    if ma120 and close < ma120:
        return "中期下方"
    return "震荡/样本不足"


def metrics_for(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {
            "last_date": None,
            "last_close": None,
            "return_20d": None,
            "return_60d": None,
            "return_120d": None,
            "drawdown_from_120d_high": None,
            "ma20": None,
            "ma60": None,
            "ma120": None,
            "trend": "无数据",
        }
    return {
        "last_date": records[-1]["date"],
        "last_close": records[-1]["close"],
        "return_20d": pct_change(records, 20),
        "return_60d": pct_change(records, 60),
        "return_120d": pct_change(records, 120),
        "drawdown_from_120d_high": max_drawdown_from_high(records, 120),
        "ma20": moving_average(records, 20),
        "ma60": moving_average(records, 60),
        "ma120": moving_average(records, 120),
        "trend": trend_label(records),
    }


def build_stock_track(entry: dict[str, Any], start: date, end: date) -> dict[str, Any]:
    raw_records, data_source, data_source_url = fetch_price_history(entry, start, end)
    records = normalize_records(raw_records)
    return {
        "id": entry["id"],
        "type": "stock",
        "name": entry["name"],
        "ticker": entry["ticker"],
        "theme": entry.get("theme", ""),
        "note": entry.get("note", ""),
        "source_url": entry.get("source_url", EASTMONEY_PROVIDER_URL),
        "data_source": data_source,
        "data_source_url": data_source_url,
        "metrics": metrics_for(records),
        "records": records,
    }


def build_basket_track(entry: dict[str, Any], start: date, end: date) -> dict[str, Any]:
    members: list[dict[str, Any]] = []
    for member in entry.get("members", []):
        raw_records, data_source, data_source_url = fetch_price_history(member, start, end)
        records = normalize_records(raw_records)
        members.append(
            {
                "name": member["name"],
                "ticker": member["ticker"],
                "source_url": member.get("source_url", EASTMONEY_PROVIDER_URL),
                "data_source": data_source,
                "data_source_url": data_source_url,
                "metrics": metrics_for(records),
                "records": records,
            }
        )
    basket_records = make_basket_records(members)
    return {
        "id": entry["id"],
        "type": "basket",
        "name": entry["name"],
        "ticker": entry.get("ticker", ""),
        "theme": entry.get("theme", ""),
        "note": entry.get("note", ""),
        "metrics": metrics_for(basket_records),
        "records": basket_records,
        "members": [
            {
                "name": member["name"],
                "ticker": member["ticker"],
                "source_url": member["source_url"],
                "data_source": member["data_source"],
                "data_source_url": member["data_source_url"],
                "metrics": member["metrics"],
            }
            for member in members
        ],
    }


def build_payload(config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    report_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    lookback_days = args.lookback_days or int(config.get("lookback_days", 365))
    source_label = args.source_label or config.get("source_label") or DEFAULT_SOURCE_LABEL
    start_date = report_date - timedelta(days=lookback_days)
    tracks = []
    errors = []
    for entry in config.get("tracks", []):
        try:
            if entry.get("type") == "basket":
                tracks.append(build_basket_track(entry, start_date, report_date))
            else:
                tracks.append(build_stock_track(entry, start_date, report_date))
        except Exception as exc:  # noqa: BLE001 - one bad track should not kill the dashboard.
            errors.append(
                {
                    "id": entry.get("id", entry.get("name", "unknown")),
                    "name": entry.get("name", ""),
                    "error": str(exc),
                }
            )
    return {
        "date": report_date.isoformat(),
        "timezone": "Asia/Shanghai",
        "generated_at": datetime.now(SHANGHAI_TZ).isoformat(timespec="seconds"),
        "source_label": source_label,
        "lookback_days": lookback_days,
        "title": f"指定股票历史曲线跟踪 {report_date.isoformat()}",
        "provider": {
            "name": "Eastmoney daily K-line with Yahoo Finance fallback",
            "url": EASTMONEY_PROVIDER_URL,
            "fallback_url": YAHOO_PROVIDER_URL,
            "note": "优先使用东方财富前复权日线行情；若接口失败，回退到 Yahoo Finance 日线行情。该模块只做价格曲线与技术状态跟踪，不替代公告、财报和交易所披露。",
        },
        "tracks": tracks,
        "errors": errors,
    }


def fmt_number(value: Any, digits: int = 2) -> str:
    if value is None:
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def fmt_pct(value: Any) -> str:
    if value is None:
        return "-"
    return f"{value * 100:+.2f}%"


def signal_summary(track: dict[str, Any]) -> str:
    metrics = track.get("metrics", {})
    trend = metrics.get("trend", "无数据")
    r60 = metrics.get("return_60d")
    drawdown = metrics.get("drawdown_from_120d_high")
    return (
        f"{trend}；60 日收益 {fmt_pct(r60)}；"
        f"距 120 日高点 {fmt_pct(drawdown)}。"
    )


def moving_average_series(records: list[dict[str, Any]], window: int) -> list[float | None]:
    values: list[float | None] = []
    rolling: list[float] = []
    for row in records:
        rolling.append(row["close"])
        if len(rolling) > window:
            rolling.pop(0)
        values.append(sum(rolling) / window if len(rolling) == window else None)
    return values


def polyline(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points if math.isfinite(x) and math.isfinite(y))


def render_svg(records: list[dict[str, Any]], unit: str) -> str:
    if len(records) < 2:
        return '<p class="empty">样本不足，无法绘制曲线。</p>'

    width, height = 920, 260
    left, right, top, bottom = 54, 20, 24, 42
    values = [row["close"] for row in records]
    ma60_values = moving_average_series(records, 60)
    plotted_values = values + [value for value in ma60_values if value is not None]
    low = min(plotted_values)
    high = max(plotted_values)
    padding = (high - low) * 0.08 or max(high * 0.02, 1)
    low -= padding
    high += padding

    def x_at(index: int) -> float:
        return left + (width - left - right) * index / (len(records) - 1)

    def y_at(value: float) -> float:
        return top + (high - value) / (high - low) * (height - top - bottom)

    price_points = [(x_at(index), y_at(value)) for index, value in enumerate(values)]
    ma_points = [
        (x_at(index), y_at(value))
        for index, value in enumerate(ma60_values)
        if value is not None
    ]
    grid_lines: list[str] = []
    for step in range(5):
        y = top + (height - top - bottom) * step / 4
        value = high - (high - low) * step / 4
        grid_lines.append(
            f'<line class="grid" x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" />'
        )
        grid_lines.append(
            f'<text class="axis" x="8" y="{y + 4:.2f}">{html.escape(fmt_number(value, 2))}</text>'
        )

    first_date = records[0]["date"]
    last_date = records[-1]["date"]
    return f"""
<svg class="history-chart" viewBox="0 0 {width} {height}" role="img" aria-label="历史曲线">
  <rect class="chart-bg" x="0" y="0" width="{width}" height="{height}" />
  {''.join(grid_lines)}
  <line class="axis-line" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" />
  <polyline class="line price-line" points="{polyline(price_points)}" />
  <polyline class="line ma-line" points="{polyline(ma_points)}" />
  <text class="date-label" x="{left}" y="{height-14}">{html.escape(first_date)}</text>
  <text class="date-label end" x="{width-right}" y="{height-14}">{html.escape(last_date)}</text>
  <text class="unit-label" x="{width-right}" y="18">{html.escape(unit)} · 收盘线 / 60日均线</text>
</svg>
"""


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# {payload['title']}",
        "",
        f"- Date: {payload['date']}",
        f"- Timezone: {payload['timezone']}",
        f"- Source: {payload['source_label']}",
        f"- Provider: [{payload['provider']['name']}]({payload['provider']['url']})",
        "",
        "> 本跟踪只处理行情曲线、收益区间、均线和回撤；公司基本面仍需回到公告、财报和交易所披露。",
        "",
        "## 跟踪表",
        "",
        "| 标的 | 类型 | 最新日期 | 最新值 | 20日 | 60日 | 120日 | 距120日高点 | 趋势 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for track in payload.get("tracks", []):
        metrics = track.get("metrics", {})
        lines.append(
            "| {name} ({ticker}) | {type} | {last_date} | {last_close} | {r20} | {r60} | {r120} | {dd} | {trend} |".format(
                name=track.get("name", ""),
                ticker=track.get("ticker", ""),
                type="主题篮子" if track.get("type") == "basket" else "单股",
                last_date=metrics.get("last_date") or "-",
                last_close=fmt_number(metrics.get("last_close"), 2),
                r20=fmt_pct(metrics.get("return_20d")),
                r60=fmt_pct(metrics.get("return_60d")),
                r120=fmt_pct(metrics.get("return_120d")),
                dd=fmt_pct(metrics.get("drawdown_from_120d_high")),
                trend=metrics.get("trend", "-"),
            )
        )
    lines.append("")

    for track in payload.get("tracks", []):
        lines.extend(
            [
                f"## {track.get('name', '')} ({track.get('ticker', '')})",
                "",
                f"- 主题：{track.get('theme', '')}",
                f"- 简讯：{signal_summary(track)}",
                f"- 说明：{track.get('note', '')}",
            ]
        )
        if track.get("source_url"):
            lines.append(f"- 行情链接：[{track['ticker']}]({track['source_url']})")
        if track.get("members"):
            lines.extend(["", "成分表现：", ""])
            for member in track["members"]:
                metrics = member.get("metrics", {})
                lines.append(
                    "- {name} ({ticker})：最新 {close}，60日 {r60}，趋势 {trend}。[行情]({url})".format(
                        name=member.get("name", ""),
                        ticker=member.get("ticker", ""),
                        close=fmt_number(metrics.get("last_close"), 2),
                        r60=fmt_pct(metrics.get("return_60d")),
                        trend=metrics.get("trend", "-"),
                        url=member.get("source_url", ""),
                    )
                )
        lines.append("")

    if payload.get("errors"):
        lines.extend(["## 数据错误", ""])
        for error in payload["errors"]:
            lines.append(f"- {error.get('name', error.get('id', 'unknown'))}: {error.get('error', '')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_html(payload: dict[str, Any]) -> str:
    rows = []
    cards = []
    for track in payload.get("tracks", []):
        metrics = track.get("metrics", {})
        rows.append(
            """
          <tr>
            <td><strong>{name}</strong><span>{ticker}</span></td>
            <td>{kind}</td>
            <td>{date}</td>
            <td>{close}</td>
            <td class="{r20_class}">{r20}</td>
            <td class="{r60_class}">{r60}</td>
            <td class="{r120_class}">{r120}</td>
            <td>{dd}</td>
            <td>{trend}</td>
          </tr>
            """.format(
                name=html.escape(track.get("name", "")),
                ticker=html.escape(track.get("ticker", "")),
                kind="主题篮子" if track.get("type") == "basket" else "单股",
                date=html.escape(metrics.get("last_date") or "-"),
                close=html.escape(fmt_number(metrics.get("last_close"), 2)),
                r20=html.escape(fmt_pct(metrics.get("return_20d"))),
                r60=html.escape(fmt_pct(metrics.get("return_60d"))),
                r120=html.escape(fmt_pct(metrics.get("return_120d"))),
                dd=html.escape(fmt_pct(metrics.get("drawdown_from_120d_high"))),
                trend=html.escape(metrics.get("trend", "-")),
                r20_class=change_class(metrics.get("return_20d")),
                r60_class=change_class(metrics.get("return_60d")),
                r120_class=change_class(metrics.get("return_120d")),
            )
        )
        member_rows = ""
        if track.get("members"):
            member_rows = "<h3>篮子成分</h3><div class=\"member-grid\">" + "".join(
                """
                <a class="member" href="{url}">
                  <span>{name}</span>
                  <strong>{ticker}</strong>
                  <em class="{klass}">{r60}</em>
                </a>
                """.format(
                    url=html.escape(member.get("source_url", "")),
                    name=html.escape(member.get("name", "")),
                    ticker=html.escape(member.get("ticker", "")),
                    klass=change_class(member.get("metrics", {}).get("return_60d")),
                    r60=html.escape(fmt_pct(member.get("metrics", {}).get("return_60d"))),
                )
                for member in track["members"]
            ) + "</div>"
        cards.append(
            """
      <section class="track-card">
        <header>
          <div>
            <p>{theme}</p>
            <h2>{name} <span>{ticker}</span></h2>
          </div>
          <div class="signal">{signal}</div>
        </header>
        {chart}
        <p class="note">{note}</p>
        {link}
        {members}
      </section>
            """.format(
                theme=html.escape(track.get("theme", "")),
                name=html.escape(track.get("name", "")),
                ticker=html.escape(track.get("ticker", "")),
                signal=html.escape(signal_summary(track)),
                chart=render_svg(track.get("records", []), "指数" if track.get("type") == "basket" else "价格"),
                note=html.escape(track.get("note", "")),
                link=(
                    f'<p class="source-link"><a href="{html.escape(track["source_url"])}">行情源链接</a></p>'
                    if track.get("source_url")
                    else ""
                ),
                members=member_rows,
            )
        )

    errors = ""
    if payload.get("errors"):
        error_items = "".join(
            f"<li>{html.escape(error.get('name', error.get('id', 'unknown')))}: {html.escape(error.get('error', ''))}</li>"
            for error in payload["errors"]
        )
        errors = f'<section class="panel error"><h2>数据错误</h2><ul>{error_items}</ul></section>'

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f7f8fb;
      --panel: #ffffff;
      --ink: #17202a;
      --muted: #5c6776;
      --line: #dce2ea;
      --accent: #2357a5;
      --accent-2: #0b7c66;
      --warn: #9c5a12;
      --bad: #b23b3b;
      --good: #13734d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
      color: var(--ink);
      background: var(--bg);
    }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 24px 16px 44px; }}
    .topline {{ display: flex; align-items: end; justify-content: space-between; gap: 16px; margin-bottom: 18px; }}
    h1 {{ font-size: 28px; line-height: 1.2; margin: 0 0 6px; letter-spacing: 0; }}
    .meta {{ color: var(--muted); font-size: 13px; margin: 0; }}
    .panel, .track-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(16, 32, 54, 0.05);
    }}
    .panel {{ padding: 16px; margin-bottom: 16px; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; min-width: 760px; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }}
    th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) {{ text-align: left; }}
    td span {{ display: block; color: var(--muted); font-size: 12px; margin-top: 2px; }}
    .track-card {{ padding: 18px; margin-bottom: 16px; }}
    .track-card header {{ display: flex; justify-content: space-between; gap: 16px; align-items: start; }}
    .track-card h2 {{ margin: 3px 0 12px; font-size: 22px; letter-spacing: 0; }}
    .track-card h2 span {{ color: var(--muted); font-size: 14px; }}
    .track-card header p {{ margin: 0; color: var(--accent); font-size: 13px; font-weight: 650; }}
    .signal {{ max-width: 380px; color: var(--muted); font-size: 13px; text-align: right; line-height: 1.5; }}
    .note {{ color: var(--muted); line-height: 1.7; }}
    .source-link a, .member {{ color: var(--accent); text-decoration: none; }}
    .history-chart {{ width: 100%; height: auto; min-height: 220px; display: block; margin: 4px 0 10px; }}
    .chart-bg {{ fill: #fbfcfe; }}
    .grid {{ stroke: #e6ebf1; stroke-width: 1; }}
    .axis-line {{ stroke: #b9c4d2; stroke-width: 1; }}
    .line {{ fill: none; stroke-linejoin: round; stroke-linecap: round; }}
    .price-line {{ stroke: var(--accent); stroke-width: 2.4; }}
    .ma-line {{ stroke: var(--accent-2); stroke-width: 1.8; stroke-dasharray: 6 5; }}
    .axis, .date-label, .unit-label {{ fill: var(--muted); font-size: 12px; }}
    .date-label.end, .unit-label {{ text-anchor: end; }}
    .member-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }}
    .member {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px; display: block; background: #fbfcfe; }}
    .member span, .member em {{ display: block; font-style: normal; color: var(--muted); font-size: 12px; }}
    .member strong {{ display: block; margin: 3px 0; color: var(--ink); }}
    .pos {{ color: var(--good); }}
    .neg {{ color: var(--bad); }}
    .flat {{ color: var(--muted); }}
    .error {{ border-color: #efc9c9; }}
    @media (max-width: 720px) {{
      .topline, .track-card header {{ display: block; }}
      .signal {{ text-align: left; max-width: none; margin-bottom: 10px; }}
      h1 {{ font-size: 23px; }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="topline">
      <div>
        <h1>{title}</h1>
        <p class="meta">{date} · {timezone} · {source_label}</p>
      </div>
      <p class="meta">行情源：<a href="{provider_url}">{provider_name}</a></p>
    </div>
    <section class="panel">
      <table>
        <thead>
          <tr>
            <th>标的</th><th>类型</th><th>最新日期</th><th>最新值</th><th>20日</th><th>60日</th><th>120日</th><th>距120日高点</th><th>趋势</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </section>
    {cards}
    {errors}
    <p class="meta">说明：本页只做指定股票/主题的历史曲线监测，不构成个性化投资建议。</p>
  </main>
</body>
</html>
""".format(
        title=html.escape(payload["title"]),
        date=html.escape(payload["date"]),
        timezone=html.escape(payload["timezone"]),
        source_label=html.escape(payload["source_label"]),
        provider_url=html.escape(payload["provider"]["url"]),
        provider_name=html.escape(payload["provider"]["name"]),
        rows="".join(rows),
        cards="".join(cards),
        errors=errors,
    )


def change_class(value: Any) -> str:
    if value is None:
        return "flat"
    if value > 0:
        return "pos"
    if value < 0:
        return "neg"
    return "flat"


def output_paths(output_dir: Path, base_name: str) -> OutputPaths:
    return OutputPaths(
        json_path=output_dir / f"{base_name}.json",
        markdown_path=output_dir / f"{base_name}.md",
        html_path=output_dir / f"{base_name}.html",
    )


def write_outputs(payload: dict[str, Any], paths: OutputPaths) -> None:
    write_json(paths.json_path, payload)
    write_text(paths.markdown_path, render_markdown(payload))
    write_text(paths.html_path, render_html(payload))


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    config = read_json(config_path)
    payload = build_payload(config, args)
    source_slug = slugify(payload["source_label"])
    dated_base = f"{payload['date']}-stock-history-tracker-from-{source_slug}"
    dated_paths = output_paths(output_dir, dated_base)
    write_outputs(payload, dated_paths)
    print(f"JSON: {dated_paths.json_path}")
    print(f"Markdown: {dated_paths.markdown_path}")
    print(f"HTML: {dated_paths.html_path}")
    if not args.no_latest:
        latest_paths = output_paths(output_dir, "stock-history-tracker-latest")
        write_outputs(payload, latest_paths)
        print(f"Latest JSON: {latest_paths.json_path}")
        print(f"Latest Markdown: {latest_paths.markdown_path}")
        print(f"Latest HTML: {latest_paths.html_path}")
    if payload.get("errors"):
        print(f"Completed with {len(payload['errors'])} data error(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
