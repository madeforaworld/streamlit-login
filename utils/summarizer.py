import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_key"])

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
- 2–3 suggested tags

Note:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content
