from transformers import pipeline

# Load Hugging Face model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, folder):
    # Route based on folder
    if folder == "Recipes":
        custom_prompt = f"""Summarize this recipe in 250 words or less.
Include:
- Type of food
- Number of ingredients (list them at a high level)
- Prep/cook time
- Short description of the dish

Content:
{text}
"""

    elif folder == "News Articles":
        custom_prompt = f"""Summarize this news article.
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
        custom_prompt = f"""Summarize this book in under 250 words.
Include:
- What it's about
- Themes or chapters
- Type of book (e.g. fiction, memoir)
- Main takeaway

Content:
{text}
"""

    else:  # Thoughts, To-Do, Notes, etc.
        custom_prompt = f"""This is a personal note, to-do, or freeform content.
Summarize it in under 200 words.
Include:
- What it's about
- Any actions or ideas
- General tone or topic
- 2–3 suggested tags

Content:
{text}
"""

    # Run summary model
    result = summarizer(custom_prompt, max_length=200, min_length=50, do_sample=False)
    return result[0]["summary_text"]
