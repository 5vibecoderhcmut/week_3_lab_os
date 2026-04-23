import random
import time
import threading
import math

def monte_carlo_pi_multi_thread(num_samples, num_threads):
    start_time = time.time()
    inside_circle = 0
    threads = []
    samples_per_thread = num_samples // num_threads

    def worker():
        nonlocal inside_circle
        local_inside_circle = 0
        random.seed(42)

        for _ in range(samples_per_thread):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)

            if x**2 + y**2 <= 1:
                local_inside_circle += 1

        inside_circle += local_inside_circle
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return (inside_circle / num_samples) * 4, time.time() - start_time

if __name__ == "__main__":
    num_samples = 1000000
    num_threads = [1, 2, 4, 8, 16, 32, 64, 128]
    logs = []

    for n_threads in num_threads:
        pi_multi, time_multi = monte_carlo_pi_multi_thread(num_samples, n_threads)
        logs.append((n_threads, pi_multi, time_multi))
        print(f"Multi-threaded ({n_threads} threads): Accuracy: {(1 -abs(pi_multi-math.pi)/math.pi)*100}%, Time taken: {time_multi:.4f} seconds")