#!/bin/bash

# Script to run all three tasks sequentially and save output to a file

OUTPUT_FILE="results_all_tasks.txt"

echo "Running all three tasks sequentially..."
echo "Output will be saved to: $OUTPUT_FILE"
echo ""

# Clear the output file
> "$OUTPUT_FILE"

# Task 3.1 - Single Thread (Baseline)
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "Task 3.1 - Single Thread (Baseline)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"
python3 task_3_1_single_thread.py 2>&1 | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Task 3.2 - Multi-Thread with Local Accumulation
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "Task 3.2 - Multi-Thread (Local Accumulation)" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"
python3 task_3_2_multi_thread_local.py 2>&1 | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Task 3.3 - Shared Variable with Mutex
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "Task 3.3 - Shared Variable with Mutex" | tee -a "$OUTPUT_FILE"
echo "========================================" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"
python3 task_3_3_shared_variable_mutex.py 2>&1 | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

echo ""
echo "✓ All tasks completed!"
echo "✓ Results saved to: $OUTPUT_FILE"

# Generate statistics and plots
echo ""
echo "Generating statistics and plots..."
python3 generate_stats.py

echo ""
echo "✓ Statistics generated!"
echo "✓ CSV file: monte_carlo_pi_stats.csv"
echo "✓ Summary file: monte_carlo_pi_summary.txt"
