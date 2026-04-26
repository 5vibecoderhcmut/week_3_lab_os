"""
Task 3.2B - Multi-Process with Local Accumulation (Correct for CPU-bound)
This version uses multiprocessing instead of threading for CPU-bound tasks.

Why multiprocessing works:
- Each process has its own GIL
- Processes run in parallel on multiple CPU cores
- Achieves TRUE speedup for CPU-bound computations
"""

import random
import time
import math
from multiprocessing import Process, Queue


def worker_process(process_id, samples_per_process, result_queue):
    """
    Worker function for each process.
    Each process has its own GIL and Python interpreter.
    """
    # Each process gets a unique seed
    random.seed(42 + process_id)
    local_inside_circle = 0
    
    # Compute samples
    for _ in range(samples_per_process):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 <= 1:
            local_inside_circle += 1
    
    # Send result to main process (thread-safe queue)
    result_queue.put(local_inside_circle)


def monte_carlo_pi_multi_process(num_samples, num_processes):
    """
    Multi-process Monte Carlo estimation of Pi.
    Each process runs independently on a separate CPU core.
    
    Args:
        num_samples: Total number of random points
        num_processes: Number of processes to use
    
    Returns:
        tuple: (estimated_pi, execution_time)
    """
    samples_per_process = num_samples // num_processes
    result_queue = Queue()
    processes = []
    
    start_time = time.time()
    
    # Create and start processes
    for process_id in range(num_processes):
        p = Process(target=worker_process, args=(process_id, samples_per_process, result_queue))
        processes.append(p)
        p.start()
    
    # Wait for all processes to complete
    for p in processes:
        p.join()
    
    elapsed_time = time.time() - start_time
    
    # Collect results from all processes
    total_inside_circle = 0
    while not result_queue.empty():
        total_inside_circle += result_queue.get()
    
    estimated_pi = (total_inside_circle / num_samples) * 4
    
    return estimated_pi, elapsed_time


def measure_performance(num_samples, process_counts, num_runs=3):
    """
    Measure the performance of multi-process approach.
    """
    baseline_time = None
    results = {}
    
    print(f"Running multi-process approach with {num_samples:,} samples...")
    print(f"Running {num_runs} times per configuration for averaging...\n")
    
    for num_processes in process_counts:
        times = []
        pi_estimates = []
        
        print(f"Testing with {num_processes:2d} process(es)...", end=" ", flush=True)
        
        for run in range(num_runs):
            estimated_pi, elapsed_time = monte_carlo_pi_multi_process(num_samples, num_processes)
            times.append(elapsed_time)
            pi_estimates.append(estimated_pi)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        avg_pi = sum(pi_estimates) / len(pi_estimates)
        accuracy = (1 - abs(avg_pi - math.pi) / math.pi) * 100
        
        # Store baseline time (single process)
        if num_processes == 1:
            baseline_time = avg_time
        
        # Calculate speedup
        speedup = baseline_time / avg_time if baseline_time else 1.0
        efficiency = (speedup / num_processes) * 100
        
        results[num_processes] = {
            'avg_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'all_times': times,
            'estimated_pi': avg_pi,
            'accuracy': accuracy,
            'speedup': speedup,
            'efficiency': efficiency
        }
        
        print(f"Avg time: {avg_time:.6f}s, Speedup: {speedup:.4f}x, Efficiency: {efficiency:.2f}%")
    
    return results, baseline_time


if __name__ == "__main__":
    # Use smaller process count due to process creation overhead
    num_samples = 10**7
    process_counts = [1, 2, 4, 8]
    
    results, baseline_time = measure_performance(num_samples, process_counts, num_runs=3)
    
    print("\n" + "="*90)
    print("MULTI-PROCESS (TRUE PARALLELISM) RESULTS")
    print("="*90)
    print(f"{'Processes':<12} {'Avg Time (s)':<15} {'Speedup':<12} {'Efficiency':<12} {'Accuracy':<12}")
    print("-"*90)
    
    for num_processes in process_counts:
        result = results[num_processes]
        print(f"{num_processes:<12} {result['avg_time']:<15.6f} {result['speedup']:<12.4f}x "
              f"{result['efficiency']:<12.2f}% {result['accuracy']:<12.4f}%")
    
    print("="*90)
    print(f"\nTrue Pi: {math.pi:.8f}")
    print(f"Estimated Pi (final run): {results[process_counts[-1]]['estimated_pi']:.8f}")
    print(f"\nBaseline time (1 process): {baseline_time:.6f} seconds")
    print(f"\nKey Insight:")
    print(f"Multiprocessing achieves REAL speedup because each process has its own GIL!")
    print(f"This is the correct approach for CPU-bound tasks in Python.")
