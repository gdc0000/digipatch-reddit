import datetime
import re

import streamlit as st
import pandas as pd


def add_footer():
    st.markdown("---")
    st.markdown("### **Gabriele Di Cicco, PhD in Social Psychology**")
    st.markdown("""
    [GitHub](https://github.com/gdc0000) |
    [ORCID](https://orcid.org/0000-0002-1439-5790) |
    [LinkedIn](https://www.linkedin.com/in/gabriele-di-cicco-124067b0/)
    """)


def credential_inputs() -> dict:
    st.header("🔑 Reddit API Credentials")
    return {
        "client_id": st.text_input("Client ID"),
        "client_secret": st.text_input("Client Secret", type="password"),
        "username": st.text_input("Username"),
        "password": st.text_input("Password", type="password")
    }


def data_parameters() -> dict:
    st.header("📊 Data Parameters")
    params = {}
    params["subreddit"] = st.text_input("Subreddit name", value="python")
    params["sorting_methods"] = st.multiselect(
        "Sorting Methods",
        ["hot", "new", "top", "controversial", "rising"],
        default=["hot"]
    )
    params["post_limit"] = st.number_input("Number of posts to download", min_value=1, value=100, step=1)
    params["collect_comments"] = st.checkbox("Download comments as well")
    if params["collect_comments"]:
        params["comment_lim"] = st.number_input("Number of comments per post", min_value=1, value=10, step=1)
    else:
        params["remove_duplicates"] = st.checkbox("Remove duplicate posts (by Post ID)", value=True)
    return params


def generate_filename(subreddit: str) -> str:
    clean_sub = re.sub(r'\W+', '', subreddit)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"reddit_data_{clean_sub}_{timestamp}.csv"


def display_data(data_store, params):
    if not data_store.posts:
        return
    st.header("📦 Collected Data")
    if params["collect_comments"]:
        df = data_store.all_data
    else:
        df = pd.DataFrame(data_store.posts, columns=[
            "Subreddit", "Post ID", "Title", "Author", "Score",
            "Comments Count", "Upvote Ratio", "URL", "Created", "Sort Method"
        ])
        if params.get("remove_duplicates", False):
            df = df.drop_duplicates(subset=["Post ID"])
    total_instances = len(df)
    st.markdown(f"**Total instances collected: {total_instances}**")
    st.dataframe(df.head(10), use_container_width=True)

    filename = generate_filename(params["subreddit"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download CSV", data=csv, file_name=filename, mime="text/csv")


def rerun_app():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.info("Data cleared. Please refresh the page manually.")
