from playwright.sync_api import sync_playwright, TimeoutError
import time
import random
import pandas as pd
import os
from urllib.parse import urlparse, urljoin

# ----------------------------
# CONFIG
# ----------------------------
QUERIES = [
    "mobile phone",      # 100
    "wireless earbuds",  # 100
    "women kurti",       # 100
    "saree for women",   # 100
    "pressure cooker"    # 100
]
BASE_URL = "https://www.flipkart.com/search?q="
TARGET_PER_QUERY = 100
MAX_RETRIES = 3
OUTPUT_DIR = "real"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# MAIN
# ----------------------------
pages = []
seen_urls = set()

def is_product_page(url):
    return "/p/" in url or "/product" in url

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    total_saved = 0

    for query in QUERIES:
        if total_saved >= 500:
            break

        search_url = BASE_URL + query.replace(" ", "+")
        print(f"\nSearching: {query} → {search_url}")

        for attempt in range(MAX_RETRIES):
            try:
                page.goto(search_url, timeout=60000)
                page.wait_for_load_state("networkidle")
                break
            except TimeoutError:
                print(f"  Timeout {attempt+1}/{MAX_RETRIES}, retrying...")
                time.sleep(5)
        else:
            print("  Failed to load search page. Skipping.")
            continue

        # Scroll to load all results
        print("  Scrolling to load products...")
        for _ in range(6):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

        # Extract product links
        product_links = page.eval_on_selector_all(
            'a[href*="/p/"], a[href*="pid="]', 
            'els => els.map(el => el.href).filter(h => h.includes("/p/") || h.includes("pid="))'
        )
        product_links = [urljoin(search_url, link) for link in product_links]
        product_links = list(dict.fromkeys(product_links))  # dedupe
        print(f"  Found {len(product_links)} product links")

        saved_this_query = 0
        for link in product_links:
            if total_saved >= 500 or saved_this_query >= TARGET_PER_QUERY:
                break

            if link in seen_urls:
                continue

            for attempt in range(MAX_RETRIES):
                try:
                    print(f"  [{total_saved+1:3d}/500] Loading: {link[:60]}...", end="")
                    page.goto(link, timeout=60000)
                    page.wait_for_load_state("networkidle")

                    # Wait for product title
                    page.wait_for_selector("span.B_NuCI, h1", timeout=10000)

                    html = page.content()
                    filename = f"page_{total_saved:03d}"
                    html_path = os.path.join(OUTPUT_DIR, f"{filename}.html")
                    img_path = os.path.join(OUTPUT_DIR, f"{filename}.png")

                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html)
                    page.screenshot(path=img_path, full_page=True)

                    pages.append({
                        "path": html_path,
                        "url": link,
                        "query": query,
                        "label": 0
                    })
                    seen_urls.add(link)
                    total_saved += 1
                    saved_this_query += 1
                    print(" SAVED")
                    time.sleep(random.uniform(1.5, 3.0))
                    break
                except Exception as e:
                    if attempt == MAX_RETRIES - 1:
                        print(f" FAILED: {e}")
                    else:
                        print(f" retry {attempt+1}")
                        time.sleep(5)

    browser.close()

# ----------------------------
# SAVE INDEX
# ----------------------------
df = pd.DataFrame(pages)
csv_path = "real_pages.csv"
df.to_csv(csv_path, index=False)
print(f"\nDONE! Saved {len(pages)} real pages.")
print(f"→ HTML + PNG in: {OUTPUT_DIR}/")
print(f"→ Index: {csv_path}")