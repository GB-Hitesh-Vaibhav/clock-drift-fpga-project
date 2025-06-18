import os
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 Optional: use seaborn only if available
try:
    import seaborn as sns
    seaborn_available = True
except ImportError:
    seaborn_available = False
    print("[WARN] Seaborn not installed. Heatmap will be skipped.")

# 📁 Ensure folders exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📥 Load order files
normal_orders = pd.read_csv("data/normal_orders.csv")
drifted_orders = pd.read_csv("data/drifted_orders.csv")

# 🧪 Detect anomalies: out-of-order order_ids
normal_sequence = list(normal_orders["order_id"])
drifted_sequence = list(drifted_orders["order_id"])

anomalies = []
last_id = -1

for i, oid in enumerate(drifted_sequence):
    if oid < last_id:
        anomalies.append({
            "position_in_stream": i,
            "current_order_id": oid,
            "previous_order_id": last_id
        })
    last_id = oid

# 📤 Save anomaly log
anomaly_df = pd.DataFrame(anomalies, columns=["position_in_stream", "current_order_id", "previous_order_id"])
anomaly_df.to_csv("output/anomaly_log.csv", index=False)

print(f"Anomaly detection completed. {len(anomalies)} out-of-order violations detected.")
print("Anomaly log saved to: output/anomaly_log.csv")

# 🖼️ Plot heatmap only if anomalies found and seaborn is available
if not anomaly_df.empty and seaborn_available:
    plt.figure(figsize=(12, 5))
    sns.heatmap(
        anomaly_df[["position_in_stream", "current_order_id"]].T,
        cmap="Reds", cbar=True, annot=True, fmt=".0f"
    )
    plt.title("Anomaly Heatmap (Order ID Violations due to Clock Drift)")
    plt.yticks([0.5, 1.5], ['Position in Stream', 'Order ID'], rotation=0)
    plt.tight_layout()
    plt.savefig("output/plots/anomaly_heatmap.png")
    plt.close()
    print("Anomaly heatmap saved to: output/plots/anomaly_heatmap.png")
elif anomaly_df.empty:
    print("No anomalies detected — skipping heatmap generation.")
elif not seaborn_available:
    print("Seaborn is not installed — skipping heatmap generation.")
