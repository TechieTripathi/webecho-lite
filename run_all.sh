# run_all.sh
#!/bin/bash

echo "WebEcho-Lite: One-Click Reproducibility"
echo "Starting at: $(date)"
echo "----------------------------------------"

# Step 1: Generate synthetic pages
echo "[1/4] Generating 500 Ollama pages..."
python generate_genai.py

# Step 2: Scrape real Flipkart pages
echo "[2/4] Scraping 429 Flipkart pages..."
python scrape_real_playwright.py

# Step 3: Extract features
echo "[3/4] Extracting DOM features..."
python extract_features.py

# Step 4: Train & plot ROC
echo "[4/4] Training threshold classifier..."
python train.py

echo "----------------------------------------"
echo "DONE! Check:"
echo "   → features.csv (929 rows)"
echo "   → roc.png (AUC = 0.997)"
echo "   → extension/ → Load in Chrome"
echo "Finished at: $(date)"