import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

# Page title
st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content card by filling out the details below. AI will assist with tagging and summarizing.</p>
""", unsafe_allow_html=True)

# Input Fields
content_type = st.selectbox("Select Folder/Type", ["News Article", "Recipe", "Todo", "Thought", "Funny Video", "Book"])
title = st.text_input("Title")
content_link = st.text_input("Content Link or Description")
tags = st.text_input("Add hashtags (comma-separated)")

generated_summary = ""  # Placeholder for future AI generation

# Submission
if st.button("Generate Preview"):
    st.markdown("---")
    st.subheader("🔍 Preview")
    st.markdown(f"**Title**: {title}")
    st.markdown(f"**Type**: {content_type}")
    st.markdown(f"**Link/Content**: {content_link}")
    st.markdown(f"**Tags**: {tags}")
    st.markdown(f"**AI Summary**: _Coming soon: auto-generated summary based on content._")

if st.button("Save Content"):
    st.success("✅ Content saved! (This will connect to storage and database in the future)")

