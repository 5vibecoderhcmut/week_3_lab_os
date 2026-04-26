"""
Task 3.2 - Approach 2: Multi-Thread with Local Accumulation Pattern
This is the correct parallel design for this problem.

Design:
- Create N threads
- Each thread processes nPoints/N samples
- Each thread maintains its own local counter
- After all threads are complete, the results are combined
- This corresponds to a map–reduce pattern:
  * Map phase: each thread independently computes partial results
  * Reduce phase: combine results into final output

Key constraints:
- No shared variable inside the main loop
- Each thread must use an independent random generator (or seed)
- Threads must not interfere with each other during computation

Measurement:
- Run with varying thread counts
- Record execution time for each configuration
- Compute speedup: Speedup = T_single / T_parallel
"""

import random
import time
import threading
import math


def monte_carlo_pi_multi_thread_local(num_samples, num_threads):
    """
    Multi-threaded Monte Carlo estimation of Pi using local accumulation.
    Each thread maintains its own local counter to avoid contention.
    
    Args:
        num_samples: Total number of random points to generate
        num_threads: Number of threads to use
    
    Returns:
        tuple: (estimated_pi, execution_time)
    """
    samples_per_thread = num_samples // num_threads
    results = []  # Thread-safe list to store results
    threads = []
    
    def worker(thread_id):
        """
        Worker function for each thread.
        Each thread has its own random seed and local counter.
        """
        # Each thread gets a unique seed based on its ID
        random.seed(42 + thread_id)
        local_inside_circle = 0
        
        # Each thread processes its assigned samples
        for _ in range(samples_per_thread):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            if x**2 + y**2 <= 1:
                local_inside_circle += 1
        
        # Store local result (no shared variable, no lock needed)
        results.append(local_inside_circle)
    
    # Create and start threads
    start_time = time.time()
    
    for thread_id in range(num_threads):
        thread = threading.Thread(target=worker, args=(thread_id,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    elapsed_time = time.time() - start_time
    
    # Reduce phase: combine all results
    total_inside_circle = sum(results)
    estimated_pi = (total_inside_circle / num_samples) * 4
    
    return estimated_pi, elapsed_time


def measure_performance(num_samples, thread_counts, num_runs=3):
    """
    Measure the performance of multi-threaded approach with varying thread counts.
    
    Args:
        num_samples: Number of random points to generate
        thread_counts: List of thread counts to test
        num_runs: Number of times to run each configuration
    
    Returns:
        dict: Performance metrics and speedup calculations
    """
    baseline_time = None
    results = {}
    
    print(f"Running multi-threaded approach with {num_samples:,} samples...")
    print(f"Running {num_runs} times per configuration for averaging...\n")
    
    for num_threads in thread_counts:
        times = []
        pi_estimates = []
        
        print(f"Testing with {num_threads:2d} thread(s)...", end=" ", flush=True)
        
        for run in range(num_runs):
            estimated_pi, elapsed_time = monte_carlo_pi_multi_thread_local(num_samples, num_threads)
            times.append(elapsed_time)
            pi_estimates.append(estimated_pi)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        avg_pi = sum(pi_estimates) / len(pi_estimates)
        accuracy = (1 - abs(avg_pi - math.pi) / math.pi) * 100
        
        # Store baseline time (single thread)
        if num_threads == 1:
            baseline_time = avg_time
        
        # Calculate speedup relative to single thread
        speedup = baseline_time / avg_time if baseline_time else 1.0
        efficiency = (speedup / num_threads) * 100  # Efficiency percentage
        
        results[num_threads] = {
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
    # Generate a large number of points
    num_samples = 10**7  # 10 million points
    
    # Test with various thread counts
    thread_counts = [1, 2, 4, 8, 16, 32, 64]
    
    results, baseline_time = measure_performance(num_samples, thread_counts, num_runs=3)
    
    # Print detailed results
    print("\n" + "="*90)
    print("MULTI-THREADED (LOCAL ACCUMULATION) RESULTS")
    print("="*90)
    print(f"{'Threads':<8} {'Avg Time (s)':<15} {'Speedup':<12} {'Efficiency':<12} {'Accuracy':<12}")
    print("-"*90)
    
    for num_threads in thread_counts:
        result = results[num_threads]
        print(f"{num_threads:<8} {result['avg_time']:<15.6f} {result['speedup']:<12.4f}x "
              f"{result['efficiency']:<12.2f}% {result['accuracy']:<12.4f}%")
    
    print("="*90)
    print(f"\nTrue Pi: {math.pi:.8f}")
    print(f"Estimated Pi (final run): {results[thread_counts[-1]]['estimated_pi']:.8f}")
    print(f"\nBaseline time (1 thread): {baseline_time:.6f} seconds")
    print(f"Maximum speedup achieved: {results[max(results.keys())]['speedup']:.4f}x")
