import time
import logging
import os
from pathlib import Path
from multiprocessing import Pool

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

from sequential_primes import is_prime, load_numbers

BASE_DIR = Path("lab_os_2")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

PROCESS_COUNTS = [1, 2, 4, 8]


def run_parallel(numbers, n_processes):
    """Filter primes using a Pool of n_processes; return (primes, elapsed)."""
    start = time.time()
    with Pool(processes=n_processes) as pool:
        mask = pool.map(is_prime, numbers, chunksize=max(1, len(numbers) // (n_processes * 4)))
    primes = [n for n, ok in zip(numbers, mask) if ok]
    elapsed = time.time() - start
    return primes, elapsed


def run_sequential(numbers):
    start = time.time()
    primes = [n for n in numbers if is_prime(n)]
    elapsed = time.time() - start
    return primes, elapsed


def main():
    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    numbers = load_numbers()
    print(f"Loaded {len(numbers)} numbers. CPU count = {os.cpu_count()}")

    seq_primes, seq_time = run_sequential(numbers)
    print(f"Sequential baseline: {seq_time:.4f}s, primes found = {len(seq_primes)}")

    results = [("sequential", 1, seq_time, 1.0)]
    timings_for_plot = {1: seq_time}

    for n_proc in PROCESS_COUNTS:
        primes, elapsed = run_parallel(numbers, n_proc)
        speedup = seq_time / elapsed if elapsed > 0 else 0.0
        results.append((f"pool-{n_proc}", n_proc, elapsed, speedup))
        timings_for_plot[n_proc] = elapsed

        out_file = OUTPUT_DIR / f"primes_pool_{n_proc}.txt"
        with out_file.open('w') as f:
            f.write('\n'.join(str(p) for p in primes))

        assert len(primes) == len(seq_primes), "Result mismatch between sequential and parallel"
        print(f"Pool({n_proc}): time={elapsed:.4f}s speedup={speedup:.2f}x")

    timing_log = LOGS_DIR / "timing.log"
    with timing_log.open('a') as tf:
        tf.write("\n--- multiprocessing run ---\n")
        tf.write(f"total_numbers={len(numbers)} cpu_count={os.cpu_count()}\n")
        tf.write(f"{'mode':<12} {'procs':<6} {'time_s':<10} {'speedup':<8}\n")
        for mode, n_proc, elapsed, speedup in results:
            tf.write(f"{mode:<12} {n_proc:<6} {elapsed:<10.4f} {speedup:<8.2f}\n")

    print("\n--- Summary ---")
    print(f"{'mode':<12} {'procs':<6} {'time_s':<10} {'speedup':<8}")
    for mode, n_proc, elapsed, speedup in results:
        print(f"{mode:<12} {n_proc:<6} {elapsed:<10.4f} {speedup:<8.2f}")

    if not HAS_MPL:
        print("matplotlib not available, skipping plot")
        return

    try:
        xs = PROCESS_COUNTS
        ys = [timings_for_plot[p] for p in xs]
        plt.figure(figsize=(8, 5))
        plt.plot(xs, ys, marker='o', label='multiprocessing.Pool')
        plt.axhline(y=seq_time, color='r', linestyle='--', label=f'Sequential ({seq_time:.2f}s)')
        plt.title('Prime search: execution time vs number of processes')
        plt.xlabel('Number of processes')
        plt.ylabel('Execution time (seconds)')
        plt.xticks(xs)
        plt.legend()
        plt.grid(True)
        plot_path = OUTPUT_DIR / "benchmark_plot.png"
        plt.savefig(plot_path)
        print(f"Plot saved -> {plot_path}")
    except Exception as e:
        logging.error(f"Could not generate plot: {e}")
        print(f"Plot generation failed: {e}")


if __name__ == "__main__":
    main()