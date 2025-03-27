import streamlit as st
from datetime import datetime
from streamlit_quill import st_quill
from openai import OpenAI
from newspaper import Article
from bs4 import BeautifulSoup
import requests
import re

# Secure OpenAI client (v1.x)
client = OpenAI(api_key=st.secrets["openai_key"])

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
user_content = ""
text_content = ""

if content_type == "Text":
    st.markdown("<small style='color: #666;'>Use the editor below for rich content — bullets, bold, headers, and checkboxes supported.</small>", unsafe_allow_html=True)
    st.markdown("##### Text")
    text_content = st_quill(key="editor_text", placeholder="Start typing your thoughts here...")
    user_content = text_content

elif content_type == "Link":
    user_content = st.text_input("Paste a URL (e.g. article, video, recipe)")
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
# Helpers: Scrape + Parse
# -------------------------------
def extract_text_from_link(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except:
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            return "\n".join([p.get_text() for p in paragraphs]).strip()
        except:
            return None

def parse_summary_and_tags(raw_output):
    tags = re.findall(r"#\w+", raw_output)
    clean_summary = re.sub(r"#\w+", '', raw_output).strip()
    return clean_summary, tags

# -------------------------------
# OpenAI Summarizer
# -------------------------------
def generate_summary(text, folder):
    if not text.strip():
        return "⚠️ No content provided."

    if folder == "Recipes":
        prompt = f"""Summarize this recipe in under 250 words. Include:
- Type of food
- Number of ingredients (list them)
- Prep/cook time
- Short description of the dish

Recipe:
{text}
"""
    elif folder == "News Articles":
        prompt = f"""Summarize the following news article in 4–5 bullet points. Include:
- What happened
- When and where it happened
- Who is involved
- Key facts or stats
- Topic and entities if possible

Article:
{text}
"""
    elif folder == "Books":
        prompt = f"""Summarize this book in under 250 words. Include:
- What the book is about
- Themes or structure
- Type of book (e.g. fiction, memoir)
- Key takeaway or message

Book:
{text}
"""
    else:
        prompt = f"""Summarize this personal note or text. Include:
- What it's about
- Any key actions, plans, or ideas
- Tone or purpose (todo, reflection, brainstorm)
- 2–3 suggested tags (as hashtags at the end)

Note:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

# -------------------------------
# Generate AI Summary
# -------------------------------
if st.button("🧠 Generate AI Summary"):
    if content_type == "Link":
        article_text = extract_text_from_link(user_content)
        if article_text:
            text_to_summarize = article_text
        else:
            st.warning("Could not extract content from link. Using fallback notes.")
            text_to_summarize = text_content
    else:
        text_to_summarize = text_content

    if text_to_summarize:
        with st.spinner("Generating summary with OpenAI..."):
            try:
                summary_result = generate_summary(text_to_summarize, folder)
                clean_summary, extracted_tags = parse_summary_and_tags(summary_result)
                st.session_state["ai_summary"] = clean_summary
                st.session_state["ai_tags"] = extracted_tags
                st.success("✅ Summary generated!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter content or notes to summarize.")

# -------------------------------
# Summary Box
# -------------------------------
summary = st.text_area("AI Summary", value=st.session_state.get("ai_summary", ""), placeholder="AI-generated summary will appear here. You can edit it.")

# -------------------------------
# Tag Selection
# -------------------------------
st.markdown("##### Suggested Tags")
existing_tags = ["#AI", "#mindtag", "#note", "#video", "#inspiration"]
default_tags = st.session_state.get("ai_tags", ["#mindtag"])
selected_tags = st.multiselect("AI-generated tags (you can add or remove)", options=existing_tags + default_tags, default=default_tags)

# -------------------------------
# Preview + Save
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
