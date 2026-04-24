import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import threading

import platform
import psutil
import os

NUM_SAMPLES = 10**7
NUM_RUNS = 5
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]

TRUE_PI = math.pi

def print_system_info():
    print("\n===== SYSTEM INFO =====")

    print(f"OS: {platform.system()} {platform.release()}")

    print(f"Python Version: {platform.python_version()}")

    print(f"CPU: {platform.processor()}")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Logical threads: {psutil.cpu_count(logical=True)}")

    freq = psutil.cpu_freq()
    if freq:
        print(f"CPU Frequency: {freq.current:.2f} MHz")

    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")

    process = psutil.Process(os.getpid())
    print(f"Process PID: {process.pid}")

    print("========================\n")


def run_single_thread():
    times = []

    for _ in range(NUM_RUNS):
        random.seed(42)
        inside = 0

        start = time.time()

        for _ in range(NUM_SAMPLES):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)

            if x*x + y*y <= 1:
                inside += 1

        times.append(time.time() - start)

    pi_est = (inside / NUM_SAMPLES) * 4
    return pi_est, np.mean(times)


def run_multithread():
    results = []

    for n_threads in THREAD_COUNTS:
        samples_per_thread = NUM_SAMPLES // n_threads

        for _ in range(NUM_RUNS):
            threads = []
            local_results = [0] * n_threads

            start = time.time()

            def worker(tid):
                local = 0
                random.seed(42 + tid)

                for _ in range(samples_per_thread):
                    x = random.uniform(-1, 1)
                    y = random.uniform(-1, 1)

                    if x*x + y*y <= 1:
                        local += 1

                local_results[tid] = local

            for i in range(n_threads):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            total = sum(local_results)
            pi_est = (total / NUM_SAMPLES) * 4

            results.append((n_threads, time.time() - start, pi_est))

    return results


def run_shared():
    results = []

    for n_threads in THREAD_COUNTS:
        samples_per_thread = NUM_SAMPLES // n_threads

        for _ in range(NUM_RUNS):
            threads = []
            lock = threading.Lock()
            inside = 0

            start = time.time()

            def worker(tid):
                nonlocal inside
                random.seed(42 + tid)

                for _ in range(samples_per_thread):
                    x = random.uniform(-1, 1)
                    y = random.uniform(-1, 1)

                    if x*x + y*y <= 1:
                        with lock:
                            inside += 1

            for i in range(n_threads):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            pi_est = (inside / NUM_SAMPLES) * 4
            results.append((n_threads, time.time() - start, pi_est))

    return results


def avg_results(results):
    data = {}
    for t, time_val, _ in results:
        data.setdefault(t, []).append(time_val)

    return {k: np.mean(v) for k, v in data.items()}


if __name__ == "__main__":

    print_system_info()

    pi_base, base_time = run_single_thread()

    print("\nSingle Thread (Baseline):")
    print(f"Pi ≈ {pi_base}, Time = {base_time}s")

    multi_results = run_multithread()
    shared_results = run_shared()

    multi_time = avg_results(multi_results)
    shared_time = avg_results(shared_results)

    speedup_multi = [base_time / multi_time[t] for t in THREAD_COUNTS]
    speedup_shared = [base_time / shared_time[t] for t in THREAD_COUNTS]

    plt.figure(figsize=(10, 5))
    plt.plot(THREAD_COUNTS, [multi_time[t] for t in THREAD_COUNTS],
             marker='o', label='Multi-Thread (Local Accumulation Pattern)')
    plt.plot(THREAD_COUNTS, [shared_time[t] for t in THREAD_COUNTS],
             marker='o', label='Shared Variable with Synchronization')
    plt.plot(THREAD_COUNTS, [base_time] * len(THREAD_COUNTS),
                marker='o', label='Single Thread (Baseline)', linestyle='--')

    plt.xlabel("Threads")
    plt.ylabel("Time (s)")
    plt.title("Execution Time vs Threads")
    plt.legend()
    plt.grid()
    plt.savefig("time_vs_threads.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(THREAD_COUNTS, speedup_multi,
             marker='o', label='Multi-Thread (Local Accumulation Pattern)')
    plt.plot(THREAD_COUNTS, speedup_shared,
             marker='o', label='Shared Variable with Synchronization')

    plt.xlabel("Threads")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Threads")
    plt.legend()
    plt.grid()
    plt.savefig("speedup_vs_threads.png")
    plt.close()

    print("\nACCURACY CHECK:")
    print(f"Error = {abs(pi_base - TRUE_PI)}")
