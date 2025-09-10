import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# 📁 Create necessary folders
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 🔧 Simulation Parameters
num_paths = 5
samples = 10000
base_clock_period_ns = 2.0       # Nominal clock period (e.g., 500 MHz)
rc_delay_base = 0.3              # Base RC delay (ns)
rc_delay_variation = 0.1         # Standard deviation of delay variation

np.random.seed(42)

# 🏗️ Simulate delay for each path in clock tree
delays = []
for i in range(num_paths):
    delay_profile = rc_delay_base + np.random.normal(0, rc_delay_variation, size=samples)
    delays.append(delay_profile)

# 📊 Organize into DataFrame
delay_df = pd.DataFrame(delays).T
delay_df.columns = [f"path_{i+1}" for i in range(num_paths)]
delay_df["sample"] = np.arange(samples)

# 🧮 Compute max skew across paths
delay_df["max_skew"] = delay_df.max(axis=1) - delay_df.min(axis=1)

# 💾 Save skew data
delay_df.to_csv("data/vlsi_clock_skew.csv", index=False, float_format="%.10f")
print("VLSI clock skew data saved to: data/vlsi_clock_skew.csv")

# 📈 Plot max skew vs. time
plt.figure(figsize=(10, 5))
plt.plot(delay_df["sample"], delay_df["max_skew"], label="Max Clock Skew (ns)", color="red")
plt.title("Clock Tree Skew Simulation (VLSI Delay Model)")
plt.xlabel("Sample Index")
plt.ylabel("Skew (ns)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("output/plots/vlsi_skew_plot.png")
plt.close()

print("Clock skew waveform saved to: output/plots/vlsi_skew_plot.png")
