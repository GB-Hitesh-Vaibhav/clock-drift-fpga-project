import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)
# Create required folders
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# Load base drift data
df = pd.read_csv("data/clock_drift.csv")

# Add sample index if missing
if "sample" not in df.columns:
    df["sample"] = np.arange(len(df))

# Fault Injection Parameters
np.random.seed(42)
fault_chance = 0.05  # 5% chance per sample
fault_magnitude_ns = 100  # 100 nanoseconds

# Copy original clock signal
df["fpga_2_faulted"] = df["fpga_2_time"].copy()

# Random fault types
fault_type = np.random.choice(["spike", "drift_jump", "stuck"], size=len(df))
fault_mask = np.random.rand(len(df)) < fault_chance

for i in range(len(df)):
    if fault_mask[i]:
        if fault_type[i] == "spike":
            df.loc[i, "fpga_2_faulted"] += np.random.choice([-1, 1]) * fault_magnitude_ns * 1e-9
        elif fault_type[i] == "drift_jump":
            df.loc[i:, "fpga_2_faulted"] += np.random.choice([-1, 1]) * (fault_magnitude_ns / 2) * 1e-9
        elif fault_type[i] == "stuck":
            if i > 0:
                df.loc[i, "fpga_2_faulted"] = df.loc[i - 1, "fpga_2_faulted"]

# Inject clustered burst faults every 2000 samples
for burst_start in range(0, len(df), 2000):
    if np.random.rand() < 0.5:
        burst = burst_start + np.arange(0, 300)
        noise = np.random.normal(loc=0, scale=50, size=len(burst)) * 1e-9
        df.loc[burst, "fpga_2_faulted"] += noise

# Save faulted data

df.to_csv("output/clock_drift_faulted.csv", index=False)
print("Faulted clock drift data saved to: output/clock_drift_faulted.csv")


# Plot fault injection results
plt.figure(figsize=(10, 5))
plt.plot(df["sample"], df["fpga_2_time"], label="Original FPGA_2", alpha=0.4)
plt.plot(df["sample"], df["fpga_2_faulted"], label="Faulted FPGA_2", color="crimson", linewidth=1)
plt.title("Aggressive Fault Injection in Clock Drift Signal")
plt.xlabel("Sample Index")
plt.ylabel("Timestamp (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/plots/fault_injection_plot.png")
plt.close()

print("Fault injection plot saved to: output/plots/fault_injection_plot.png")
