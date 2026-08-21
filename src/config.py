import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "data" / "system_config.json"


def load_config():
    """Load NetSage system configuration."""

    with CONFIG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)