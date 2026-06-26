"""
Central configuration for Health Hub PRO.

API keys are NEVER hard-coded here. They are loaded from (in order):
  1. .streamlit/secrets.toml   -> st.secrets["USDA_API_KEY"] / ["GROQ_API_KEY"]
  2. environment variables      -> USDA_API_KEY / GROQ_API_KEY

This keeps your private keys out of the source code so they can't be
read or misused by anyone who sees the project files.
"""
import os
from pathlib import Path

import streamlit as st


def _get_secret(key: str, default: str = "") -> str:
    """Read a secret from st.secrets first, then the environment."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        # No secrets.toml present / not running under Streamlit yet.
        pass
    return os.environ.get(key, default).strip()


# --- Private API keys (resolved at runtime, kept out of source) ---------
USDA_API_KEY = _get_secret("USDA_API_KEY")
GROQ_API_KEY = _get_secret("GROQ_API_KEY")

USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

# --- Local data storage (gitignored) ------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
HISTORY_FILE = DATA_DIR / "chat_history.json"

# --- App constants ------------------------------------------------------
APP_NAME = "Health Hub PRO"
APP_ICON = "💎"

FOOD_CATEGORIES = {
    "Protein": "🥩",
    "Carb": "🍞",
    "Fruit": "🍎",
    "Vegetable": "🥦",
    "Dairy": "🥛",
    "Fat": "🥑",
    "Legume": "🫘",
    "Nut": "🥜",
    "Other": "🍽️",
}

# Aurora palette used across the UI
COLORS = {
    "primary": "#7c5cff",
    "secondary": "#ff6ec7",
    "accent": "#34e7c8",
    "warning": "#ffb347",
    "text": "#e8e9f3",
    "muted": "#a9adc9",
}
