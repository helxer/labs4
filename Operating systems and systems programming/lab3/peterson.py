"""Step 4: Peterson's algorithm — software-only mutual exclusion for two processes.

Shared variables:
  flag[i] — process i wants to enter the critical section
  turn    — whose "turn" it is to wait (the polite one defers to the other)

Process i (i = 0 or 1):
  flag[i] = True
  turn = 1 - i          # let the OTHER go first
  while flag[1-i] and turn == 1-i:
      pass              # busy wait
  # --- critical section ---
  flag[i] = False
"""
import logging
import time
from pathlib import Path
from multiprocessing import Process, Value, Array

BASE_DIR = Path("lab_os_3")
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

ITERATIONS = 10_000


def peterson_worker(i: int, flag, turn, counter):
    """Process i (0 or 1) increments the shared counter ITERATIONS times,
    using Peterson's algorithm to guard the read-modify-write."""
    other = 1 - i
    for _ in range(ITERATIONS):
        flag[i] = 1
        turn.value = other
        while flag[other] == 1 and turn.value == other:
            pass  # busy wait until the other process leaves

        # --- critical section ---
        tmp = counter.value
        counter.value = tmp + 1
        # --- end critical section ---

        flag[i] = 0


def main():
    BASE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    # 'b' = signed char (used as boolean 0/1); lock=False — we provide our own protocol
    flag = Array('b', [0, 0], lock=False)
    turn = Value('i', 0, lock=False)
    counter = Value('i', 0, lock=False)
    expected = 2 * ITERATIONS

    p0 = Process(target=peterson_worker, args=(0, flag, turn, counter))
    p1 = Process(target=peterson_worker, args=(1, flag, turn, counter))

    start = time.time()
    p0.start()
    p1.start()
    p0.join()
    p1.join()
    elapsed = time.time() - start

    actual = counter.value
    lost = expected - actual
    msg = (
        f"Peterson's algorithm: expected={expected} actual={actual} "
        f"lost_updates={lost} time={elapsed:.4f}s"
    )
    print(msg)
    logging.info(msg)

    out = OUTPUT_DIR / "peterson_result.txt"
    with out.open('w') as f:
        f.write(msg + '\n')
    return actual, expected


if __name__ == "__main__":
    main()
