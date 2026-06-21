import datetime
import time
from functools import wraps
from typing import List, Optional, Generator

import praw
from praw.exceptions import PRAWException
import prawcore

from .config import MAX_RETRIES, BASE_SLEEP_MULTIPLIER


def handle_rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except prawcore.exceptions.TooManyRequests:
                sleep_time = BASE_SLEEP_MULTIPLIER * (retries + 1)
                import streamlit as st
                st.warning(f"Rate limited. Retrying in {sleep_time}s...")
                time.sleep(sleep_time)
                retries += 1
        import streamlit as st
        st.error("Max retries reached. Skipping this request.")
        return None
    return wrapper


@handle_rate_limit
def initialize_reddit(client_id: str, client_secret: str,
                      username: str, password: str) -> Optional[praw.Reddit]:
    try:
        return praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=f"DigiPatch data collection (by /u/{username})",
            check_for_async=False
        )
    except PRAWException as e:
        import streamlit as st
        st.error(f"Authentication failed: {str(e)}")
        return None


def process_post(post: praw.models.Submission, subreddit: str, sorting_method: str) -> dict:
    return {
        "Subreddit": subreddit,
        "Post ID": post.id,
        "Title": post.title,
        "Author": str(post.author),
        "Score": post.score,
        "Comments Count": post.num_comments,
        "Upvote Ratio": post.upvote_ratio,
        "URL": post.url,
        "Created": datetime.datetime.fromtimestamp(post.created_utc, datetime.timezone.utc),
        "Sort Method": sorting_method
    }


def process_comment(comment: praw.models.Comment) -> dict:
    return {
        "Post ID": comment.submission.id,
        "Comment Author": str(comment.author) if comment.author else None,
        "Comment Score": comment.score,
        "Comment Body": comment.body,
        "Comment Timestamp": datetime.datetime.fromtimestamp(comment.created_utc, datetime.timezone.utc)
    }


@handle_rate_limit
def get_post_comments(post: praw.models.Submission, comment_lim: int) -> List[dict]:
    try:
        post.comments.replace_more(limit=None)
        all_comments = [c for c in post.comments.list() if isinstance(c, praw.models.Comment)]
        comments = all_comments[:comment_lim]
        return [process_comment(c) for c in comments if c.body not in ["[deleted]", "[removed]"]]
    except Exception as e:
        import streamlit as st
        st.error(f"Error retrieving comments: {str(e)}")
        return []


def collect_reddit_data(reddit: praw.Reddit,
                        subreddit: str,
                        sorting_methods: List[str],
                        post_limit: int,
                        collect_comments: bool,
                        comment_lim: int) -> Generator:
    total_operations = len(sorting_methods) * post_limit
    processed = 0
    subreddit_obj = reddit.subreddit(subreddit)
    for method in sorting_methods:
        try:
            posts = getattr(subreddit_obj, method)(limit=post_limit)
            for post in posts:
                post_data = process_post(post, subreddit, method)
                yield ("post", post_data)
                if collect_comments:
                    comments = get_post_comments(post, comment_lim)
                    for comment in comments:
                        yield ("comment", comment)
                processed += 1
                progress = processed / total_operations
                yield ("progress", progress)
        except PRAWException as e:
            import streamlit as st
            st.error(f"Error retrieving posts with method '{method}': {str(e)}")
