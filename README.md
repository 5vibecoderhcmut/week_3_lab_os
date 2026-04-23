# Week 3 Lab OS - Monte Carlo Pi Estimation

This repository contains implementations of Monte Carlo Pi estimation with different parallelization approaches to demonstrate performance characteristics and synchronization overhead.

## Overview

The project implements three approaches to estimate Pi using the Monte Carlo method:

1. **Task 3.1**: Single-threaded baseline
2. **Task 3.2**: Multi-threaded with local accumulation (optimal parallel design)
3. **Task 3.3**: Multi-threaded with shared variables and mutex (demonstrates contention)

## Files Structure

### Python Implementations
- `task_3_1_single_thread.py` - Baseline single-threaded implementation
- `task_3_2_multi_thread_local.py` - Multi-threaded with local accumulation
- `task_3_3_shared_variable_mutex.py` - Multi-threaded with shared counter and mutex
- `task_3_2b_multi_process.py` - Multi-process version (for comparison)

### C Implementations
- `task_3_1_single_thread.c` - C version of baseline
- `task_3_2_multi_thread_local.c` - C version with local accumulation
- `task_3_3_shared_variable_mutex.c` - C version with shared counter

### Scripts and Tools
- `run_all_tasks.sh` - Run all Python tasks and generate statistics
- `run_all_c_tasks.sh` - Run all C tasks
- `generate_stats.py` - Generate CSV and summary files for plotting

### Results and Analysis
- `results_all_tasks.txt` - Complete output from Python tasks
- `monte_carlo_pi_stats.csv` - CSV data for plotting
- `monte_carlo_pi_summary.txt` - Human-readable summary

## Key Findings

### Performance Comparison (C Implementation)

| Approach | 1 Thread | 2 Threads | 4 Threads | 8 Threads | 32 Threads |
|----------|----------|-----------|-----------|-----------|------------|
| **Task 3.1 (Baseline)** | 0.095s | - | - | - | - |
| **Task 3.2 (Local Accum.)** | 0.092s | 0.045s (2.1x) | 0.025s (3.7x) | 0.020s (4.7x) | 0.016s (5.8x) |
| **Task 3.3 (Shared Mutex)** | 0.140s | 0.276s (0.5x) | 0.399s (0.35x) | 0.526s (0.27x) | 0.463s (0.30x) |

### Insights
- **Task 3.2** demonstrates proper parallel design with significant speedup
- **Task 3.3** shows the overhead of frequent synchronization (contention)
- **Python threading** doesn't provide speedup for CPU-bound tasks due to GIL
- **C threading** achieves real parallelism without GIL limitations

## How to Run

### Quick Start
```bash
# Run all Python tasks and generate statistics
./run_all_tasks.sh

# Run all C tasks
./run_all_c_tasks.sh

# Generate statistics only
python3 generate_stats.py
```

### Individual Tasks
```bash
# Python versions
python3 task_3_1_single_thread.py
python3 task_3_2_multi_thread_local.py
python3 task_3_3_shared_variable_mutex.py

# C versions (after compiling)
gcc -O2 -pthread task_3_1_single_thread.c -o task_3_1_single_thread
gcc -O2 -pthread task_3_2_multi_thread_local.c -o task_3_2_multi_thread_local
gcc -O2 -pthread task_3_3_shared_variable_mutex.c -o task_3_3_shared_variable_mutex

./task_3_1_single_thread
./task_3_2_multi_thread_local
./task_3_3_shared_variable_mutex
```

## Plotting Results

The `generate_stats.py` script creates `monte_carlo_pi_stats.csv` which can be imported into Excel or used with Python matplotlib:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('monte_carlo_pi_stats.csv')

# Plot speedup comparison
task_3_2 = df[df['task'] == 'Task_3_2_Local_Accumulation']
task_3_3 = df[df['task'] == 'Task_3_3_Shared_Variable_Mutex']

plt.plot(task_3_2['threads'], task_3_2['speedup'], 'o-', label='Local Accumulation')
plt.plot(task_3_3['threads'], task_3_3['speedup'], 's-', label='Shared Variable')
plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.legend()
plt.savefig('speedup_comparison.png')
```

## Requirements

- **Python**: 3.6+
- **C Compiler**: GCC with pthreads support
- **Libraries**: Standard C library, Python threading/multiprocessing

## Educational Value

This project demonstrates:
- **Parallel programming concepts**: Threading, synchronization, contention
- **Performance analysis**: Speedup, efficiency, scalability
- **Language differences**: Python GIL vs C native threading
- **Design patterns**: Map-reduce, shared state management

## License

This project is for educational purposes as part of Operating Systems course work.