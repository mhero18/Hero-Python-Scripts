import cloudscraper

INPUT_FILE = "items.txt"
OUTPUT_FILE = "output.txt"

API_URL = "https://itemdb.com.br/api/v1/items/many"

scraper = cloudscraper.create_scraper()

def load_item_names(filename):
    # Read item names from a text file (one per line)
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def fetch_items(item_names):
    # Send all names to the API in one request
    payload = {
        "id": [],
        "item_id": [],
        "name": item_names,
        "image_id": [],
        "name_image_id": []
    }
    resp = scraper.post(API_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def save_images_txt(item_names, items, filename):
    # Write <img> tags in the same order as the input (allow duplicates, ignore case)
    # Build a case-insensitive lookup map
    lookup = {item["name"].lower(): item for item in items.values()}

    with open(filename, "w", encoding="utf-8") as f:
        for name in item_names:
            match = lookup.get(name.lower())
            if match and match.get("image"):
                f.write(f'<img src="{match["image"]}">\n')
            else:
                f.write(f"<!-- Not found: {name} -->\n")

def main():
    item_names = load_item_names(INPUT_FILE)
    if not item_names:
        print("No item names found in input file.")
        return

    data = fetch_items(item_names)
    save_images_txt(item_names, data, OUTPUT_FILE)
    print(f"Saved {len(item_names)} items to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
