import streamlit as st
from datetime import datetime
from streamlit_quill import st_quill
import openai

# Set OpenAI API key securely
openai.api_key = st.secrets["openai_key"]

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# -------------------------------
# Folder Setup
# -------------------------------
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

# -------------------------------
# Content Type Selection
# -------------------------------
content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])
st.session_state["content_type"] = content_type

if folder is None and content_type == "Link":
    st.session_state.selected_folder = "News Articles"
    folder = "News Articles"

# -------------------------------
# Content Input Area
# -------------------------------
user_content
