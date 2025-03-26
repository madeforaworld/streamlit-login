import streamlit as st
from datetime import datetime, timedelta
import random

# --- Fake User Info ---
user_name = "Percy Plum"
user_avatar_url = "https://i.imgur.com/4ZQZxvS.png"  # Just a placeholder avatar
linked_drive = "PercyPlumGdrive"
drive_icon = "https://upload.wikimedia.org/wikipedia/commons/1/1f/Google_Drive_logo.png"

# --- Fake Content Grid Data ---
fake_items = [
    {"type": "News Article", "title": "AI Is Changing Journalism", "date": datetime.now() - timedelta(days=1), "preview": "https://www.bbc.com/news/tech-67683274"},
    {"type": "Recipe", "title": "Vegan Carbonara", "date": datetime.now() - timedelta(days=2), "preview": "https://minimalistbaker.com/vegan-carbonara/"},
    {"type": "Todo", "title": "Finish MindTag MVP", "date": datetime.now() - timedelta(days=1), "preview": "Design + code content grid and onboarding."},
    {"type": "Thought", "title": "What if content was memory?", "date": datetime.now() - timedelta(days=3), "preview": "Need to explore link between mind & cloud."},
    {"type": "Funny Video", "title": "Dog on Zoom Call", "date": datetime.now() - timedelta(days=1), "preview": "https://www.instagram.com/p/CwFunnyDog/"},
    {"type": "Book", "title": "The Creative Act", "date": datetime.now() - timedelta(days=4), "preview": "Highlight: Simplicity = power."}
]

# Filter for past 7 days
gridded_items = [item for item in fake_items if item["date"] >= datetime.now() - timedelta(days=7)]

# --- Layout ---
st.set_page_config(layout="wide")

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
        st.markdown(f"**{item['title']}**")
        if item["preview"].startswith("http"):
            st.markdown(f"[{item['preview']}]({item['preview']})")
        else:
            st.markdown(f"*{item['preview']}*")
        st.caption(f"{item['type']} – Saved {item['date'].strftime('%b %d')}")
        st.markdown("---")

# --- Folder Buttons ---
st.markdown("### Explore Folders")
folder_names = ["News Articles", "Recipes", "Todo", "Thoughts", "Funny Videos", "Books"]
folder_cols = st.columns(len(folder_names))

for i, folder in enumerate(folder_names):
    with folder_cols[i]:
        st.button(folder, key=f"folder_{i}")

