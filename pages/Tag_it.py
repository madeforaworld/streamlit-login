import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# -------------------------
# Folder Selection Section
# -------------------------

st.markdown("#### Select Folder")
st.markdown("<small style='color:#999;'>Click a folder below or create a new one.</small>", unsafe_allow_html=True)

# Folder chip styling
st.markdown("""
<style>
.folder-chip {
    display: inline-block;
    background-color: #f0f0f0;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 4px 6px 4px 0;
    font-size: 0.85rem;
    font-weight: 500;
    color: #333;
    border: 1px solid #ccc;
    cursor: pointer;
    text-align: center;
}
.folder-chip.selected {
    background-color: #3366FF !important;
    color: white !important;
    border-color: #3366FF !important;
}
</style>
""", unsafe_allow_html=True)

# Folder state setup
if "folder_list" not in st.session_state:
    st.session_state.folder_list = ["News Articles", "Recipes", "Todo", "Thoughts", "Funny Videos", "Books"]
if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = None
if "creating_folder" not in st.session_state:
    st.session_state.creating_folder = False

# Render folder chips and create button
folder_area = st.container()
with folder_area:
    cols = st.columns(len(st.session_state.folder_list) + 1)
    for i, f in enumerate(st.session_state.folder_list):
        with cols[i]:
            chip_class = "folder-chip selected" if st.session_state.selected_folder == f else "folder-chip"
            if st.button(f, key=f"folder_{f}"):
                st.session_state.selected_folder = f
            st.markdown(f"<div class='{chip_class}'>{f}</div>", unsafe_allow_html=True)

    # "Create" chip
    with cols[-1]:
        if not st.session_state.creating_folder:
            if st.button("➕ Create", key="create_folder_btn"):
                st.session_state.creating_folder = True
        else:
            new_folder = st.text_input("New folder name", key="new_folder_input")
            if new_folder:
                st.session_state.folder_list.append(new_folder)
                st.session_state.selected_folder = new_folder
                st.session_state.creating_folder = False
                st.success(f"✅ Folder '{new_folder}' created and selected.")

folder = st.session_state.selected_folder

# -------------------------
# Content Type Selection
# -------------------------

content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])
st.session_state["content_type"] = content_type

# Auto-select default folder for link
if folder is None and content_type == "Link":
    folder = "News Articles"
    st.session_state.selected_folder = folder

# -------------------------
# Content Input Area
# -------------------------

if content_type == "Text":
    from streamlit_quill import st_quill
    st.markdown("<small style='color: #666;'>Use the editor below for rich content — bullets, bold, headers, and checkboxes supported.</small>", unsafe_allow_html=True)
    user_content = st_quill(key="editor", placeholder="Start typing your thoughts here...")

elif content_type == "Link":
    user_content = st.text_input("Paste a URL (e.g. article, video, social post)")
    link_notes = st.text_area("Optional Notes", placeholder="Write any personal notes or context about this link.")

elif content_type == "Asset":
    uploaded_file = st.file_uploader("Upload a file (PDF, image, doc, audio, etc.)")
    if uploaded_file:
        user_content = uploaded_file.name
        st.info("📁 File uploaded: " + uploaded_file.name)
        asset_notes = st.text_area("Optional Notes", placeholder="Write any thoughts, context, or observations about this file.")

# -------------------------
# AI Summary & Tags
# -------------------------

if st.button("🧠 Generate AI Summary"):
    st.info("AI will soon analyze your content and generate a summary here.")

summary = st.text_area("AI Summary", placeholder="AI-generated summary will appear here. You can edit it.")

st.markdown("##### Suggested Tags")
existing_tags = ["#AI", "#mindtag", "#note", "#video", "#inspiration"]
selected_tags = st.multiselect("AI-generated tags (you can add or remove)", options=existing_tags, default=["#mindtag"])

# -------------------------
# Submission Section
# -------------------------

col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Preview"):
        st.markdown("---")
        st.markdown(f"""
        <div style='border: 1px solid #ddd; border-radius: 12px; padding: 1rem; background-color: #fefefe;'>
            <h4>🔍 Preview</h4>
            <p><strong>Type:</strong> {content_type}</p>
            <p><strong>Folder:</strong> {folder}</p>
            <p><strong>Summary:</strong> {summary}</p>
            <p><strong>Content:</strong><br>{user_content}</p>
            <p><strong>Tags:</strong> {' '.join(selected_tags)}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.button("Save Content"):
        st.success("✅ Content saved! (This will connect to database in future phase)")
