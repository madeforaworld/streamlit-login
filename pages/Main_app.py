import streamlit as st
from datetime import datetime, timedelta

# --- Layout must come first ---
st.set_page_config(layout="wide", page_title="MindTag Dashboard", page_icon="🧠")

# Apply global light mode style override
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #f9fafb;
            color: #111;
        }
        .block-container {
            background-color: #ffffff;
        }
        .stButton > button {
            background-color: #3366FF !important;
            color: white !important;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
        }
        .stButton > button:hover {
            background-color: #254eda !important;
        }
    </style>
""", unsafe_allow_html=True)


user_name = "Percy Plum"
user_avatar_url = "https://e7.pngegg.com/pngimages/687/86/png-clipart-google-logo-google-adwords-g-suite-google-account-google-logo-chess.png"
linked_drive = "Percy Google Drive"
drive_icon = "https://www.gstatic.com/marketing-cms/assets/images/e8/4f/69d708b2455397d7b88b0312f7c5/google-drive.webp=s96-fcrop64=1,00000000ffffffff-rw"

# --- Fake Content Grid Data with Summary and Emoji Tokens ---
fake_items = [
    {"type": "News Article", "title": "AI Is Changing Journalism", "date": datetime.now() - timedelta(days=1), "preview": "https://www.bbc.com/news/tech-67683274", "summary": "News article about how AI is impacting journalism.", "emoji": "📰", "hashtags": ["#AI", "#media", "#future"]},
    {"type": "Recipe", "title": "Vegan Carbonara", "date": datetime.now() - timedelta(days=2), "preview": "https://minimalistbaker.com/vegan-carbonara/", "summary": "Vegan pasta recipe that takes about 30 minutes to cook and has 10 ingredients.", "emoji": "🍽️", "hashtags": ["#vegan", "#dinner", "#quickmeals"]},
    {"type": "Todo", "title": "Finish MindTag MVP", "date": datetime.now() - timedelta(days=1), "preview": "Design + code content grid and onboarding.", "summary": "Task to finalize and polish the MindTag MVP features.", "emoji": "✅", "hashtags": ["#productivity", "#launch", "#founder"]},
    {"type": "Thought", "title": "What if content was memory?", "date": datetime.now() - timedelta(days=3), "preview": "Need to explore link between mind & cloud.", "summary": "Idea exploring digital content as an extension of memory.", "emoji": "💭", "hashtags": ["#philosophy", "#UX", "#mind"]},
    {"type": "Funny Video", "title": "Dog on Zoom Call", "date": datetime.now() - timedelta(days=1), "preview": "https://www.instagram.com/p/CwFunnyDog/", "summary": "Instagram video of a dog joining a Zoom call.", "emoji": "📹", "hashtags": ["#funny", "#pets", "#lol"]},
    {"type": "Book", "title": "The Creative Act", "date": datetime.now() - timedelta(days=4), "preview": "Highlight: Simplicity = power.", "summary": "Insight from a book about the power of simplicity in creativity.", "emoji": "📚", "hashtags": ["#creativity", "#simplicity", "#books"]}
]

# Filter for past 7 days
gridded_items = [item for item in fake_items if item["date"] >= datetime.now() - timedelta(days=7)]

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

# --- AI Search Bar ---
with st.container():
    st.markdown("#### Search your content")
    search_query = st.text_input("Ask anything, search by topic or content type", placeholder="e.g. Show me dog videos or vegan recipes")
    if search_query:
        filtered_items = [item for item in gridded_items if search_query.lower() in item['title'].lower() or search_query.lower() in item['summary'].lower() or any(search_query.lower() in tag.lower() for tag in item['hashtags'])]
        st.success(f"Found {len(filtered_items)} matching result(s) for: '{search_query}'")
        gridded_items = filtered_items

# --- Content Grid Preview ---
st.markdown("---")
st.markdown("#### Tagged This Week")
cols = st.columns(3)

for i, item in enumerate(gridded_items):
    with cols[i % 3]:
        with st.container():
            st.markdown(
                f"""
                <div style='border-radius: 16px; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem; border: 1px solid #e2e2e2; word-wrap: break-word;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-weight: bold; font-size: 1.1rem;'>{item['title']}</div>
                        <span style='font-size: 1.5rem;'>{item['emoji']}</span>
                    </div>
                    <hr style='border: none; border-top: 1px solid #eee; margin: 0.5rem 0;'>
                    <div style='font-size: 0.9rem; color: #444; margin-bottom: 0.25rem;'>Summary</div>
                    <div style='font-size: 0.95rem; margin-bottom: 0.75rem;'>{item['summary']}</div>
                    <div>
                        {'<a href="' + item['preview'] + '" style="word-break: break-word;">' + item['preview'] + '</a>' if item['preview'].startswith('http') else '<em>' + item['preview'] + '</em>'}<br>
                        <small>{item['type']} – Saved {item['date'].strftime('%b %d')}</small>
                        <div style='margin-top: 0.5rem;'>
                            {" ".join([f"<span style='background:#f0f0f0;border-radius:8px;padding:2px 6px;margin-right:4px;font-size:0.8rem;'>{tag}</span>" for tag in item['hashtags']])}
                        </div>
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
