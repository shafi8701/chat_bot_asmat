# src/config.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "chunking.yaml"

with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)

def get_chunking_method():
    return CONFIG["chunking"]["method"]