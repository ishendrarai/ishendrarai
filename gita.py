import requests

url = "https://api.bhagavadgita.io/v2/get-daily-verse/"

try:
    response = requests.get(url, timeout=10)
    data = response.json()

    chapter = data["chapter_number"]
    verse = data["verse_number"]
    shloka = data["text"]

    # first translation
    meaning = data["translations"][0]["description"]

except Exception as e:
    chapter = "-"
    verse = "-"
    shloka = "Unable to fetch Bhagavad Gita verse today 🙏"
    meaning = "API temporarily unavailable."

text = f"""
## 🕉 Bhagavad Gita Shloka of the Day

📖 Chapter: {chapter}  
🔢 Verse: {verse}

{shloka}

💡 Meaning:
{meaning}
"""

with open("gita.md","w",encoding="utf-8") as f:
    f.write(text)
