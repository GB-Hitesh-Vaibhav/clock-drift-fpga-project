import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

os.makedirs("output", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# Load order data
normal_df = pd.read_csv("data/normal_orders.csv")
drifted_df = pd.read_csv("data/drifted_orders.csv")

# Simulate a price timeline (random walk)
np.random.seed(42)
price_changes = np.random.normal(loc=0, scale=0.1, size=len(normal_df) + 100)
prices_over_time = 100 + np.cumsum(price_changes)

# 🧠 Price based on timestamps
normal_df["executed_price"] = np.interp(normal_df["fpga_1_ts"], np.linspace(0, 1, len(prices_over_time)), prices_over_time)
drifted_df["executed_price"] = np.interp(drifted_df["fpga_2_ts"], np.linspace(0, 1, len(prices_over_time)), prices_over_time)

# Calculate values
normal_df["value"] = normal_df["executed_price"]
drifted_df["value"] = drifted_df["executed_price"]

# Compare by order_id
merged = pd.merge(
    normal_df[["order_id", "value"]],
    drifted_df[["order_id", "value"]],
    on="order_id",
    suffixes=("_normal", "_drifted")
)

# Loss = drifted - normal
merged["loss_per_order"] = merged["value_drifted"] - merged["value_normal"]

# Save and plot
merged.to_csv("output/loss_report.csv", index=False)
print("Loss report saved to: output/loss_report.csv")

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
