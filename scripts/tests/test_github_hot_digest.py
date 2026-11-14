import json
import sys
import tempfile
import threading
import unittest
from datetime import date, datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generate_github_hot_digest as g  # noqa: E402

TODAY = date(2026, 11, 14)


def make_repo(name: str, stars: int = 1000, **kwargs) -> g.RepositorySnapshot:
    defaults = dict(
        full_name=name,
        html_url=f"https://github.com/{name}",
        description="A useful thing",
        owner_login=name.split("/")[0].lower(),
        owner_type="User",
        owner_url="",
        stargazers_count=stars,
        forks_count=10,
        language="Python",
        topics=[],
        homepage="",
        pushed_at=datetime(2026, 11, 13, tzinfo=timezone.utc),
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    defaults.update(kwargs)
    return g.RepositorySnapshot(**defaults)


class FakeClient:
    def __init__(self, releases=None):
        self.releases = releases or {}

    def latest_release(self, full_name):
        return self.releases.get(full_name)


class TrendingTest(unittest.TestCase):
    def test_parses_name_and_stars_today(self):
        html = """
        <article class="Box-row"><h2 class="h3"> <a data-x="1" href="/acme/rocket">acme / rocket</a></h2>
        <span>1,925 stars today</span></article>
        <article class="Box-row"><h2><a href="/solo/quiet">x</a></h2></article>
        """
        self.assertEqual(g.parse_trending_html(html), {"acme/rocket": 1925, "solo/quiet": 0})


class StarGainTest(unittest.TestCase):
    def test_snapshot_delta_beats_total_stars(self):
        repo = make_repo("a/b", stars=1500)
        g.apply_star_gains(repo, {"2026-11-13": {"a/b": 1200}, "2026-11-10": {"a/b": 900}}, TODAY, 30)
        self.assertEqual((repo.daily_gain, repo.daily_gain_source), (300.0, "snapshot"))
        self.assertEqual((repo.weekly_gain, repo.weekly_gain_days), (600, 4))

    def test_trending_wins_and_new_repo_falls_back_to_average(self):
        hot = make_repo("a/hot", trending_stars_today=800)
        g.apply_star_gains(hot, {"2026-11-13": {"a/hot": 900}}, TODAY, 30)
        self.assertEqual(hot.daily_gain_source, "trending")

        young = make_repo("a/young", stars=1000, created_at=datetime(2026, 11, 4, tzinfo=timezone.utc))
        g.apply_star_gains(young, {}, TODAY, 30)
        self.assertEqual((young.daily_gain, young.daily_gain_source), (100.0, "average"))

        old = make_repo("a/old", stars=90000)
        g.apply_star_gains(old, {}, TODAY, 30)
        self.assertIsNone(old.daily_gain)

    def test_snapshots_are_pruned_and_today_is_replaced(self):
        kept = g.update_snapshots(
            {"2026-10-01": {"a/b": 1}, "2026-11-13": {"a/b": 2}, "2026-11-14": {"a/b": 3}},
            TODAY,
            [make_repo("a/b", stars=9)],
        )
        self.assertEqual(kept, {"2026-11-13": {"a/b": 2}, "2026-11-14": {"a/b": 9}})


class RankingTest(unittest.TestCase):
    def rank(self, repos, ledger, releases=None, snapshots=None):
        return g.rank_repositories(FakeClient(releases), repos, g.Settings(), TODAY, snapshots or {}, ledger)

    def test_fast_small_repo_outranks_big_static_one(self):
        giant = make_repo("big/giant", stars=120000)
        riser = make_repo("new/riser", stars=900, trending_stars_today=400)
        selection = self.rank([giant, riser], {})
        self.assertEqual(selection.featured[0].full_name, "new/riser")

    def test_cooldown_moves_repo_to_watchlist(self):
        repo = make_repo("a/regular", trending_stars_today=500)
        fresh = make_repo("b/fresh", trending_stars_today=50)
        selection = self.rank([repo, fresh], {"a/regular": {"dates": ["2026-11-10"], "release_tag": "v1.2.0"}})
        self.assertEqual([r.full_name for r in selection.featured], ["b/fresh"])
        self.assertEqual([r.full_name for r in selection.watching], ["a/regular"])

    def test_cooldown_expires(self):
        repo = make_repo("a/regular", trending_stars_today=500)
        selection = self.rank([repo], {"a/regular": {"dates": ["2026-10-01"], "release_tag": ""}})
        self.assertEqual([r.full_name for r in selection.featured], ["a/regular"])

    def test_major_release_breaks_cooldown_but_patch_does_not(self):
        ledger = {
            "a/major": {"dates": ["2026-11-10"], "release_tag": "v1.9.3"},
            "a/patch": {"dates": ["2026-11-10"], "release_tag": "v1.9.3"},
        }
        published = datetime(2026, 11, 13, tzinfo=timezone.utc)
        releases = {
            "a/major": g.ReleaseInfo("u", published, "v2.0.0"),
            "a/patch": g.ReleaseInfo("u", published, "v1.9.4"),
        }
        repos = [make_repo("a/major", trending_stars_today=100), make_repo("a/patch", trending_stars_today=100)]
        selection = self.rank(repos, ledger, releases)
        self.assertEqual([r.full_name for r in selection.featured], ["a/major"])
        self.assertIn("v2.0.0", selection.featured[0].refeature_reason)

    def test_one_repo_per_owner(self):
        repos = [make_repo("o/a", trending_stars_today=300), make_repo("o/b", trending_stars_today=200)]
        self.assertEqual([r.full_name for r in self.rank(repos, {}).featured], ["o/a"])


class LedgerTest(unittest.TestCase):
    def test_bootstrap_from_old_digests_and_same_day_rerun(self):
        with tempfile.TemporaryDirectory() as tmp:
            digests = Path(tmp)
            (digests / "github-hot-2026-11-13.md").write_text(
                "### 1. github/gh-aw | 📌 持续热门（连续 6 天） | 综合评分 240.0\n", encoding="utf-8"
            )
            ledger_path = digests / "ledger.json"
            ledger = g.load_ledger(ledger_path, digests, TODAY)
            self.assertEqual(ledger, {"github/gh-aw": {"dates": ["2026-11-13"], "release_tag": ""}})

            g.record_featured(ledger, [make_repo("x/y")], TODAY)
            g.save_json(ledger_path, ledger)
            again = g.load_ledger(ledger_path, digests, TODAY)
            self.assertNotIn("x/y", again)  # today's earlier run is forgotten
            self.assertIn("github/gh-aw", again)

    def test_parse_version(self):
        self.assertEqual(g.parse_version("@openai/agents-extensions@0.22.0"), (0, 22))
        self.assertEqual(g.parse_version("v3.1.4"), (3, 1))
        self.assertIsNone(g.parse_version("nightly"))


class LLMTest(unittest.TestCase):
    def test_parse_handles_code_fences_and_garbage(self):
        fenced = "```json\n{\"one_liner\": \"好用\", \"problem\": \"p\"}\n```"
        self.assertEqual(g.parse_llm_json(fenced)["one_liner"], "好用")
        self.assertIsNone(g.parse_llm_json("sorry, I cannot"))
        self.assertIsNone(g.parse_llm_json("{}"))

    def test_roundtrip_against_openai_compatible_stub_and_failure_fallback(self):
        seen = {}

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen.update(path=self.path, auth=self.headers["Authorization"], model=body["model"])
                content = json.dumps({"one_liner": "一句话", "problem": "问题", "risks": "风险"})
                payload = json.dumps({"choices": [{"message": {"content": content}}]}).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{server.server_port}/v1"
            review = g.llm_commentary(g.LLMConfig("k", base, "some-model"), make_repo("a/b"), "# readme")
        finally:
            server.shutdown()
            server.server_close()
        self.assertEqual(seen, {"path": "/v1/chat/completions", "auth": "Bearer k", "model": "some-model"})
        self.assertEqual(review["one_liner"], "一句话")
        self.assertEqual(review["audience"], "")

        dead = g.LLMConfig("k", "http://127.0.0.1:9/v1", "m")
        self.assertIsNone(g.llm_commentary(dead, make_repo("a/b"), ""))


class RenderTest(unittest.TestCase):
    def test_layout_with_and_without_review(self):
        top = make_repo("a/top", trending_stars_today=500, description='Say "hi"')
        top.reasons = ["GitHub Trending 今日 +500 Stars"]
        top.daily_gain, top.daily_gain_source = 500.0, "trending"
        brief = make_repo("b/brief")
        watch = make_repo("c/watch", last_featured=date(2026, 11, 1))
        selection = g.Selection(featured=[top, brief], watching=[watch])

        plain = g.render_digest(selection, g.Settings(), TODAY, {}, {"a/top": "```\npip install top\n```"})
        self.assertIn("## 今日主推：[a/top]", plain)
        self.assertIn("pip install top", plain)
        self.assertIn("### 1. b/brief", plain)
        self.assertIn("| [c/watch](https://github.com/c/watch) | 1,000 | — | 2026-11-01 |", plain)
        title = next(line for line in plain.splitlines() if line.startswith("title: "))
        self.assertEqual(json.loads(title[len("title: "):]), 'GitHub 热点 2026-11-14｜top：Say "hi"')

        review = {key: "" for key in g.LLM_FIELDS}
        review.update(one_liner="值得一看", problem="解决 X")
        rich = g.render_digest(selection, g.Settings(), TODAY, {"a/top": review}, {})
        self.assertIn("> 值得一看", rich)
        self.assertIn("**它解决什么问题**", rich)
        self.assertIn("点评由 LLM", rich)

    def test_empty_day_still_renders(self):
        text = g.render_digest(g.Selection([], []), g.Settings(), TODAY)
        self.assertIn("今日无新上榜项目", text)


if __name__ == "__main__":
    unittest.main()
