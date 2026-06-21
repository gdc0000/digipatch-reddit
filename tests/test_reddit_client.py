import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from src.reddit_client import (
    handle_rate_limit, process_post, process_comment,
    initialize_reddit, get_post_comments,
)


class TestHandleRateLimit(unittest.TestCase):
    def test_passes_through_on_success(self):
        fn = Mock(return_value="ok")

        @handle_rate_limit
        def d():
            return fn()

        self.assertEqual(d(), "ok")
        self.assertEqual(fn.call_count, 1)

    @patch("src.reddit_client.time.sleep")
    @patch("src.reddit_client.prawcore")
    def test_returns_none_after_exhaustion(self, pc, _):
        pc.exceptions.TooManyRequests = type("TooManyRequests", (Exception,), {})
        fn = Mock(side_effect=pc.exceptions.TooManyRequests)

        @handle_rate_limit
        def d():
            return fn()

        with patch("src.reddit_client.MAX_RETRIES", 3):
            self.assertIsNone(d())

    def test_propagates_non_rate_exception(self):
        @handle_rate_limit
        def d():
            raise ValueError("unexpected")

        with self.assertRaises(ValueError):
            d()


_sub = SimpleNamespace(
    id="abc123", title="T", author="u1", score=42,
    num_comments=5, upvote_ratio=0.9, url="https://r/abc123",
    created_utc=1704067200,
)
_cmt = SimpleNamespace(
    submission=SimpleNamespace(id="abc123"),
    author="u2", score=10, body="Great post!", created_utc=1704153600,
)


class TestProcessPost(unittest.TestCase):
    def test_returns_dict_with_all_keys(self):
        r = process_post(_sub, "test", "hot")
        self.assertEqual(set(r.keys()), {
            "Subreddit", "Post ID", "Title", "Author", "Score",
            "Comments Count", "Upvote Ratio", "URL", "Created", "Sort Method"
        })
        self.assertEqual(r["Score"], 42)

    def test_author_is_string(self):
        self.assertIsInstance(process_post(_sub, "t", "n")["Author"], str)


class TestProcessComment(unittest.TestCase):
    def test_returns_dict_with_all_keys(self):
        r = process_comment(_cmt)
        self.assertEqual(set(r.keys()), {
            "Post ID", "Comment Author", "Comment Score",
            "Comment Body", "Comment Timestamp"
        })
        self.assertEqual(r["Comment Body"], "Great post!")

    def test_none_author(self):
        cmt = SimpleNamespace(**_cmt.__dict__ | {"author": None})
        self.assertIsNone(process_comment(cmt)["Comment Author"])


class TestInitializeReddit(unittest.TestCase):
    @patch("src.reddit_client.praw.Reddit")
    def test_calls_praw_with_credentials(self, m):
        instance = Mock()
        m.return_value = instance
        self.assertIs(initialize_reddit("cid", "csec", "u", "p"), instance)
        m.assert_called_once_with(
            client_id="cid", client_secret="csec", username="u", password="p",
            user_agent="DigiPatch data collection (by /u/u)", check_for_async=False,
        )


def _mock_comment(body="Great post!"):
    c = Mock()
    c.body = body
    c.score = 10
    c.created_utc = 1704153600
    c.author = "u2"
    c.submission.id = "abc123"
    return c


class TestGetPostComments(unittest.TestCase):
    @patch("src.reddit_client.praw.models")
    def test_filters_deleted_and_removed(self, m):
        m.Comment = Mock
        s = Mock()
        s.comments.replace_more = Mock()
        s.comments.list.return_value = [
            _mock_comment("[deleted]"),
            _mock_comment("[removed]"),
            _mock_comment("Real"),
        ]
        bodies = [c["Comment Body"] for c in get_post_comments(s, 10)]
        self.assertNotIn("[deleted]", bodies)
        self.assertNotIn("[removed]", bodies)
        self.assertIn("Real", bodies)
