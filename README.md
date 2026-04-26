# Week 3 Lab OS - Monte Carlo Pi Estimation

This repository contains implementations of Monte Carlo Pi estimation with different parallelization approaches to demonstrate performance characteristics and synchronization overhead.

## Overview

The project implements three approaches to estimate Pi using the Monte Carlo method:

1. **Task 1**: Single-threaded baseline
2. **Task 2**: Multi-threaded with local accumulation (optimal parallel design)
3. **Task 3**: Multi-threaded with shared variables and mutex (demonstrates contention)

## Requirements

Before running the code, make sure you have Python 3.8+ installed.

Install required dependencies:

```
pip install numpy matplotlib psutil
```
## File Structure

```
.
├── monte_carlo_pi.py
├── time_vs_threads.png
├── speedup_vs_threads.png
└── README.md
```

## How to Run
Run the main script:
```
python monte_carlo_pi.py
```