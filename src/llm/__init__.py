# Global llm object to ensure singleton class structure is followed...
_llm = None


# src/llm/factory.py
from src.llm.openai_llm import OpenAILLM

#YAML convert to readable json config...
import yaml
from pathlib import Path
_CONFIG_PATH = Path("src/config/llm.yaml")

def _load_config():
    with open(_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_llm():
    """
    Factory method:
    - Loads YAML once
    - Instantiates correct llm service
    - Returns singleton
    """

    global _llm

    if _llm is not None:
        return _llm
    
    CONFIG = _load_config()

    method = CONFIG["llm"]["method"]

    if method == "openai":
        cfg = CONFIG["openai"]
        _chunking = OpenAILLM(cfg["api_key"], cfg["model"], cfg["temperature"])
    else:
        raise ValueError(f"Unsupported llm method: {method}")
    return _llm
