# extract_features.py — FINAL ROBUST VERSION
from bs4 import BeautifulSoup
import pandas as pd
import glob
import os

def get_stats(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        if not html.strip():
            print(f"Empty file: {path}")
            return None
        soup = BeautifulSoup(html, "html.parser")
        return {
            "nodes": len(soup.find_all()),
            "images": len(soup.find_all("img")),
            "text_len": len(soup.get_text()),
            "label": 1 if "genai" in path else 0,
            "path": os.path.basename(path)
        }
    except Exception as e:
        print(f"ERROR parsing {path}: {e}")
        return None

# Collect valid files
files = glob.glob("genai/*.html") + glob.glob("real/*.html")
data = []
for f in files:
    stats = get_stats(f)
    if stats:
        data.append(stats)

# Save
df = pd.DataFrame(data)
df.to_csv("features.csv", index=False)

# Print stats
print(f"\nSUCCESS: {len(df)} valid pages")
print(df["label"].value_counts().sort_index())
print("\nAverage per class:")
print(df.groupby("label")[["nodes", "images", "text_len"]].mean().round(1))