import streamlit as st

from .data_store import RedditDataStore
from .reddit_client import initialize_reddit, collect_reddit_data
from .ui import add_footer, credential_inputs, data_parameters, display_data, rerun_app


def main():
    if "data_store" not in st.session_state:
        st.session_state.data_store = RedditDataStore()

    st.image("DigiPatchLogo.png", width=700)
    st.title("WP4 DigiPatch: Reddit Data Collection")
    st.markdown("Collect Reddit data with resumable progress and smart rate limit handling.")

    creds = credential_inputs()
    params = data_parameters()

    if st.button("🚀 Start/Resume Collection"):
        if not all(creds.values()):
            st.error("Missing API credentials!")
            return

        reddit = initialize_reddit(**creds)
        if not reddit:
            return

        data_gen = collect_reddit_data(
            reddit=reddit,
            subreddit=params["subreddit"],
            sorting_methods=params["sorting_methods"],
            post_limit=params["post_limit"],
            collect_comments=params["collect_comments"],
            comment_lim=params.get("comment_lim", 0)
        )

        progress_bar = st.progress(0)
        with st.spinner("Collecting data..."):
            try:
                for record in data_gen:
                    record_type, data = record
                    if record_type == "post":
                        st.session_state.data_store.posts.append(data)
                    elif record_type == "comment":
                        st.session_state.data_store.comments.append(data)
                    elif record_type == "progress":
                        progress_bar.progress(min(data, 1.0))
            except Exception as e:
                st.error(f"Collection failed: {str(e)}")
        st.success("Collection complete!")

    display_data(st.session_state.data_store, params)

    if st.session_state.data_store.posts and st.button("❌ Clear Data"):
        st.session_state.data_store = RedditDataStore()
        rerun_app()

    add_footer()


if __name__ == "__main__":
    main()
