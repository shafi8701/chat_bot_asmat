from pathlib import Path
from src.core.etl import process_file

INCOMING_DIR = Path("/app/data/incoming")
PROCESSED_DIR = Path("/app/data/processed")

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline():
    print("🚀 One-Time ETL Run Started")
    print(f"📂 Scanning: {INCOMING_DIR}")

    files = (
        list(INCOMING_DIR.glob("*.pdf")) +
        list(INCOMING_DIR.glob("*.txt"))
    )

    if not files:
        print("📭 No files found. Exiting.")
        return

    for file_path in files:
        try:
            print(f"📥 Processing: {file_path.name}")
            process_file(file_path, PROCESSED_DIR)
        except Exception as e:
            print(f"❌ Failed processing {file_path.name}: {e}")

    print("✅ ETL Run Complete. Exiting.")


if __name__ == "__main__":
    run_pipeline()