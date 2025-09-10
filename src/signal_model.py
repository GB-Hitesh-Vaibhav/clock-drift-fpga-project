import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# 📁 Ensure output folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# 📏 Simulation Parameters
samples = 10000
base_delay_ns = 3.2            # Baseline propagation delay (ns)
jitter_stddev_ns = 0.2         # Jitter (ns)
skew_ns = 0.5                  # Constant skew (ns)

np.random.seed(42)

# 🔀 Simulate signal path delays
jitter = np.random.normal(0, jitter_stddev_ns, size=samples)
signal_a = np.linspace(0, samples * base_delay_ns, samples) + jitter
signal_b = signal_a + skew_ns

# 📊 Calculate delay profile
delay_profile = signal_b - signal_a

# 💾 Save signal delay profile
signal_df = pd.DataFrame({
    "sample": np.arange(samples),
    "signal_a_time": signal_a,
    "signal_b_time": signal_b,
    "delay_ns": delay_profile
})
signal_df.to_csv("data/signal_delay_profile.csv", index=False, float_format="%.10f")
print("Signal delay profile saved to: data/signal_delay_profile.csv")

# 📈 Plot waveform
plt.figure(figsize=(10, 5))
plt.plot(signal_df["sample"], signal_df["delay_ns"], label="Delay (Skew + Jitter)", color="purple")
plt.axhline(y=skew_ns, color="gray", linestyle="--", label="Ideal Skew")
plt.title("Signal Delay Profile with Jitter and Skew")
plt.xlabel("Sample Index")
plt.ylabel("Delay (ns)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("output/plots/signal_delay_profile.png")
plt.close()

print("Delay waveform saved to: output/plots/signal_delay_profile.png")
