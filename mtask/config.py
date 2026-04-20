import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "mtask"
CONFIG_FILE = CONFIG_DIR / "config.json"

def save_config(token: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"access_token": token}, f)

def load_config() -> dict[str, str]:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_token() -> str | None:
    config = load_config()
    return config.get("access_token")
