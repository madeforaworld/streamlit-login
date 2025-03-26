import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# Step 1: Content Type Dropdown
content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])

if content_type == "Text":
    from streamlit_quill import st_quill
    st.markdown("<small style='color: #666;'>Use the editor below for rich content — bullets, bold, headers, and checkboxes supported.</small>", unsafe_allow_html=True)
    user_content = st_quill(key="editor", theme="snow", placeholder="Start typing your thoughts here...")
elif content_type == "Link":
    user_content = st.text_input("Paste a URL (e.g. article, video, social post)")
elif content_type == "Asset":
    uploaded_file = st.file_uploader("Upload a file (PDF, image, doc, audio, etc.)")
    if uploaded_file:
        user_content = uploaded_file.name
        st.info("📁 File uploaded: " + uploaded_file.name)

# Step 4: AI Summary (editable by user)
summary = st.text_area("AI Summary", placeholder="AI-generated summary will appear here. You can edit it.")

# Step 5: AI Tags (editable tag list)
st.markdown("##### Suggested Tags")
existing_tags = ["#AI", "#mindtag", "#note", "#video", "#inspiration"]
selected_tags = st.multiselect("AI-generated tags (you can add or remove)", options=existing_tags, default=["#mindtag"])

# Submission buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Preview"):
        st.markdown("---")
        st.subheader("🔍 Preview")
        st.markdown(f"**Type**: {content_type}")
        st.markdown(f"**Folder**: {folder}")
        st.markdown(f"**Summary**: {summary}")
        st.markdown(f"**Content**: {user_content}")
        st.markdown(f"**Tags**: {', '.join(selected_tags)}")

with col2:
    if st.button("Save Content"):
        st.success("✅ Content saved! (This will connect to database in future phase)")
