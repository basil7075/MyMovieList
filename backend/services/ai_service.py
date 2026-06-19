import json
from groq import Groq
from ..config import GROQ_API_KEY

client = Groq(api_key = GROQ_API_KEY)

def get_recommendations(watched_movies: list[dict]) -> list[dict]:
    
    if not watched_movies:
        return []

    movie_list = "\n".join(
        f"-{m['title']}({m.get('genres','unknown_genre')}) - rated{m.get('rating','?')}/10"
        for m in watched_movies[:10]
    )

    prompt = f"""Based on these movies the user has watched and rated:
    {movie_list}
    Recommend 3 movies they would enjoy. Reply ONLY with a JSON array, no markdown, no explanation outside the JSON.
    Format:
    [
    {{"title": "Movie Title", "reason": "One sentence why they'd like it"}},
    ...
    ]"""

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = [{"role":"user","content":prompt}],
        temperature = 0.7,
        max_tokens = 300,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)
