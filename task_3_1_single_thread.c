#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

static double get_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

long long count_inside_circle(long long samples, unsigned int seed) {
    long long inside = 0;
    unsigned int state = seed;
    for (long long i = 0; i < samples; ++i) {
        double x = (double)rand_r(&state) / RAND_MAX * 2.0 - 1.0;
        double y = (double)rand_r(&state) / RAND_MAX * 2.0 - 1.0;
        if (x*x + y*y <= 1.0) {
            inside++;
        }
    }
    return inside;
}

int main(void) {
    const long long num_samples = 10000000LL;
    const int num_runs = 5;
    double total_time = 0.0;
    double min_time = 1e9;
    double max_time = 0.0;
    double avg_pi = 0.0;

    printf("Running single-threaded approach with %lld samples...\n", num_samples);
    printf("Running %d times to compute average...\n\n", num_runs);

    for (int run = 0; run < num_runs; ++run) {
        double start = get_seconds();
        long long inside = count_inside_circle(num_samples, 42 + run);
        double elapsed = get_seconds() - start;
        double estimated_pi = (double)inside / (double)num_samples * 4.0;
        avg_pi += estimated_pi;
        total_time += elapsed;
        if (elapsed < min_time) min_time = elapsed;
        if (elapsed > max_time) max_time = elapsed;
        printf("Run %d: time = %.6f s, pi = %.8f\n", run + 1, elapsed, estimated_pi);
    }

    avg_pi /= num_runs;
    double avg_time = total_time / num_runs;
    double accuracy = (1.0 - fabs(avg_pi - M_PI) / M_PI) * 100.0;

    printf("\n=============================================================\n");
    printf("BASELINE (SINGLE-THREADED) RESULTS\n");
    printf("=============================================================\n");
    printf("Number of samples: %lld\n", num_samples);
    printf("Number of runs: %d\n", num_runs);
    printf("Average time: %.6f s\n", avg_time);
    printf("Min time: %.6f s\n", min_time);
    printf("Max time: %.6f s\n", max_time);
    printf("Estimated Pi: %.8f\n", avg_pi);
    printf("True Pi: %.8f\n", M_PI);
    printf("Accuracy: %.4f%%\n", accuracy);
    printf("=============================================================\n");
    return 0;
}
