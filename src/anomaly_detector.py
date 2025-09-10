import os
import pandas as pd
import matplotlib.pyplot as plt

# Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# Auto-install seaborn if missing
try:
    import seaborn as sns
except ImportError:
    print("[INFO] seaborn not found. Installing now...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])
    import seaborn as sns
    print("[INFO] seaborn successfully installed.")

seaborn_available = True

# Ensure folders exist
os.makedirs("output", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# Load order files
normal_orders = pd.read_csv("data/normal_orders.csv")
drifted_orders = normal_orders.copy()

# ----- Inject anomalies into drifted_orders -----
import numpy as np
np.random.seed(42)

num_anomalies = max(1, len(drifted_orders)//50)  # ~2% anomalies
for _ in range(num_anomalies):
    i, j = np.random.randint(0, len(drifted_orders), 2)
    drifted_orders.loc[i, "order_id"], drifted_orders.loc[j, "order_id"] = (
        drifted_orders.loc[j, "order_id"], drifted_orders.loc[i, "order_id"]
    )

# Save drifted_orders to output (optional)
drifted_orders.to_csv("output/drifted_orders.csv", index=False)

# Detect anomalies: out-of-order order_ids
anomalies = []
last_id = -1
for i, oid in enumerate(drifted_orders["order_id"]):
    if oid < last_id:
        anomalies.append({
            "position_in_stream": i,
            "current_order_id": oid,
            "previous_order_id": last_id
        })
    last_id = oid

# Handle anomalies
if anomalies:
    anomaly_df = pd.DataFrame(anomalies)[["position_in_stream", "current_order_id", "previous_order_id"]]
    anomaly_df.to_csv("output/anomaly_log.csv", index=False)
    print(f"[INFO] Anomaly detection completed. {len(anomalies)} out-of-order violations detected.")
    print("Anomaly log saved to: output/anomaly_log.csv")

    # Plot heatmap if seaborn is available
    if seaborn_available:
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
else:
    print("[OK] No anomalies detected — all order IDs are in correct sequence.")
    # Save empty CSV to maintain consistent output
    pd.DataFrame(columns=["position_in_stream", "current_order_id", "previous_order_id"]).to_csv(
        "output/anomaly_log.csv", index=False
    )
