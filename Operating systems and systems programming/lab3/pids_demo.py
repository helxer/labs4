"""Step 1 & 2: Display PID/PPID hierarchy and demonstrate OS scheduling
by spawning parallel child processes with sleep delays."""
import os
import time
import logging
from pathlib import Path
from multiprocessing import Process

BASE_DIR = Path("lab_os_3")
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"


def setup_directories():
    BASE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    OUTPUT_DIR.chmod(0o755)
    LOGS_DIR.chmod(0o700)


def worker(name: str, delay: float):
    """Child process: prints identity, sleeps, prints again to show preemption."""
    print(f"[{name}] start  PID={os.getpid()}  PPID={os.getppid()}", flush=True)
    for i in range(3):
        time.sleep(delay)
        print(f"[{name}] tick {i+1}  PID={os.getpid()}  t={time.strftime('%H:%M:%S.%f')[:-3]}", flush=True)
    print(f"[{name}] done   PID={os.getpid()}", flush=True)


def main():
    setup_directories()
    parent_pid = os.getpid()
    print(f"=== Parent process ===  PID={parent_pid}  PPID={os.getppid()}")
    logging.info(f"Parent PID={parent_pid} PPID={os.getppid()}")

    children = [
        Process(target=worker, args=("A", 0.4)),
        Process(target=worker, args=("B", 0.3)),
        Process(target=worker, args=("C", 0.5)),
    ]

    for p in children:
        p.start()

    print(f"\n=== Process tree (parent={parent_pid}) ===")
    for p in children:
        print(f"  child PID={p.pid}  name={p.name}")

    for p in children:
        p.join()

    print("\n=== All children finished ===")
    logging.info("All children joined")


if __name__ == "__main__":
    main()
