import streamlit as st
from datetime import datetime
from streamlit_quill import st_quill

st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# --------------------------------------
# Folder State & Dropdown
# --------------------------------------

if "folder_list" not in st.session_state:
    st.session_state.folder_list = ["News Articles", "Recipes", "Todo", "Thoughts", "Funny Videos", "Books"]

if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = st.session_state.folder_list[0]

if "creating_folder" not in st.session_state:
    st.session_state.creating_folder = False

folder_options = st.session_state.folder_list + ["➕ Create New Folder"]

st.markdown("#### Select Folder")
selected_folder = st.selectbox(
    "Choose a folder",
    folder_options,
    index=folder_options.index(st.session_state.selected_folder)
    if st.session_state.selected_folder in folder_options else 0
)

if selected_folder == "➕ Create New Folder":
    st.session_state.creating_folder = True
else:
    st.session_state.selected_folder = selected_folder
    st.session_state.creating_folder = False

if st.session_state.creating_folder:
    new_folder = st.text_input("Name your new folder:")
    if new_folder:
        st.session_state.folder_list.append(new_folder)
        st.session_state.selected_folder = new_folder
        st.session_state.creating_folder = False
        st.success(f"✅ Folder '{new_folder}' created and selected.")

folder = st.session_state.selected_folder

# --------------------------------------
# Content Type Selection
# --------------------------------------

content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])
st.session_state["content_type"] = content_type

# Auto-select default folder for Link type
if folder is None and content_type == "Link":
    default_folder = "News Articles"
    st.session_state.selected_folder = default_folder
    folder = default_folder

# --------------------------------------
# Content Input Area
# --------------------------------------

user_content = ""
text_content = ""

if content_type == "Text":
    st.markdown("<small style='color: #666;'>Use the editor below for rich content — bullets, bold, headers, and checkboxes supported.</small>", unsafe_allow_html=True)
    st.markdown("##### Text")
    text_content = st_quill(key="editor_text", placeholder="Start typing your thoughts here...")
    user_content = text_content

elif content_type == "Link":
    user_content = st.text_input("Paste a URL (e.g. article, video, social post)")
    st.markdown("##### Text")
    text_content = st_quill(key="editor_link", placeholder="Write any personal notes or context about this link.")

elif content_type == "Asset":
    uploaded_file = st.file_uploader("Upload a file (PDF, image, doc, audio, etc.)")
    if uploaded_file:
        user_content = uploaded_file.name
        st.info("📁 File uploaded: " + uploaded_file.name)

    st.markdown("##### Text")
    text_content = st_quill(key="editor_asset", placeholder="Write any thoughts, context, or observations about this file.")

# --------------------------------------
# AI
