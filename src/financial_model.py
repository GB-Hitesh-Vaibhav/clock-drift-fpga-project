import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📁 Ensure folders exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📥 Load order data
normal_df = pd.read_csv("data/normal_orders.csv")
drifted_df = pd.read_csv("data/drifted_orders.csv")

# ⚙️ Simulate market prices (e.g., random walk)
np.random.seed(42)
price_changes = np.random.normal(loc=0, scale=0.1, size=len(normal_df))
prices = 100 + np.cumsum(price_changes)

normal_df["executed_price"] = prices
drifted_df["executed_price"] = prices  # same price timeline for fair comparison

# 🧮 Calculate theoretical vs drifted trade values
normal_df["value"] = normal_df["executed_price"]
drifted_df["value"] = drifted_df["executed_price"]

# Align by order_id for comparison
merged = pd.merge(
    normal_df[["order_id", "value"]],
    drifted_df[["order_id", "value"]],
    on="order_id",
    suffixes=("_normal", "_drifted")
)

# 📊 Calculate profit/loss due to misordering
merged["loss_per_order"] = merged["value_drifted"] - merged["value_normal"]

# 📤 Save report
merged.to_csv("output/loss_report.csv", index=False)
print("Loss report saved to: output/loss_report.csv")

# 📈 Plotting
plt.figure(figsize=(10, 5))
plt.plot(merged["order_id"], merged["loss_per_order"], label="Loss per Order", color='orange')
plt.axhline(0, color='black', linestyle='--')
plt.title("Profit/Loss Impact Due to Clock Drift")
plt.xlabel("Order ID")
plt.ylabel("Loss (₹ or $)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("output/plots/loss_graph.png")
plt.close()

print("Loss impact graph saved to: output/plots/loss_graph.png")
