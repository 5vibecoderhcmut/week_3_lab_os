#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <math.h>

typedef struct {
    long long samples;
    unsigned int seed;
    long long *shared_inside;
    pthread_mutex_t *mutex;
} ThreadData;

static double get_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void *worker(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    unsigned int state = data->seed;
    for (long long i = 0; i < data->samples; ++i) {
        double x = (double)rand_r(&state) / RAND_MAX * 2.0 - 1.0;
        double y = (double)rand_r(&state) / RAND_MAX * 2.0 - 1.0;
        if (x*x + y*y <= 1.0) {
            // Each thread updates the shared variable directly with mutex protection
            pthread_mutex_lock(data->mutex);
            *data->shared_inside += 1;
            pthread_mutex_unlock(data->mutex);
        }
    }
    return NULL;
}

int main(void) {
    const long long num_samples = 10000000LL;
    const int num_runs = 3;
    const int thread_counts[] = {1, 2, 4, 8, 16, 32};
    const int count_len = sizeof(thread_counts) / sizeof(thread_counts[0]);

    printf("Running multi-threaded shared variable with synchronization with %lld samples...\n", num_samples);
    printf("Running %d times per configuration...\n\n", num_runs);

    double baseline_time = 0.0;
    for (int t = 0; t < count_len; ++t) {
        int num_threads = thread_counts[t];
        double total_time = 0.0;
        double min_time = 1e9;
        double max_time = 0.0;
        double avg_pi = 0.0;

        for (int run = 0; run < num_runs; ++run) {
            pthread_t threads[num_threads];
            ThreadData data[num_threads];
            long long samples_per_thread = num_samples / num_threads;
            long long shared_inside = 0;
            pthread_mutex_t mutex;
            pthread_mutex_init(&mutex, NULL);

            for (int i = 0; i < num_threads; ++i) {
                data[i].samples = samples_per_thread;
                data[i].seed = 42u + (unsigned int)i + (unsigned int)run * 31u;
                data[i].shared_inside = &shared_inside;
                data[i].mutex = &mutex;
            }

            double start = get_seconds();
            for (int i = 0; i < num_threads; ++i) {
                pthread_create(&threads[i], NULL, worker, &data[i]);
            }
            for (int i = 0; i < num_threads; ++i) {
                pthread_join(threads[i], NULL);
            }
            double elapsed = get_seconds() - start;
            double estimated_pi = (double)shared_inside / (double)(samples_per_thread * num_threads) * 4.0;
            avg_pi += estimated_pi;
            total_time += elapsed;
            if (elapsed < min_time) min_time = elapsed;
            if (elapsed > max_time) max_time = elapsed;
            pthread_mutex_destroy(&mutex);
        }

        double avg_time = total_time / num_runs;
        avg_pi /= num_runs;
        double speedup = 0.0;
        double efficiency = 0.0;
        if (t == 0) {
            baseline_time = avg_time;
            speedup = 1.0;
            efficiency = 100.0;
        } else {
            speedup = baseline_time / avg_time;
            efficiency = speedup / num_threads * 100.0;
        }
        double accuracy = (1.0 - fabs(avg_pi - M_PI) / M_PI) * 100.0;
        printf("threads=%2d avg=%.6f min=%.6f max=%.6f speedup=%.4fx efficiency=%.2f%% accuracy=%.4f%%\n",
               num_threads, avg_time, min_time, max_time, speedup, efficiency, accuracy);
    }
    return 0;
}
