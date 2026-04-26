"""
Task 3.3 - Approach 3: Shared Variable with Synchronization
This version uses multiprocessing and shared state with a lock.

Design:
- Use a shared counter across processes
- Each process computes a local result first
- Then each process updates the shared counter inside a locked section

Why this changes Task 3:
- It preserves the shared-variable-with-synchronization model
- It also allows real speedup for a CPU-bound workload
- The lock is held only briefly during final update

Measurement:
- Same setup as other approaches
- Compare execution time and speedup
- Show how multiprocessing can improve performance over single-process baseline
"""

import random
import time
import math
from multiprocessing import Process, Manager


def worker(process_id, samples_per_process, shared_counter, lock):
    """
    Worker function for each process.
    Each process computes its local count first, then updates shared counter.
    """
    random.seed(42 + process_id)
    local_inside_circle = 0
    
    for _ in range(samples_per_process):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            local_inside_circle += 1
    
    # Update shared counter under lock once per process
    with lock:
        shared_counter.value += local_inside_circle


def monte_carlo_pi_multi_process_mutex(num_samples, num_processes):
    """
    Multi-process Monte Carlo estimation of Pi using a shared counter and lock.
    """
    samples_per_process = num_samples // num_processes
    manager = Manager()
    shared_counter = manager.Value('i', 0)
    lock = manager.Lock()
    processes = []
    
    start_time = time.time()
    
    for process_id in range(num_processes):
        process = Process(
            target=worker,
            args=(process_id, samples_per_process, shared_counter, lock)
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    elapsed_time = time.time() - start_time
    estimated_pi = (shared_counter.value / num_samples) * 4
    return estimated_pi, elapsed_time


def measure_performance(num_samples, process_counts, num_runs=3):
    """
    Measure the performance of the shared-variable multiprocessing approach.
    """
    baseline_time = None
    results = {}
    
    print(f"Running multiprocessing approach (shared counter with lock) with {num_samples:,} samples...")
    print(f"Running {num_runs} times per configuration for averaging...\n")
    
    for num_processes in process_counts:
        times = []
        pi_estimates = []
        
        print(f"Testing with {num_processes:2d} process(es)...", end=" ", flush=True)
        
        for run in range(num_runs):
            estimated_pi, elapsed_time = monte_carlo_pi_multi_process_mutex(num_samples, num_processes)
            times.append(elapsed_time)
            pi_estimates.append(estimated_pi)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        avg_pi = sum(pi_estimates) / len(pi_estimates)
        accuracy = (1 - abs(avg_pi - math.pi) / math.pi) * 100
        
        if num_processes == 1:
            baseline_time = avg_time
        
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
    num_samples = 10**7
    process_counts = [1, 2, 4, 8]
    
    results, baseline_time = measure_performance(num_samples, process_counts, num_runs=3)
    
    print("\n" + "="*90)
    print("MULTI-PROCESS (SHARED VARIABLE WITH LOCK) RESULTS")
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
    print(f"Maximum speedup achieved: {results[max(results.keys())]['speedup']:.4f}x")
    print("\nThis version uses a shared counter plus a lock across processes, but only updates the shared state once per process.")
    print("It therefore still shows speedup while preserving the shared-variable-with-synchronization pattern.")
