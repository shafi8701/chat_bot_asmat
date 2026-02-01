import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "chunking.yaml"

with open(CONFIG_PATH) as f:
    CHUNKING_CONFIG = yaml.safe_load(f)["chunking"]