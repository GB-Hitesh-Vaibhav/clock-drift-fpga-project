import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("output/plots", exist_ok=True)

# Simulation Parameters
duration_sec = 1           # Total simulated time in seconds
sampling_rate_hz = 1e6     # 1 MHz sampling rate (1 sample per microsecond)
drift_per_sec = 10e-6      # 10 microseconds drift per second

# Time Axis
total_samples = int(duration_sec * sampling_rate_hz)
time = np.arange(total_samples) / sampling_rate_hz  # seconds

# FPGA_1 Clock (Perfect Reference Clock)
clock_1 = time.copy()

# FPGA_2 Clock (with Drift)
drift = np.linspace(0, drift_per_sec, total_samples)
clock_2 = time + drift

# Save to CSV
df = pd.DataFrame({
    "sample": np.arange(total_samples),
    "time_sec": time,
    "fpga_1_time": clock_1,
    "fpga_2_time": clock_2,
    "drift_us": (clock_2 - clock_1) * 1e6  # Convert to microseconds
})
df.to_csv("data/clock_drift.csv", index=False, float_format="%.10f")

# Plot the drift
plt.figure(figsize=(10, 5))
plt.plot(time * 1000, (clock_2 - clock_1) * 1e6, label="Clock Drift", color='red')
plt.xlabel("Time (ms)")
plt.ylabel("Drift (µs)")
plt.title("Simulated Clock Drift between FPGA_1 and FPGA_2")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("output/plots/drift_waveform.png")
plt.close()

print("Clock drift simulation completed.")
print("Data saved to: data/clock_drift.csv")
print("Drift plot saved to: output/plots/drift_waveform.png")
