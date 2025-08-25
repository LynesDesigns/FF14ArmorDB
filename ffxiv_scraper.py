import requests
from bs4 import BeautifulSoup
import csv
import json
import os

# Target page to scrape
START_PAGE = "https://ffxiv.consolegameswiki.com/wiki/Armor"

# Output folder (GitHub Pages root = docs/)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CSV_FILE = os.path.join(OUTPUT_DIR, "ffxiv_armor.csv")
JSON_FILE = os.path.join(OUTPUT_DIR, "ffxiv_armor.json")

def scrape_armor():
    print("🔎 Fetching armor list from:", START_PAGE)
    response = requests.get(START_PAGE)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Simplistic example: all links inside wiki content
    armor_data = []
    for link in soup.select("div#mw-content-text a"):
        name = link.get_text(strip=True)
        href = link.get("href", "")
        if not name or not href:
            continue
        if not href.startswith("http"):
            href = "https://ffxiv.consolegameswiki.com" + href

        # Only keep links that look like gear/armor pages
        if "/wiki/" in href and len(name) > 2:
            armor_data.append({
                "name": name,
                "url": href,
                "image": "",  # can be extended to fetch page + image
            })

    print(f"✅ Found {len(armor_data)} armor entries")

    # Save CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url", "image"])
        writer.writeheader()
        writer.writerows(armor_data)
    print("📄 Saved CSV:", CSV_FILE)

    # Save JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(armor_data, f, indent=2, ensure_ascii=False)
    print("📄 Saved JSON:", JSON_FILE)

    print("\n🌐 Once pushed to GitHub, files will be live at:")
    print("   https://lynesdesigns.github.io/FF14ArmorDB/ffxiv_armor.json")
    print("   https://lynesdesigns.github.io/FF14ArmorDB/ffxiv_armor.csv")

if __name__ == "__main__":
    scrape_armor()
