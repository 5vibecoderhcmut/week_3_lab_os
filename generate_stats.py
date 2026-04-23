#!/usr/bin/env python3
"""
Script to run all three C tasks and generate a statistics file for plotting.
Output format: CSV with headers for easy plotting in Excel, Python matplotlib, etc.
"""

import subprocess
import re
import csv
import os

def run_command(cmd):
    """Run a command and return its output as string."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def parse_task_3_1(output):
    """Parse task 3.1 output and return baseline time."""
    # Extract average time from task 3.1
    match = re.search(r'Average time:\s+([\d.]+)', output)
    if match:
        return float(match.group(1))
    return None

def parse_task_3_2_and_3(output, task_name):
    """Parse task 3.2 and 3.3 output and return list of (threads, avg_time, speedup, efficiency, accuracy)."""
    results = []
    lines = output.split('\n')
    for line in lines:
        # Match lines like: threads= 1 avg=0.099259 min=0.087747 max=0.121847 speedup=1.0000x efficiency=100.00% accuracy=99.9868%
        match = re.search(r'threads=\s*(\d+)\s+avg=([\d.]+).*speedup=([\d.]+)x.*efficiency=([\d.]+)%.*accuracy=([\d.]+)%', line)
        if match:
            threads = int(match.group(1))
            avg_time = float(match.group(2))
            speedup = float(match.group(3))
            efficiency = float(match.group(4))
            accuracy = float(match.group(5))
            results.append({
                'task': task_name,
                'threads': threads,
                'avg_time': avg_time,
                'speedup': speedup,
                'efficiency': efficiency,
                'accuracy': accuracy
            })
    return results

def main():
    # Ensure we're in the right directory
    os.chdir('/Users/tinngo/Documents/Code/Pi')

    # Compile programs if not already done
    print("Compiling programs...")
    subprocess.run('gcc -O2 -pthread task_3_1_single_thread.c -o task_3_1_single_thread', shell=True)
    subprocess.run('gcc -O2 -pthread task_3_2_multi_thread_local.c -o task_3_2_multi_thread_local', shell=True)
    subprocess.run('gcc -O2 -pthread task_3_3_shared_variable_mutex.c -o task_3_3_shared_variable_mutex', shell=True)

    # Run task 3.1
    print("Running Task 3.1...")
    output_3_1 = run_command('./task_3_1_single_thread')
    baseline_time = parse_task_3_1(output_3_1)

    # Run task 3.2
    print("Running Task 3.2...")
    output_3_2 = run_command('./task_3_2_multi_thread_local')
    results_3_2 = parse_task_3_2_and_3(output_3_2, 'Task_3_2_Local_Accumulation')

    # Run task 3.3
    print("Running Task 3.3...")
    output_3_3 = run_command('./task_3_3_shared_variable_mutex')
    results_3_3 = parse_task_3_2_and_3(output_3_3, 'Task_3_3_Shared_Variable_Mutex')

    # Combine all results
    all_results = results_3_2 + results_3_3

    # Write to CSV file
    csv_filename = 'monte_carlo_pi_stats.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['task', 'threads', 'avg_time', 'speedup', 'efficiency', 'accuracy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in all_results:
            writer.writerow(result)

    print(f"\nStatistics saved to {csv_filename}")
    print(f"Baseline time (Task 3.1): {baseline_time:.6f} seconds")
    print(f"Total data points: {len(all_results)}")

    # Also create a simple text summary
    txt_filename = 'monte_carlo_pi_summary.txt'
    with open(txt_filename, 'w') as f:
        f.write("Monte Carlo Pi Estimation - Performance Statistics\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Baseline (Task 3.1): {baseline_time:.6f} seconds\n\n")
        f.write("Task Results:\n")
        f.write("-" * 60 + "\n")
        for result in all_results:
            f.write(f"{result['task']}: {result['threads']} threads, "
                   f"Time: {result['avg_time']:.6f}s, "
                   f"Speedup: {result['speedup']:.4f}x, "
                   f"Efficiency: {result['efficiency']:.2f}%, "
                   f"Accuracy: {result['accuracy']:.4f}%\n")

    print(f"Summary saved to {txt_filename}")

    # Print sample of data
    print("\nSample data (first 5 rows):")
    print("Task,Threads,Avg_Time,Speedup,Efficiency,Accuracy")
    for i, result in enumerate(all_results[:5]):
        print(f"{result['task']},{result['threads']},{result['avg_time']:.6f},{result['speedup']:.4f},{result['efficiency']:.2f},{result['accuracy']:.4f}")

if __name__ == "__main__":
    main()