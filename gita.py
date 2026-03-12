import requests
import random

chapter = random.randint(1,18)
verse = random.randint(1,20)

url = f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter}/verses/{verse}/"

headers = {
"X-RapidAPI-Key":"demo",
"X-RapidAPI-Host":"bhagavad-gita3.p.rapidapi.com"
}

try:
    response = requests.get(url,headers=headers)
    data = response.json()

    shloka = data["text"]
    meaning = data["translations"][0]["description"]

except:
    shloka = "Unable to fetch shloka today 🙏"
    meaning = "Please check again tomorrow."

text=f"""
## 🕉 Bhagavad Gita Shloka of the Day

📖 Chapter: {chapter}  
🔢 Verse: {verse}

{shloka}

💡 Meaning:
{meaning}
"""

with open("gita.md","w",encoding="utf-8") as f:
    f.write(text)
