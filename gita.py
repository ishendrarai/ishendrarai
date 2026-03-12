import requests
import random

# Bhagavad Gita chapters with verse count
chapters = {
1:47,2:72,3:43,4:42,5:29,6:47,
7:30,8:28,9:34,10:42,11:55,12:20,
13:35,14:27,15:20,16:24,17:28,18:78
}

chapter = random.choice(list(chapters.keys()))
verse = random.randint(1, chapters[chapter])

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
