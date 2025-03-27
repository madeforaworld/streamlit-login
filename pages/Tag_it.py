import streamlit as st
from datetime import datetime
from streamlit_quill import st_quill
from transformers import pipeline

# -------------------------------
# Set page config
# -------------------------------
st.set_page_config(page_title="Tag It | MindTag", layout="wide", page_icon="🏷️")

st.markdown("""
    <h2 style='margin-top: 0;'>📝 Tag It</h2>
    <p style='color: #555;'>Create a new content item. Content type determines how it's processed by AI.</p>
""", unsafe_allow_html=True)

# -------------------------------
# Initialize summarizer
# -------------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def generate_summary(text, folder):
    if folder == "Recipes":
        prompt = f"""Summarize this recipe in 250 words or less.
Include:
- Type of food
- Number of ingredients (list them at a high level)
- Prep/cook time
- Short description of the dish

Content:
{text}
"""

    elif folder == "News Articles":
        prompt = f"""Summarize this news article.
Include:
- Main event
- When it happened
- Who is involved
- Key facts
- Date, topic, or people mentioned

Content:
{text}
"""

    elif folder == "Books":
        prompt = f"""Summarize this book in under 250 words.
Include:
- What it's about
- Themes or structure
- Type of book (e.g. fiction, memoir)
- Key takeaway or message

Content:
{text}
"""

    else:
        prompt = f"""This is a personal note, thought, to-do list or general content.
Summarize it in under 200 words.
Include:
- General topic or purpose
- Any actions or ideas
- Tone (reflective, to-do, creative)
- Suggest 2–3 topic tags

Content:
{text}
"""

    result = summarizer(prompt, max_length=200, min_length=50, do_sample=False)
    return result[0]["summary_text"]

# -------------------------------
# Folder setup
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
# Content Type selection
# -------------------------------
content_type = st.selectbox("Choose content type", ["Text", "Link", "Asset"])
st.session_state["content_type"] = content_type

if folder is None and content_type == "Link":
    st.session_state.selected_folder = "News Articles"
    folder = "News Articles"

# -------------------------------
# Content input area
# -------------------------------
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

# -------------------------------
# Generate AI Summary (Hugging Face)
# -------------------------------
if st.button("🧠 Generate AI Summary"):
    if text_content:
        with st.spinner("Generating summary with Hugging Face..."):
            summary_result = generate_summary(text_content, folder)
            st.session_state["ai_summary"] = summary_result
            st.success("✅ Summary generated!")
    else:
        st.warning("Please enter some text content first.")

summary = st.text_area("AI Summary", value=st.session_state.get("ai_summary", ""), placeholder="AI-generated summary will appear here. You can edit it.")

# -------------------------------
# Tag selection
# -------------------------------
st.markdown("##### Suggested Tags")
existing_tags = ["#AI", "#mindtag", "#note", "#video", "#inspiration"]
selected_tags = st.multiselect("AI-generated tags (you can add or remove)", options=existing_tags, default=["#mindtag"])

# -------------------------------
# Submission area
# -------------------------------
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
            <p><strong>Text:</strong><br>{text_content}</p>
            <p><strong>Tags:</strong> {' '.join(selected_tags)}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.button("Save Content"):
        st.success("✅ Content saved! (This will connect to database in future phase)")
