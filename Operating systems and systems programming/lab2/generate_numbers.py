import random
import logging
from pathlib import Path

BASE_DIR = Path("lab_os_2")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

COUNT = 50_000
LOW = 100_000_000
HIGH = 10_000_000_000


def setup_directories():
    """Creates lab_os_2/{input,output,logs} with the same permissions as lab1."""
    BASE_DIR.mkdir(exist_ok=True)
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=LOGS_DIR / "app.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    INPUT_DIR.chmod(0o755)
    OUTPUT_DIR.chmod(0o755)
    LOGS_DIR.chmod(0o700)
    logging.info("Directories created and permissions set.")


def generate_numbers():
    """Generates COUNT random integers in [LOW, HIGH] and writes them to input/numbers.txt."""
    output_file = INPUT_DIR / "numbers.txt"
    logging.info(f"Generating {COUNT} numbers into {output_file}")

    numbers = [random.randint(LOW, HIGH) for _ in range(COUNT)]
    with output_file.open('w') as f:
        f.write('\n'.join(str(n) for n in numbers))

    logging.info(f"Wrote {COUNT} numbers to {output_file}")
    print(f"Generated {COUNT} numbers in range [{LOW}, {HIGH}] -> {output_file}")


if __name__ == "__main__":
    setup_directories()
    generate_numbers()