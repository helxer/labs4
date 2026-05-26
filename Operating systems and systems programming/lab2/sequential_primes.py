import time
import logging
from pathlib import Path

BASE_DIR = Path("lab_os_2")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"


def is_prime(n: int) -> bool:
    """Trivial-division primality check."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def load_numbers():
    with (INPUT_DIR / "numbers.txt").open('r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def main():
    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    numbers = load_numbers()
    print(f"Loaded {len(numbers)} numbers. Running sequential primality test...")

    start = time.time()
    primes = [n for n in numbers if is_prime(n)]
    elapsed = time.time() - start

    output_file = OUTPUT_DIR / "primes_sequential.txt"
    with output_file.open('w') as f:
        f.write('\n'.join(str(p) for p in primes))

    msg = (
        f"Sequential: total={len(numbers)} primes={len(primes)} "
        f"time={elapsed:.4f}s"
    )
    print(msg)
    logging.info(msg)

    with (LOGS_DIR / "timing.log").open('a') as tf:
        tf.write(msg + '\n')

    return elapsed


if __name__ == "__main__":
    main()