import streamlit as st
import feedparser
import re
from datetime import datetime

st.set_page_config(
    page_title="Business News Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Business News Intelligence Platform")
st.subheader("AI-powered Business News Analysis")

st.info(
    "Search any company to view the latest business news from multiple trusted sources."
)

company = st.text_input(
    "Enter a company name",
    placeholder="Apple, Tesla, Microsoft, Nvidia..."
)

if st.button("Search News"):

    if company.strip() == "":
        st.warning("Please enter a company name.")
        st.stop()

    url = f"https://news.google.com/rss/search?q={company}+business"

    feed = feedparser.parse(url)

    if len(feed.entries) == 0:
        st.warning("No articles found.")

    else:
        st.success(
            f"✅ Showing top {min(10, len(feed.entries))} articles for '{company}'"
        )

        for article in feed.entries[:10]:

            with st.container(border=True):

                # ----------------------
                # Headline
                # ----------------------
                title = article.title.split(" - ")[0]

                # ----------------------
                # Source
                # ----------------------
                if hasattr(article, "source"):
                    source = article.source.title
                else:
                    source = article.title.split(" - ")[-1]

                # ----------------------
                # Published Date
                # ----------------------
                published = "Unknown"

                if hasattr(article, "published"):
                    try:
                        dt = datetime.strptime(
                            article.published,
                            "%a, %d %b %Y %H:%M:%S %Z"
                        )
                        published = dt.strftime("%d %b %Y")
                    except:
                        published = article.published[:16]

                # ----------------------
                # Display
                # ----------------------
                st.markdown(f"### 📰 {title}")
                st.markdown(f"**🏢 Source:** {source}")
                st.markdown(f"**📅 Published:** {published}")

                # ----------------------
                # Summary
                # ----------------------
                if hasattr(article, "summary"):

                    summary = re.sub(r"<[^>]+>", "", article.summary)
                    summary = summary.replace("&#39;", "'")
                    summary = summary.replace("&amp;", "&")
                    summary = summary.replace("\n", " ")
                    summary = summary.strip()

                    st.markdown("**📝 Summary**")
                    st.write(summary)

                # ----------------------
                # Article Button
                # ----------------------
                st.link_button(
                    "🔗 Read Full Article",
                    article.link
                )

                st.write("")