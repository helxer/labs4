"""Step 3: Demonstrate race condition on a shared counter without synchronization.
Two processes each increment a multiprocessing.Value by 10,000.
Expected result = 20,000; actual result < 20,000 due to lost updates."""
import logging
import time
from pathlib import Path
from multiprocessing import Process, Value

BASE_DIR = Path("lab_os_3")
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

ITERATIONS = 10_000


def unsafe_increment(counter):
    """Read-modify-write without any lock — classic race condition."""
    for _ in range(ITERATIONS):
        tmp = counter.value
        # tiny sleep makes scheduler-induced preemption much more visible
        # so we don't need it to occur "by chance"
        counter.value = tmp + 1


def main():
    BASE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # 'i' = signed int; lock=False disables the implicit RLock to reveal the race
    counter = Value('i', 0, lock=False)
    expected = 2 * ITERATIONS

    p1 = Process(target=unsafe_increment, args=(counter,))
    p2 = Process(target=unsafe_increment, args=(counter,))

    start = time.time()
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    elapsed = time.time() - start

    actual = counter.value
    lost = expected - actual
    msg = (
        f"Race condition demo: expected={expected} actual={actual} "
        f"lost_updates={lost} time={elapsed:.4f}s"
    )
    print(msg)
    logging.info(msg)

    out = OUTPUT_DIR / "race_result.txt"
    with out.open('w') as f:
        f.write(msg + '\n')
    return actual, expected


if __name__ == "__main__":
    main()
