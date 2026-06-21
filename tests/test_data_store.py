import unittest

from src.data_store import RedditDataStore


class TestRedditDataStore(unittest.TestCase):
    def setUp(self):
        self.store = RedditDataStore()

    def test_init_posts_empty(self):
        self.assertEqual(self.store.posts, [])

    def test_init_comments_empty(self):
        self.assertEqual(self.store.comments, [])

    def test_all_data_no_posts_no_comments(self):
        df = self.store.all_data
        self.assertTrue(df.empty)
        self.assertIn("Subreddit", df.columns)

    def test_all_data_posts_only(self):
        self.store.posts.append({
            "Subreddit": "test", "Post ID": "abc123", "Title": "Test Post",
            "Author": "user1", "Score": 42, "Comments Count": 5,
            "Upvote Ratio": 0.9, "URL": "https://reddit.com/r/test/abc123",
            "Created": "2024-01-01", "Sort Method": "hot"
        })
        df = self.store.all_data
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Post ID"], "abc123")
        self.assertNotIn("Comment Author", df.columns)

    def test_all_data_with_comments(self):
        self.store.posts.append({
            "Subreddit": "test", "Post ID": "abc123", "Title": "Test Post",
            "Author": "user1", "Score": 42, "Comments Count": 5,
            "Upvote Ratio": 0.9, "URL": "https://reddit.com/r/test/abc123",
            "Created": "2024-01-01", "Sort Method": "hot"
        })
        self.store.comments.append({
            "Post ID": "abc123", "Comment Author": "user2",
            "Comment Score": 10, "Comment Body": "Great post!",
            "Comment Timestamp": "2024-01-02"
        })
        df = self.store.all_data
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Comment Body"], "Great post!")
        self.assertIn("Comment Author", df.columns)

    def test_all_data_deduplicates_comments(self):
        self.store.posts.append({
            "Subreddit": "test", "Post ID": "abc123", "Title": "Test Post",
            "Author": "user1", "Score": 42, "Comments Count": 5,
            "Upvote Ratio": 0.9, "URL": "https://reddit.com/r/test/abc123",
            "Created": "2024-01-01", "Sort Method": "hot"
        })
        duplicate_body = "Duplicate comment"
        self.store.comments.append({
            "Post ID": "abc123", "Comment Author": "user2",
            "Comment Score": 10, "Comment Body": duplicate_body,
            "Comment Timestamp": "2024-01-02"
        })
        self.store.comments.append({
            "Post ID": "abc123", "Comment Author": "user2",
            "Comment Score": 10, "Comment Body": duplicate_body,
            "Comment Timestamp": "2024-01-02"
        })
        df = self.store.all_data
        self.assertEqual(len(df), 1)
