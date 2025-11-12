# 🚦 Traffic Signal Control System

**Deep Reinforcement Learning-based 4-way Traffic Signal Control with GPU Support**

A complete, production-ready system for optimizing traffic signal timing using Double DQN agent with multi-objective rewards, safety constraints, and professional visualization.

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Visualization Methods](#visualization-methods)
- [Configuration](#configuration)
- [Performance](#performance)
- [Constraints Implemented](#constraints-implemented)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## ✨ Features

### Core Capabilities
- **4-Way Intersection Control**: North, South, East, West directions
- **11-Action Space**: Diverse signal phases for different traffic scenarios
- **Multi-Vehicle Types**: Regular vehicles, pedestrians, emergency vehicles
- **Turn Management**: Left turns, right turns, straight movements with safety
- **A* Priority Queue**: Intelligent object prioritization by urgency
- **GPU Acceleration**: Automatic CUDA detection and utilization

### Reward System
- **Multi-Objective Optimization**:
  - Throughput (minimize queue length)
  - Fairness (Gini coefficient-based balance)
  - Safety (risky event penalties)
  - Pedestrian care (minimize crossing wait)
  - Efficiency (smooth signal transitions)

### Safety & Constraints
- ✓ Dynamic pedestrian crossing (3-10 seconds based on traffic)
- ✓ Left turn yield logic with opposing traffic
- ✓ Emergency vehicle override (priority weight: 10000)
- ✓ Starvation prevention (30-second maximum wait threshold)
- ✓ Hard safety constraints (8-60 second green times)
- ✓ All-red periods for conflict prevention

### Visualization
- **3 Visualization Methods**:
  1. Console (ASCII art) - No dependencies
  2. Matplotlib (animated plots) - Real-time metrics
  3. PyQt5 GUI (professional UI) - Interactive controls

### Agent Architecture
- **Double DQN** with target network
- **Experience Replay** buffer (10,000 capacity)
- **Epsilon-Greedy** exploration (1.0 → 0.01)
- **Gradient Clipping** for stability
- **Automatic GPU/CPU** selection

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
cd traffic_control_rl

# Install in editable mode
pip install -e .

python scripts/run_demo.py