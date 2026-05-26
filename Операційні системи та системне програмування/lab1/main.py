import os
import random
import string
import time
import threading
from pathlib import Path
import logging
import matplotlib.pyplot as plt

BASE_DIR = Path("lab_os_1")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

def setup_logger():
    """Configures the logger to write to the logs directory."""
    log_file = LOGS_DIR / "app.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def setup_directories():
    """Creates directory structure and sets permissions."""
    print("Setting up directories...")
    try:
        BASE_DIR.mkdir(exist_ok=True)
        INPUT_DIR.mkdir(exist_ok=True)
        OUTPUT_DIR.mkdir(exist_ok=True)
        LOGS_DIR.mkdir(exist_ok=True)
        
        setup_logger()
        logging.info("Directories created.")

        INPUT_DIR.chmod(0o755)
        OUTPUT_DIR.chmod(0o755)
        LOGS_DIR.chmod(0o700)
        logging.info("Permissions set successfully.")
    except PermissionError as e:
        print(f"Permission error during setup: {e}")
        if logging.getLogger().hasHandlers():
            logging.error(f"Permission error during setup: {e}")
    except Exception as e:
        print(f"Error during setup: {e}")
        if logging.getLogger().hasHandlers():
            logging.error(f"Error during setup: {e}")

# Pre-generate a pool of random words to speed up file generation
WORDS_POOL = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(1000)]

def generate_files(num_files):
    """Generates N text files with at least 1000 lines each."""
    print(f"Generating {num_files} files in {INPUT_DIR}...")
    logging.info(f"Started generating {num_files} files.")
    
    # Clean existing generated files
    for filepath in INPUT_DIR.iterdir():
        if filepath.is_file():
            try:
                filepath.unlink()
            except Exception as e:
                logging.error(f"Failed to delete {filepath}: {e}")
            
    for i in range(1, num_files + 1):
        filename = f"file_{i:03d}.txt" # Padding with zeros for better sorting (e.g. file_001.txt)
        filepath = INPUT_DIR / filename
        
        try:
            with filepath.open('w') as f:
                lines = []
                for _ in range(1000):
                    line_words = random.choices(WORDS_POOL, k=random.randint(5, 15))
                    lines.append(' '.join(line_words) + '\n')
                f.writelines(lines)
        except PermissionError as e:
            logging.error(f"Permission error writing to {filepath}: {e}")
        except Exception as e:
            logging.error(f"Error writing to {filepath}: {e}")
            
    logging.info(f"Finished generating {num_files} files.")

def process_single_file(filepath):
    """Processes a single file and returns stats (filename, lines, words, chars, size)."""
    lines_count = 0
    words_count = 0
    chars_count = 0
    file_size = 0
    
    try:
        file_stat = filepath.stat()
        file_size = file_stat.st_size
        
        with filepath.open('r') as f:
            for line in f:
                lines_count += 1
                chars_count += len(line)
                words_count += len(line.split())
    except PermissionError as e:
        logging.error(f"Permission error reading {filepath}: {e}")
        return filepath.name, 0, 0, 0, 0
    except Exception as e:
        logging.error(f"Error reading {filepath}: {e}")
        return filepath.name, 0, 0, 0, 0
            
    return filepath.name, lines_count, words_count, chars_count, file_size

def process_sequential():
    """Processes all files sequentially."""
    logging.info("Started sequential processing.")
    results = []
    
    start_time = time.time()
    for filepath in INPUT_DIR.glob('*.txt'):
        results.append(process_single_file(filepath))
    end_time = time.time()
    
    # Write results
    results.sort() # Uses default sorting
    output_path = OUTPUT_DIR / "result_sequential.txt"
    try:
        with output_path.open('w') as f:
            for filename, lines, words, chars, size in results:
                f.write(f"{filename} lines={lines} words={words} chars={chars} size_bytes={size}\n")
    except PermissionError as e:
        logging.error(f"Permission error writing to {output_path}: {e}")
        
    logging.info("Finished sequential processing.")
    return end_time - start_time

def process_multithreaded():
    """Processes all files using multithreading."""
    logging.info("Started multithreaded processing.")
    results = []
    lock = threading.Lock()
    
    def worker(filepath):
        res = process_single_file(filepath)
        with lock:
            results.append(res)
            
    start_time = time.time()
    threads = []
    for filepath in INPUT_DIR.glob('*.txt'):
        t = threading.Thread(target=worker, args=(filepath,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    end_time = time.time()
    
    # Write results
    results.sort() # Uses default sorting
    output_path = OUTPUT_DIR / "result_threads.txt"
    try:
        with output_path.open('w') as f:
            for filename, lines, words, chars, size in results:
                f.write(f"{filename} lines={lines} words={words} chars={chars} size_bytes={size}\n")
    except PermissionError as e:
        logging.error(f"Permission error writing to {output_path}: {e}")

    logging.info("Finished multithreaded processing.")
    return end_time - start_time

def check_permissions(path):
    """Returns the last 3 octal digits of the path's permissions."""
    try:
        mode = path.stat().st_mode
        return oct(mode)[-3:]
    except Exception as e:
        return f"Error: {e}"

def run_benchmark():
    setup_directories()
    
    test_sizes = [100, 300, 500]
    seq_times = []
    mt_times = []
    
    print("\n--- Performance Benchmark ---")
    print(f"{'Files':<10} | {'Sequential (s)':<15} | {'Multithreaded (s)':<15} | {'Speedup':<10}")
    print("-" * 57)
    
    for n in test_sizes:
        generate_files(n)
        
        seq_time = process_sequential()
        mt_time = process_multithreaded()
        
        seq_times.append(seq_time)
        mt_times.append(mt_time)
        
        speedup = seq_time / mt_time if mt_time > 0 else 0
        print(f"{n:<10} | {seq_time:<15.4f} | {mt_time:<15.4f} | {speedup:<10.2f}x")
        
    print("-" * 57)
    
    # Generate Plot
    try:
        plt.figure(figsize=(8, 5))
        plt.plot(test_sizes, seq_times, marker='o', label='Sequential Processing')
        plt.plot(test_sizes, mt_times, marker='s', label='Multithreaded Processing')
        plt.title('Sequential vs Multithreaded Processing Time')
        plt.xlabel('Number of Files')
        plt.ylabel('Execution Time (seconds)')
        plt.legend()
        plt.grid(True)
        
        plot_path = OUTPUT_DIR / "benchmark_plot.png"
        plt.savefig(plot_path)
        print(f"\nPlot saved to {plot_path}")
    except Exception as e:
        print(f"\nCould not generate plot: {e}")
        logging.error(f"Could not generate plot: {e}")
    
    print("\nFile structure and permissions checking:")
    print(f"{BASE_DIR}: {check_permissions(BASE_DIR)}")
    print(f"{INPUT_DIR}: {check_permissions(INPUT_DIR)}")
    print(f"{OUTPUT_DIR}: {check_permissions(OUTPUT_DIR)}")
    print(f"{LOGS_DIR}: {check_permissions(LOGS_DIR)}")
    
if __name__ == "__main__":
    run_benchmark()
