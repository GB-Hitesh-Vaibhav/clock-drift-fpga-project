import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📁 Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📥 Load original drift data
df = pd.read_csv("data/clock_drift.csv")

# ✅ Add sample index if missing
if "sample" not in df.columns:
    df.insert(0, "sample", range(len(df)))

# ⚙️ Simulate PTP sync every N samples
sync_interval = 5000  # e.g., sync every 5ms
correction_strength = 0.5  # 0=no correction, 1=perfect sync

# 💡 Apply periodic corrections
corrected_fpga_2 = df["fpga_2_time"].copy()
for i in range(0, len(df), sync_interval):
    drift = df.loc[i, "fpga_2_time"] - df.loc[i, "fpga_1_time"]
    correction = -correction_strength * drift
    corrected_fpga_2.iloc[i:] += correction

# 🧾 Save corrected drift data
df["fpga_2_corrected"] = corrected_fpga_2
df.to_csv("data/clock_drift_corrected.csv", index=False)

print("PTP sync simulation completed.")
print("Corrected clock data saved to: data/clock_drift_corrected.csv")

# 📈 Plot for visualization
plt.figure(figsize=(10, 5))
plt.plot(df["sample"], df["fpga_1_time"], label="FPGA_1 (Reference)", linestyle="--", alpha=0.7)
plt.plot(df["sample"], df["fpga_2_time"], label="FPGA_2 (Original Drift)", alpha=0.6)
plt.plot(df["sample"], df["fpga_2_corrected"], label="FPGA_2 (After PTP Sync)", color='green')
plt.title("PTP Clock Synchronization Simulation")
plt.xlabel("Sample Index")
plt.ylabel("Timestamp (ns)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/plots/ptp_sync_plot.png")
plt.close()

print("Sync visualization saved to: output/plots/ptp_sync_plot.png")
