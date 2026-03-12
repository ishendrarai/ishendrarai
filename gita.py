import requests
import random

chapter = random.randint(1, 18)
verse = random.randint(1, 20)

url = f"https://bhagavadgitaapi.in/slok/{chapter}/{verse}"

response = requests.get(url)
data = response.json()

shloka = data["slok"]
meaning = data["tej"]["ht"]

text = f"""
## 🕉️ Bhagavad Gita Shloka of the Day

📖 Chapter: {chapter}  
🔢 Verse: {verse}

{shloka}

💡 Meaning:
{meaning}
"""

with open("gita.md", "w", encoding="utf-8") as f:
    f.write(text)