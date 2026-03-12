import requests
import re
import random
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────
#  Fallback verse shown when the API is unreachable
# ─────────────────────────────────────────────
FALLBACK_VERSE = {
    "chapter": 2,
    "verse": 47,
    "slok": (
        "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।\n"
        "मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥"
    ),
    "transliteration": (
        "karmaṇy-evādhikāras te mā phaleṣhu kadāchana\n"
        "mā karma-phala-hetur bhūr mā te saṅgo 'stv akarmaṇi"
    ),
    "siva": {
        "et": (
            "You have a right to perform your prescribed duties, but you are not "
            "entitled to the fruits of your actions. Never consider yourself the "
            "cause of the results of your activities, and never be attached to "
            "not doing your duty."
        )
    },
}

# ─────────────────────────────────────────────
#  Bhagavad Gita has 18 chapters; verse counts
# ─────────────────────────────────────────────
CHAPTER_VERSE_COUNT = {
    1: 47,  2: 72,  3: 43,  4: 42,  5: 29,
    6: 47,  7: 30,  8: 28,  9: 34, 10: 42,
    11: 55, 12: 20, 13: 35, 14: 27, 15: 20,
    16: 24, 17: 28, 18: 78,
}

API_BASE = "https://vedicscriptures.github.io/slok"

def pick_verse_of_the_day() -> tuple[int, int]:
    """Deterministically pick a verse based on today's date."""
    today = datetime.now(timezone.utc)
    day_of_year = today.timetuple().tm_yday
    year = today.year

    # Build flat list of all (chapter, verse) pairs once
    all_verses = [
        (ch, v)
        for ch, total in CHAPTER_VERSE_COUNT.items()
        for v in range(1, total + 1)
    ]
    total_verses = len(all_verses)

    # Rotate through all verses, cycling yearly
    idx = (day_of_year + year * 365) % total_verses
    return all_verses[idx]


def fetch_verse(chapter: int, verse: int) -> dict | None:
    """Fetch verse data from vedicscriptures API."""
    url = f"{API_BASE}/{chapter}/{verse}/"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch verse {chapter}:{verse} — {e}")
        return None


def extract_english(data: dict) -> str:
    """Pull the best available English translation from the response."""
    # Try multiple translator keys in priority order
    for key in ("siva", "purohit", "chinmay", "san", "adi"):
        val = data.get(key, {})
        et = val.get("et") or val.get("sc") or ""
        if et and et.strip():
            return et.strip()
    return "Translation not available."


def build_readme_block(data: dict, chapter: int, verse: int) -> str:
    today_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    slok = data.get("slok", "").strip()
    transliteration = data.get("transliteration", "").strip()
    english = extract_english(data)

    block = f"""## 🕉️ Bhagavad Gita — Verse of the Day

> *Updated daily via GitHub Actions*  
> 📅 **{today_str}**

---

### 📖 Chapter {chapter}, Verse {verse}

**Sanskrit (Devanāgarī)**

```
{slok}
```

**Transliteration**

*{transliteration}*

**English Meaning**

> {english}

---

<sub>Verse fetched from the [Vedic Scriptures API](https://vedicscriptures.github.io) · Automated with ❤️ using Python & GitHub Actions</sub>
"""
    return block


def update_readme(block: str, readme_path: str = "README.md") -> None:
    """
    Replace the Gita section (between markers) inside the README,
    or append it if the markers are absent.
    """
    start_marker = "<!-- GITA_START -->"
    end_marker   = "<!-- GITA_END -->"

    path = Path(readme_path)
    original = path.read_text(encoding="utf-8") if path.exists() else ""

    new_section = f"{start_marker}\n{block}\n{end_marker}"

    if start_marker in original and end_marker in original:
        updated = re.sub(
            re.escape(start_marker) + ".*?" + re.escape(end_marker),
            new_section,
            original,
            flags=re.DOTALL,
        )
    else:
        # First run — append section to whatever is already there
        updated = original.rstrip() + "\n\n" + new_section + "\n"

    path.write_text(updated, encoding="utf-8")
    print(f"[OK] README updated — Chapter {chapter}, Verse {verse}")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    chapter, verse = pick_verse_of_the_day()
    print(f"[INFO] Today's verse → Chapter {chapter}, Verse {verse}")

    data = fetch_verse(chapter, verse)
    if data is None:
        # Fallback: try a random verse
        chapter = random.randint(1, 18)
        verse   = random.randint(1, CHAPTER_VERSE_COUNT[chapter])
        print(f"[WARN] Retrying with random verse → {chapter}:{verse}")
        data = fetch_verse(chapter, verse)

    if data is None:
        print("[WARN] API unreachable — using built-in fallback verse.")
        data    = FALLBACK_VERSE
        chapter = FALLBACK_VERSE["chapter"]
        verse   = FALLBACK_VERSE["verse"]

    block = build_readme_block(data, chapter, verse)
    update_readme(block)
