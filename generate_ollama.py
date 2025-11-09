import ollama
import random
import os
import pandas as pd
from pathlib import Path

# ----------------------------
# 1. Create output directory
# ----------------------------
OUT_DIR = Path("genai")
OUT_DIR.mkdir(exist_ok=True)

# ----------------------------
# 2. Product pool (100 unique items → repeat + shuffle for variety)
# ----------------------------
base_products = [
    "Samsung Galaxy S24", "iPhone 15 Pro", "OnePlus 12", "Google Pixel 9",
    "Sony WH-1000XM5", "Bose QuietComfort 45", "AirPods Pro 2", "JBL Flip 6",
    "Nike Air Max 270", "Adidas Ultraboost", "Puma RS-X", "Reebok Nano X",
    "Dell XPS 13", "MacBook Air M3", "HP Spectre x360", "Lenovo ThinkPad X1",
    "Logitech MX Master 3S", "Apple Magic Keyboard", "Razer DeathAdder V3",
    "Nikon Z6 II", "Canon EOS R6", "GoPro HERO12", "DJI Mini 4 Pro",
    "Dyson V15 Detect", "Roomba i7+", "Philips Airfryer XXL", "Instant Pot Duo",
    "Kindle Paperwhite", "Fitbit Charge 6", "Garmin Forerunner 965", "Oura Ring Gen 3",
    "PlayStation 5 Slim", "Xbox Series X", "Nintendo Switch OLED", "Steam Deck",
    "Samsung 55\" QLED 4K", "LG C3 65\" OLED", "Sony Bravia XR", "Bose Soundbar 900",
    "Apple Watch Ultra 2", "Galaxy Watch 7", "Fossil Gen 6", "Tissot PRX",
    "Ray-Ban Meta Smart Glasses", "Oakley Sunglasses", "Casio G-Shock", "Seiko 5 Sports"
] * 5  # 200+ items → will sample randomly

# Take 500 unique or near-unique names
random.seed(42)
random.shuffle(base_products)
selected_products = (base_products * 3)[:500]  # Ensures 500 even if short

# ----------------------------
# 3. Prompt template
# ----------------------------
def build_prompt(product):
    return f"""
Write a **complete, realistic Indian e-commerce product page** for **{product}** as seen on **Flipkart**.

**Must include**:
- `<title>` with product name and key specs
- Price in ₹ with discount % (e.g., ₹48,999)
- Star rating (4.2–4.8) with review count
- Bullet points (5–7) under "Highlights"
- Full description (150–200 words)
- 3–5 placeholder images: `<img src="https://via.placeholder.com/400x400?text={product}+Image+{{i}}" alt="...">`
- 3 customer reviews with names, dates, ratings, and text
- Full HTML with proper `<div>`, `<section>`, CSS classes like `._1AtVbE`, `.col-6-12`, etc.
- Use inline or `<style>` for basic styling
- **Return ONLY the raw HTML code. No markdown, no explanation.**

Make it look **exactly like a real Flipkart product page**.
"""

# ----------------------------
# 4. Generate & Save
# ----------------------------
pages = []

print(f"Generating 500 Ollama pages using llama3.2...")
for idx, product in enumerate(selected_products):
    try:
        print(f"[{idx+1:3d}/500] Generating: {product[:50]}...", end="")
        response = ollama.generate(model='llama3.2', prompt=build_prompt(product))
        html_content = response['response'].strip()

        # Save HTML file
        file_path = OUT_DIR / f"page_{idx:03d}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        pages.append({"path": str(file_path), "product": product, "label": 1})
        print(" DONE")
    except Exception as e:
        print(f" FAILED: {e}")
        continue

# ----------------------------
# 5. Save index CSV
# ----------------------------
df = pd.DataFrame(pages)
csv_path = "genai_pages.csv"
df.to_csv(csv_path, index=False)
print(f"\nDone! Generated {len(pages)} pages.")
print(f"Index saved: {csv_path}")
print(f"HTML files in: {OUT_DIR}/")