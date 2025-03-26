import streamlit as st
from datetime import datetime, timedelta
import random

# --- Fake User Info ---
user_name = "Percy Plum"
user_avatar_url = "https://e7.pngegg.com/pngimages/687/86/png-clipart-google-logo-google-adwords-g-suite-google-account-google-logo-chess.png"
linked_drive = "Percy Google Drive"
drive_icon = "https://www.gstatic.com/marketing-cms/assets/images/e8/4f/69d708b2455397d7b88b0312f7c5/google-drive.webp=s96-fcrop64=1,00000000ffffffff-rw"

# --- Fake Content Grid Data ---
fake_items = [
    {"type": "News Article", "title": "AI Is Changing Journalism", "date": datetime.now() - timedelta(days=1), "preview": "https://www.bbc.com/news/tech-67683274", "hashtags": ["#AI", "#media", "#future"]},
    {"type": "Recipe", "title": "Vegan Carbonara", "date": datetime.now() - timedelta(days=2), "preview": "https://minimalistbaker.com/vegan-carbonara/", "hashtags": ["#vegan", "#dinner", "#quickmeals"]},
    {"type": "Todo", "title": "Finish MindTag MVP", "date": datetime.now() - timedelta(days=1), "preview": "Design + code content grid and onboarding.", "hashtags": ["#productivity", "#launch", "#founder"]},
    {"type": "Thought", "title": "What if content was memory?", "date": datetime.now() - timedelta(days=3), "preview": "Need to explore link between mind & cloud.", "hashtags": ["#philosophy", "#UX", "#mind"]},
    {"type": "Funny Video", "title": "Dog on Zoom Call", "date": datetime.now() - timedelta(days=1), "preview": "https://www.instagram.com/p/CwFunnyDog/", "hashtags": ["#funny", "#pets", "#lol"]},
    {"type": "Book", "title": "The Creative Act", "date": datetime.now() - timedelta(days=4), "preview": "Highlight: Simplicity = power.", "hashtags": ["#creativity", "#simplicity", "#books"]}
]

# Filter for past 7 days
gridded_items = [item for item in fake_items if item["date"] >= datetime.now() - timedelta(days=7)]

# --- Layout ---
st.set_page_config(layout="wide", page_title="MindTag Dashboard", page_icon="🧠")

with st.container():
    cols = st.columns([0.08, 0.92])
    with cols[0]:
        st.image(user_avatar_url, width=48)
    with cols[1]:
        st.markdown(f"### Welcome, {user_name}")

# --- Linked Storage Display ---
with st.container():
    st.markdown("#### Linked Storage")
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(drive_icon, width=32)
    with col2:
        st.markdown(f"**{linked_drive}**")

# --- Tag It Button ---
st.markdown("---")
st.markdown("#### Add New Content")
if st.button("Tag it", use_container_width=True):
    st.info("Redirecting to content creator page... (Not wired yet)")

# --- Content Grid Preview ---
st.markdown("---")
st.markdown("#### Saved This Week")
cols = st.columns(3)

for i, item in enumerate(gridded_items):
    with cols[i % 3]:
        with st.container():
            st.markdown(
                f"""
                <div style='border-radius: 16px; background-color: #ffffff; padding: 1rem; box-shadow: 0 0 10px rgba(0,0,0,0.05);'>
                    <strong>{item['title']}</strong><br>
                    {'<a href="' + item['preview'] + '">' + item['preview'] + '</a>' if item['preview'].startswith('http') else '<em>' + item['preview'] + '</em>'}<br>
                    <small>{item['type']} – Saved {item['date'].strftime('%b %d')}</small><br>
                    <div style='margin-top: 0.5rem;'>
                        {" ".join([f"<span style='background:#f0f0f0;border-radius:8px;padding:2px 6px;margin-right:4px;font-size:0.8rem;'>{tag}</span>" for tag in item['hashtags']])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Folder Buttons ---
st.markdown("### Explore Folders")
folder_names = ["News Articles", "Recipes", "Todo", "Thoughts", "Funny Videos", "Books"]
folder_cols = st.columns(len(folder_names))

for i, folder in enumerate(folder_names):
    with folder_cols[i]:
        st.button(folder, key=f"folder_{i}")
