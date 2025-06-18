 HEAD
# clock-drift-fpga-project
Clock Drift Anomaly Detection using FPGA Order Timestamps

# Clock Drift-Induced Financial Risk Detection in FPGA-Based Trading Systems

## 📌 Summary

This software-only project simulates how **clock drift** in FPGA-based High-Frequency Trading (HFT) systems can lead to **timing anomalies**, **order execution failures**, and **financial losses**.

It models timing desynchronization between FPGAs, generates trade order sequences, detects FIFO violations, and estimates potential monetary impact—**all through Python-based simulation.**

---

## 🎯 Motivation

In high-frequency trading:
- Every microsecond matters.
- Orders are placed using **ultra-low latency FPGAs**.
- Even a **10 µs clock skew** can cause trades to execute out of order.

This project replicates those risks and builds a detection + analysis framework around it.

---

## 💡 Features

- ✅ Clock Drift Simulator (hardware-inspired)
- ✅ Synthetic Trade Order Generator (with timestamps)
- ✅ FIFO Violation + Anomaly Detection
- ✅ Financial Loss Modeling
- ✅ VLSI-inspired delay + jitter modeling
- ✅ PTP-based synchronization recovery simulation
- ✅ Interactive Dashboard for drift vs. loss analysis

---

## 📁 Project Structure

```bash
clock-drift-fpga-project/
│
├── README.md                 # Project overview
├── requirements.txt          # Python dependencies
│
├── data/                     # Simulated clocks & trade order datasets
│   ├── normal_orders.csv
│   ├── drifted_orders.csv
│   └── clock_drift.csv
│
├── src/                      # Core simulation and modeling scripts
│   ├── clock_simulator.py
│   ├── order_simulator.py
│   ├── anomaly_detector.py
│   ├── financial_model.py
│   ├── ptp_sync_model.py
│   ├── signal_model.py
│   ├── vlsi_drift_model.py
│   ├── fault_injection.py
│   └── corrective_feedback.py
│
├── notebooks/                # Visualizations and dashboard
│   └── dashboard.ipynb
│
└── output/                   # Logs, losses, and plots
    ├── anomaly_log.csv
    ├── loss_report.csv
    └── plots/
        ├── drift_waveform.png
        ├── anomaly_heatmap.png
        └── loss_graph.png
 049ec4f (Initial commit: Upload Clock Drift FPGA Python simulation)
