import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📁 Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📥 Load faulty drift data
df = pd.read_csv("data/clock_drift_faulted.csv")

# 🧠 Feedback Correction Model (simple proportional control)
kp = 0.1  # Proportional gain

# ➕ Initialize correction
df["fpga_2_corrected"] = df["fpga_2_faulted"].copy()

# 🧪 Apply feedback control
for i in range(1, len(df)):
    drift_error = df.loc[i, "fpga_2_corrected"] - df.loc[i, "fpga_1_time"]
    correction = -kp * drift_error
    df.loc[i, "fpga_2_corrected"] += correction  # adjust using feedback

# 💾 Save corrected data
df.to_csv("data/clock_drift_corrected.csv", index=False)
print("Corrected drift data saved to: data/clock_drift_corrected.csv")

# 📈 Plot comparison of faulted vs corrected
plt.figure(figsize=(10, 5))
plt.plot(df["sample"], df["fpga_2_faulted"], label="Faulted FPGA_2", alpha=0.4)
plt.plot(df["sample"], df["fpga_2_corrected"], label="Corrected FPGA_2", color="green")
plt.plot(df["sample"], df["fpga_1_time"], label="Reference FPGA_1", color="blue", linestyle="--", alpha=0.6)
plt.title("Drift Correction using Feedback Controller")
plt.xlabel("Sample Index")
plt.ylabel("Timestamp (ns)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/plots/corrected_feedback_plot.png")
plt.close()

print("Correction plot saved to: output/plots/corrected_feedback_plot.png")
