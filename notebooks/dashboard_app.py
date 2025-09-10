import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set Streamlit page config
st.set_page_config(page_title="Clock Drift FPGA Dashboard", layout="wide")

st.title("FPGA Clock Drift Analysis Dashboard")

# Helper: load CSV if exists
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# Load all CSVs
drift_df = load_csv("data/clock_drift.csv")
faulted_df = load_csv("data/clock_drift_faulted.csv")
corrected_df = load_csv("data/clock_drift_corrected.csv")
loss_df = load_csv("output/loss_report.csv")
anomaly_df = load_csv("output/anomaly_log.csv")
skew_df = load_csv("data/vlsi_clock_skew.csv")
signal_df = load_csv("data/signal_delay_profile.csv")

# Sample Range Control
if drift_df is not None:
    max_sample = len(drift_df)
    sample_range = st.slider("Select Sample Range", 0, max_sample, (0, max_sample), step=1000)
else:
    sample_range = (0, 0)

# Plotting utility
def render_plot(title, fig):
    st.subheader(title)
    st.pyplot(fig)

# 1. Clock Drift Plot
if drift_df is not None:
    sliced = drift_df.iloc[sample_range[0]:sample_range[1]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sliced["sample"], (sliced["fpga_2_time"] - sliced["fpga_1_time"]) * 1e6, label="Drift (µs)", color='red')
    ax.set_xlabel("Sample")
    ax.set_ylabel("Drift (µs)")
    ax.set_title("Clock Drift Between FPGA_1 and FPGA_2")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    render_plot("Clock Drift Over Time", fig)

# 2. Faulted vs Corrected
if faulted_df is not None and corrected_df is not None:
    sliced_fault = faulted_df.iloc[sample_range[0]:sample_range[1]]
    sliced_corr = corrected_df.iloc[sample_range[0]:sample_range[1]]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sliced_fault["sample"], sliced_fault["fpga_2_faulted"], alpha=0.4, label="Faulted")
    ax.plot(sliced_corr["sample"], sliced_corr["fpga_2_corrected"], label="Corrected", color='green')
    ax.plot(sliced_corr["sample"], sliced_corr["fpga_1_time"], linestyle='--', label="FPGA_1", alpha=0.6)

    ax.set_title("Clock Correction via Feedback")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Time (ns)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    render_plot("Faulted vs Corrected Clocks", fig)
else:
    st.warning("Faulted or Corrected CSV not found.")

# 3. Profit/Loss Chart
if loss_df is not None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(loss_df["order_id"], loss_df["loss_per_order"], label="Loss per Order", color="orange")
    ax.axhline(0, color='black', linestyle='--')
    ax.set_title("Loss due to Clock Drift")
    ax.set_xlabel("Order ID")
    ax.set_ylabel("Loss")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    render_plot("Profit/Loss Impact", fig)

# 4. Anomaly Heatmap
if anomaly_df is not None and not anomaly_df.empty:
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.heatmap(
        anomaly_df[["position_in_stream", "current_order_id"]].T,
        cmap="Reds", annot=True, fmt=".0f", cbar=True, ax=ax
    )
    ax.set_title("Order ID Anomalies due to Clock Drift")
    render_plot("Anomaly Heatmap", fig)

# 5. VLSI Clock Skew Simulation
if skew_df is not None:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(skew_df["sample"], skew_df["max_skew"], label="Max Skew", color="purple")
    ax.set_title("VLSI Clock Tree Skew Simulation")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Skew (ns)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    render_plot("Clock Skew in VLSI Paths", fig)

# 6. Signal Delay Profile
if signal_df is not None and not signal_df.empty:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(signal_df["sample"], signal_df["delay_ns"], label="Delay", color="teal")
    ax.axhline(signal_df["delay_ns"].mean(), linestyle="--", color="gray", label="Mean Delay")
    ax.set_title("Signal Delay Profile (Skew + Jitter)")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Delay (ns)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    render_plot("Signal Delay & Jitter Profile", fig)
else:
    st.warning("Signal delay profile CSV is missing or empty.")