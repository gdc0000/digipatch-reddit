import pandas as pd


class RedditDataStore:
    def __init__(self):
        self.posts = []
        self.comments = []

    @property
    def all_data(self):
        if self.comments:
            df_posts = pd.DataFrame(self.posts, columns=[
                "Subreddit", "Post ID", "Title", "Author", "Score",
                "Comments Count", "Upvote Ratio", "URL", "Created", "Sort Method"
            ])
            df_comments = pd.DataFrame(self.comments, columns=[
                "Post ID", "Comment Author", "Comment Score",
                "Comment Body", "Comment Timestamp"
            ])
            df_comments["Comment Body"] = df_comments["Comment Body"].str.strip()
            df_comments = df_comments.drop_duplicates(subset=["Post ID", "Comment Body"])
            merged = pd.merge(df_posts, df_comments, on="Post ID", how="right")
            return merged
        else:
            return pd.DataFrame(self.posts, columns=[
                "Subreddit", "Post ID", "Title", "Author", "Score",
                "Comments Count", "Upvote Ratio", "URL", "Created", "Sort Method"
            ])
