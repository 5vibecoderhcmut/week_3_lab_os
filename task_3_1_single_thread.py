"""
Task 3.1 - Approach 1: Single Thread (Baseline)
This version establishes a reference for performance comparison.

Requirements:
- Generate a large number of points (10^7 or higher)
- Count how many fall inside the circle
- Measure total execution time
- Use a fixed random seed to ensure reproducibility
- Avoid printing inside loops (I/O distorts timing)
- Run the program multiple times and compute the average execution time
"""

import random
import time
import math


def monte_carlo_pi_single_thread(num_samples):
    """
    Single-threaded Monte Carlo estimation of Pi.
    
    Args:
        num_samples: Number of random points to generate
    
    Returns:
        tuple: (estimated_pi, execution_time)
    """
    random.seed(42)  # Fixed seed for reproducibility
    inside_circle = 0
    
    # Generate random points and count those inside the circle
    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 <= 1:
            inside_circle += 1
    
    # Estimate Pi: (inside_circle / num_samples) * 4
    estimated_pi = (inside_circle / num_samples) * 4
    
    return estimated_pi


def measure_performance(num_samples, num_runs=5):
    """
    Measure the performance of single-threaded approach over multiple runs.
    
    Args:
        num_samples: Number of random points to generate
        num_runs: Number of times to run the experiment
    
    Returns:
        dict: Statistics including average time, min, max, and estimated Pi
    """
    times = []
    pi_estimates = []
    
    print(f"Running single-threaded approach with {num_samples:,} samples...")
    print(f"Running {num_runs} times to compute average...")
    
    for run in range(num_runs):
        start_time = time.time()
        estimated_pi = monte_carlo_pi_single_thread(num_samples)
        elapsed_time = time.time() - start_time
        
        times.append(elapsed_time)
        pi_estimates.append(estimated_pi)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    avg_pi = sum(pi_estimates) / len(pi_estimates)
    accuracy = (1 - abs(avg_pi - math.pi) / math.pi) * 100
    
    return {
        'num_samples': num_samples,
        'num_runs': num_runs,
        'average_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'all_times': times,
        'estimated_pi': avg_pi,
        'accuracy': accuracy,
        'true_pi': math.pi
    }


if __name__ == "__main__":
    # Generate a large number of points for baseline measurement
    num_samples = 10**7  # 10 million points
    
    results = measure_performance(num_samples, num_runs=5)
    
    # Print results
    print("\n" + "="*70)
    print("BASELINE (SINGLE-THREADED) RESULTS")
    print("="*70)
    print(f"Number of samples:    {results['num_samples']:,}")
    print(f"Number of runs:       {results['num_runs']}")
    print(f"Average execution time: {results['average_time']:.6f} seconds")
    print(f"Min execution time:     {results['min_time']:.6f} seconds")
    print(f"Max execution time:     {results['max_time']:.6f} seconds")
    print(f"Std deviation:          {(max(results['all_times']) - min(results['all_times'])) / 2:.6f} seconds")
    print(f"\nEstimated Pi:         {results['estimated_pi']:.8f}")
    print(f"True Pi:              {results['true_pi']:.8f}")
    print(f"Accuracy:             {results['accuracy']:.4f}%")
    print("="*70)
