#!/bin/bash

# Script to compile and run all three C tasks sequentially

echo "Compiling and running all three C tasks..."
echo ""

# Compile all programs
echo "Compiling..."
gcc -O2 -pthread task_3_1_single_thread.c -o task_3_1_single_thread
gcc -O2 -pthread task_3_2_multi_thread_local.c -o task_3_2_multi_thread_local
gcc -O2 -pthread task_3_3_shared_variable_mutex.c -o task_3_3_shared_variable_mutex
echo "Compilation complete."
echo ""

# Run Task 3.1
echo "=========================================="
echo "Task 3.1 - Single Thread (Baseline)"
echo "=========================================="
./task_3_1_single_thread
echo ""

# Run Task 3.2
echo "=========================================="
echo "Task 3.2 - Multi-Thread (Local Accumulation)"
echo "=========================================="
./task_3_2_multi_thread_local
echo ""

# Run Task 3.3
echo "=========================================="
echo "Task 3.3 - Shared Variable with Synchronization"
echo "=========================================="
./task_3_3_shared_variable_mutex
echo ""

echo "All tasks completed!"
echo "Summary:"
echo "- Task 3.1: Baseline single-thread performance"
echo "- Task 3.2: Shows real speedup with local accumulation"
echo "- Task 3.3: Demonstrates synchronization overhead (no speedup)"