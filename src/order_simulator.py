import os
import pandas as pd
import numpy as np
import os

# 🔍 Set working directory to project root if not already
project_root = "D:/clock-drift-fpga-project"
if os.getcwd() != project_root:
    os.chdir(project_root)

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Load clock drift data
try:
    df = pd.read_csv("data/clock_drift.csv")
except FileNotFoundError:
    raise FileNotFoundError("Missing 'data/clock_drift.csv'. Please run the clock drift generator first.")

# Order generation parameters
order_interval = 1000  # Every 1000 samples = 1 ms
order_indices = np.arange(0, len(df), order_interval)

# Generate Orders
orders = pd.DataFrame({
    "order_id": np.arange(len(order_indices)),
    "fpga_1_ts": df.loc[order_indices, "fpga_1_time"].values,
    "fpga_2_ts": df.loc[order_indices, "fpga_2_time"].values
})

# Save normal orders (FPGA_1 is ground truth)
normal_orders = orders.sort_values(by="fpga_1_ts").reset_index(drop=True)
normal_orders.to_csv("data/normal_orders.csv", index=False)

# Save drifted orders (FPGA_2 introduces possible reorder)
drifted_orders = orders.sort_values(by="fpga_2_ts").reset_index(drop=True)
drifted_orders.to_csv("data/drifted_orders.csv", index=False)

print("Order simulation completed.")
print("Normal order timestamps saved to: data/normal_orders.csv")
print("Drifted order timestamps saved to: data/drifted_orders.csv")
