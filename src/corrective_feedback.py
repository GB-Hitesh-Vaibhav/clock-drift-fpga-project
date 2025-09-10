import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# Ensure necessary folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# Load faulty drift data
df = pd.read_csv("data/clock_drift_faulted.csv")

# Feedback Correction Model using Proportional Control
kp = 0.1  # Proportional gain

# ➕ Initialize corrected signal
df["fpga_2_corrected"] = df["fpga_2_faulted"].copy()

# 🛠 Apply feedback correction iteratively
for i in range(1, len(df)):
    drift_error = df.loc[i, "fpga_2_corrected"] - df.loc[i, "fpga_1_time"]
    correction = -kp * drift_error
    df.loc[i, "fpga_2_corrected"] += correction

# Save the corrected clock data
df.to_csv("data/clock_drift_corrected.csv", index=False, float_format="%.10f")
print("Corrected drift data saved to: data/clock_drift_corrected.csv")

# Plot: Faulted vs Corrected vs Reference
plt.figure(figsize=(10, 5))
plt.plot(df["sample"], df["fpga_2_faulted"], label="Faulted FPGA_2", alpha=0.4)
plt.plot(df["sample"], df["fpga_2_corrected"], label="Corrected FPGA_2", color="green")
plt.plot(df["sample"], df["fpga_1_time"], label="Reference FPGA_1", color="blue", linestyle="--", alpha=0.6)
plt.title("Drift Correction using Feedback Controller")
plt.xlabel("Sample Index")
plt.ylabel("Timestamp (s)")  # Fixed unit label
plt.legend(loc="upper right")  # Prevents performance warning
plt.grid(True)
plt.tight_layout()
plt.savefig("output/plots/corrected_feedback_plot.png")
plt.close()

print("Correction plot saved to: output/plots/corrected_feedback_plot.png")
