import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# Step 1: Content Type Dropdown
folder_list = ["News Articles", "Recipes", "Todo", "Thoughts", "Funny Videos", "Books"]
selected_folder = st.session_state.get("selected_folder", None)

st.markdown("#### Select Folder")
st.markdown("<small style='color:#999;'>Click a folder below or create a new one.</small>", unsafe_allow_html=True)

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
    background-color: #3366FF;
    color: white;
    border-color: #3366FF;
}
</style>
""", unsafe_allow_html=True)

selected_folder = st.session_state.get("selected_folder", None)

st.markdown("#### Select Folder")

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
    background-color: #3366FF;
    color: white;
    border-color: #3366FF;
}
</style>
""", unsafe_allow_html=True)

folder_area = st.empty()
selected_folder = st.session_state.get("selected_folder", None)
creating_folder = st.session_state.get("creating_folder", False)

# Render folder chips inline using real Streamlit buttons
st.markdown("""
<style>
.folder-chip {
    padding: 6px 14px;
    border-radius: 20px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    font-size: 0.85rem;
    font-weight: 500;
    color: #333;
    cursor: pointer;
    transition: 0.2s ease;
    display: inline-block;
    margin: 4px 6px 4px 0;
    text-align: center;
}
.folder-chip.selected {
    background-color: #3366FF;
    color: white;
    border-color: #3366FF;
}
</style>
""", unsafe_allow_html=True)

st.markdown("#### Select Folder")

folder_cols = st.columns(len(folder_list) + 1)
for i, f in enumerate(folder_list):
    with folder_cols[i]:
        if st.button(f, key=f"folder_{f}"):
            st.session_state["selected_folder"] = f
        if st.session_state.get("selected_folder") == f:
            st.markdown(f"<div class='folder-chip selected'>{f}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='folder-chip'>{f}</div>", unsafe_allow_html=True)

with folder_cols[-1]:
    if st.button("➕ Create", key="folder_create"):
        st.session_state["creating_folder"] = True

if st.session_state.get("creating_folder"):
    new_folder = st.text_input("Name your new folder:", key="new_folder_input")
    if new_folder:
        folder_list.append(new_folder)
        st.session_state["selected_folder"] = new_folder
        st.session_state["creating_folder"] = False
        st.success(f"✅ Folder '{new_folder}' created and selected.")

folder = st.session_state.get("selected_folder")


folder = st.session_state.get("selected_folder")

st.markdown("<small style='color:#999;'>Click a folder above or create a new one below.</small>", unsafe_allow_html=True)

# Auto-select folder if content type is Link
if folder is None and 'Link' in st.session_state.get("content_type", ""):
    folder = "News Articles"
    st.session_state["selected_folder"] = folder




content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])

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

# Step 4: AI Summary (editable by user)
if st.button("🧠 Generate AI Summary"):
    st.info("AI will soon analyze your content and generate a summary here.")

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
        st.markdown("""
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
