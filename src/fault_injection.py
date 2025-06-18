import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📁 Ensure required folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📥 Load drift data to inject faults into
df = pd.read_csv("data/clock_drift.csv")

# ✅ If 'sample' column is missing, add it
if "sample" not in df.columns:
    df["sample"] = np.arange(len(df))

# 🔧 Fault Injection Parameters
np.random.seed(42)
fault_chance = 0.01  # 1% of samples are faulty
fault_magnitude_ns = 10  # Injected spike size in nanoseconds

# 🧠 Inject spikes randomly
fault_mask = np.random.rand(len(df)) < fault_chance
fault_type = np.random.choice(["spike", "drift_jump", "stuck"], size=len(df))

# Create a copy of original
df["fpga_2_faulted"] = df["fpga_2_time"].copy()

for i in range(len(df)):
    if fault_mask[i]:
        if fault_type[i] == "spike":
            df.loc[i, "fpga_2_faulted"] += np.random.choice([-1, 1]) * fault_magnitude_ns
        elif fault_type[i] == "drift_jump":
            df.loc[i:, "fpga_2_faulted"] += np.random.choice([-1, 1]) * fault_magnitude_ns / 2
        elif fault_type[i] == "stuck":
            if i > 0:
                df.loc[i, "fpga_2_faulted"] = df.loc[i - 1, "fpga_2_faulted"]

# 💾 Save faulted data
df.to_csv("data/clock_drift_faulted.csv", index=False)
print("Faulted drift data saved to: data/clock_drift_faulted.csv")

# 📈 Plot comparison
plt.figure(figsize=(10, 5))
plt.plot(df["sample"], df["fpga_2_time"], label="Original FPGA_2", alpha=0.5)
plt.plot(df["sample"], df["fpga_2_faulted"], label="Faulted FPGA_2", color="crimson", linewidth=1)
plt.title("Injected Faults in Clock Drift Signal")
plt.xlabel("Sample Index")
plt.ylabel("Timestamp (ns)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/plots/fault_injection_plot.png")
plt.close()

print("Fault visualization saved to: output/plots/fault_injection_plot.png")
