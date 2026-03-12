import re

with open("README.md","r",encoding="utf-8") as f:
    readme = f.read()

with open("gita.md","r",encoding="utf-8") as f:
    gita = f.read()

pattern = r"<!-- GITA_SHLOKA_START -->(.*?)<!-- GITA_SHLOKA_END -->"

replacement = f"<!-- GITA_SHLOKA_START -->\n{gita}\n<!-- GITA_SHLOKA_END -->"

new_readme = re.sub(pattern, replacement, readme, flags=re.S)

with open("README.md","w",encoding="utf-8") as f:
    f.write(new_readme)