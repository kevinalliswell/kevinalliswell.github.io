import sys
import unittest
import urllib.error
from datetime import datetime
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generate_ai_digest as a  # noqa: E402

TZ = ZoneInfo("Asia/Shanghai")
NOW = datetime(2026, 11, 14, 9, 0, tzinfo=TZ)
GOOD_FEED = """<?xml version="1.0"?><rss><channel><item>
<title>New AI model released</title><link>https://example.com/a</link>
<description>An agent model</description><pubDate>Fri, 13 Nov 2026 08:00:00 GMT</pubDate>
</item></channel></rss>"""


def source(name: str) -> a.SourceConfig:
    return a.SourceConfig(name=name, site_url="", feed_url=f"https://feeds.test/{name}", mode="feed_items")


def collect(responses: dict, names: list) -> list:
    calls = {}

    def fake_fetch(url: str) -> str:
        name = url.rsplit("/", 1)[-1]
        calls[name] = calls.get(name, 0) + 1
        result = responses[name]
        if isinstance(result, list):
            result = result[min(calls[name], len(result)) - 1]
        if isinstance(result, Exception):
            raise result
        return result

    with mock.patch.object(a, "fetch_text", fake_fetch), mock.patch.object(sys, "stderr"):
        items = a.collect_candidates([source(n) for n in names], TZ, NOW, retry_delay=0)
    return items, calls


class CollectCandidatesTest(unittest.TestCase):
    def test_bad_source_is_skipped_and_the_rest_still_publish(self):
        # The failure seen in CI: a feed answered with something that is not XML.
        items, calls = collect({"good": GOOD_FEED, "broken": "\x1f\x8b not xml"}, ["broken", "good"])
        self.assertEqual([item.source_name for item in items], ["good"])
        self.assertEqual(calls["broken"], 2)  # retried once before giving up

    def test_network_error_is_skipped(self):
        error = urllib.error.URLError("connection reset")
        items, _ = collect({"good": GOOD_FEED, "down": error}, ["down", "good"])
        self.assertEqual(len(items), 1)

    def test_transient_failure_recovers_on_retry(self):
        items, calls = collect({"flaky": ["<html>challenge", GOOD_FEED]}, ["flaky"])
        self.assertEqual(len(items), 1)
        self.assertEqual(calls["flaky"], 2)

    def test_leading_bom_and_whitespace_are_tolerated(self):
        items, calls = collect({"bom": "\ufeff\n" + GOOD_FEED}, ["bom"])
        self.assertEqual((len(items), calls["bom"]), (1, 1))

    def test_all_sources_failing_is_still_an_error(self):
        with self.assertRaises(RuntimeError):
            collect({"x": "nope", "y": "nope"}, ["x", "y"])


class DecodeBodyTest(unittest.TestCase):
    def test_unrequested_gzip_is_decompressed(self):
        import gzip

        packed = gzip.compress(GOOD_FEED.encode("utf-8"))
        self.assertEqual(a.decode_body(packed, "gzip", "utf-8"), GOOD_FEED)
        self.assertEqual(a.decode_body(packed, None, "utf-8"), GOOD_FEED)  # header missing

    def test_plain_body_and_mislabelled_body_pass_through(self):
        self.assertEqual(a.decode_body(GOOD_FEED.encode("utf-8"), None, "utf-8"), GOOD_FEED)
        self.assertEqual(a.decode_body(b"<rss/>", "gzip", "utf-8"), "<rss/>")


if __name__ == "__main__":
    unittest.main()
