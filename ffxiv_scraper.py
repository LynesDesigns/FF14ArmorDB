import requests
from bs4 import BeautifulSoup
import json

# Base URL of the wiki
BASE_URL = "https://ffxiv.consolegameswiki.com"

# Page containing list of armor
LIST_URL = f"{BASE_URL}/wiki/Equipment"

response = requests.get(LIST_URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

armor_items = []

# Assume armor items are in tables or list elements
for link in soup.select("a[href*='/wiki/']"):  # All internal wiki links
    name = link.get_text(strip=True)
    url = BASE_URL + link['href']

    # Skip links without names
    if not name or name.lower() == "equipment":
        continue

    # Visit the item page to get the main image
    try:
        item_resp = requests.get(url)
        item_resp.raise_for_status()
        item_soup = BeautifulSoup(item_resp.text, "html.parser")
        # Wiki main image is usually in infobox with class "pi-image-thumbnail"
        img_tag = item_soup.select_one(".pi-image-thumbnail img")
        if img_tag and img_tag.has_attr("src"):
            image_url = img_tag["src"]
            if image_url.startswith("//"):
                image_url = "https:" + image_url
        else:
            image_url = ""  # fallback

        armor_items.append({
            "name": name,
            "url": url,
            "image": image_url
        })

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

# Save to JSON
with open("armor_items.json", "w", encoding="utf-8") as f:
    json.dump(armor_items, f, indent=2, ensure_ascii=False)

print(f"Saved {len(armor_items)} items to armor_items.json")