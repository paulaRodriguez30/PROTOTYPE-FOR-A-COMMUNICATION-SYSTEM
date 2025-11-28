# Prototype for a Communication System over TV White Spaces (TVWS)

This repository contains the complete development of an SDR-based communication system for reliable transmission of images and text over **TV White Spaces (TVWS)**.  
It includes spectrum analysis, environment characterization, GNU Radio simulations, SDR implementation with USRP-2920 and HackRF One, and real-world transmission/reception tests.

---

## 📌 Project Overview

The main goal of this project is to **design, implement, and evaluate** a digital communication system using **Software Defined Radio (SDR)** to transmit medical-related images and text reliably over unused TV broadcast channels (TVWS).

The work covers:

- Analysis and characterization of the **electromagnetic environment** and TVWS spectrum.
- Design of a **complete baseband chain**: framing, coding, modulation, channel modeling, and BER estimation.
- Implementation of the system in **GNU Radio Companion (GRC)**.
- Validation in **simulation** and in **real hardware** using USRP-2920 and HackRF One.
- Comparison and analysis of measurement data using **Python / Jupyter / Google Colab**.

---

## 🎯 Main Objectives

- Identify **available TVWS channels** suitable for experimental communication.
- Implement an SDR-based communication system supporting:
  - Text transmission
  - Image transmission
- Evaluate the system in:
  - Controlled **simulation environments**
  - **Real RF channels** (coaxial link + over-the-air)
- Optimize transmission parameters for **robustness and low bit error rate (BER)**.

---

## 🧱 System Architecture (High-Level)

The communication system is built around:

- **Framing:** HDLC-based frames (flags, length, CRC/FCS).
- **Pre-processing:** scrambling / descrambling and **NRZI** coding / decoding.
- **Modulation schemes:**
  - FSK / GFSK (used in early tests and simulations)
  - **GMSK** (final scheme selected for real SDR experiments)
- **Channel models:**
  - Virtual channel in GNU Radio (noise, frequency offset, timing offset, multipath).
  - Physical channel using:
    - Coaxial cable (C4, 24.38 m, ~26.70 dB + 30 dB attenuator)
    - Over-the-air links with 400 MHz–1 GHz antennas.
- **Receivers:**
  - AGC + filtering → demodulation → NRZI decode → descrambling → HDLC deframing.
  - Recovery of text or image files and BER estimation.

---

## 📂 Repository Structure

Suggested structure (may vary slightly from your final layout):

```text
PROTOTYPE-FOR-A-COMMUNICATION-SYSTEM/
├─ README.md
├─ docs/
│  ├─ figures/                  # Block diagrams, flowcharts, setup photos
│  └─ thesis_notes.md           # Optional extra notes / excerpts
├─ Analysis-and-characterization-of-the-environment/
│  ├─ raw_scans/                # Raw spectrum scan files
│  ├─ TVWS_Final_Sweep_Comparison.ipynb
│  └─ TVWS_Final_Sweep_Comparison.csv
├─ TVWS_Spectrum_Scanning_and_Occupancy_Assessment/
│  └─ CSV/                      # Final TVWS sweep data for occupancy analysis
├─ SDR_System_Implementation/
│  ├─ usrp/
│  │  ├─ tx_flowgraph.grc
│  │  └─ rx_flowgraph.grc
│  ├─ hackrf/
│  │  ├─ tx_flowgraph.grc
│  │  └─ rx_flowgraph.grc
│  └─ tools/
│     ├─ image_sender.py
│     └─ image_receiver.py
├─ Simulation/
│  ├─ fsk_simulation.grc
│  └─ gmsk_simulation.grc
└─ data/
   └─ ber_results/              # BER logs, CSVs and analysis outputs
