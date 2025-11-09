# train.py — FINAL
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

df = pd.read_csv("features.csv")
X = df["nodes"]
y = df["label"]

threshold = 200
pred = (X < threshold).astype(int)
auc = roc_auc_score(y, pred)
print(f"AUC (threshold < {threshold}): {auc:.3f}")

fpr, tpr, _ = roc_curve(y, -X)
plt.figure(figsize=(5,4))
plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
plt.plot([0,1],[0,1],'k--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC: DOM Nodes Only (n=929)")
plt.legend()
plt.tight_layout()
plt.savefig("roc.png", dpi=300)
print("roc.png saved")