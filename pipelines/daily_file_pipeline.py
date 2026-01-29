import time
from pathlib import Path
from src.core.etl import process_file

INCOMING_DIR = Path("data/incoming")
PROCESSED_DIR = Path("data/processed")
POLL_INTERVAL = 5


INCOMING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline():
    print("🚀 Daily ETL Pipeline Started")
    print(f"Watching: {INCOMING_DIR.resolve()}")


    while True:
        files = list(INCOMING_DIR.glob("*"))


        for file_path in files:
            try:
                process_file(file_path, PROCESSED_DIR)
            except Exception as e:
                print(f"❌ Failed processing {file_path.name}: {e}")

time.sleep(POLL_INTERVAL)