"""Paths, port, club name and colours."""
import os
import secrets
from pathlib import Path

CLUB_NAME = "Aquinas Board Games" 

# club.db, logo.jpg and crash_log.txt sit in the folder that holds this package
# (set CLUB_TRACKER_HOME to keep them somewhere else)
BASE_DIR = Path(os.environ.get("CLUB_TRACKER_HOME") or Path(__file__).resolve().parent.parent)
DB_PATH = BASE_DIR / "club.db"
LOGO_PATH = BASE_DIR / "logo.jpg"
TROPHY_PATH = BASE_DIR / "trophy.jpg"
SPONGEBOB_PATH = BASE_DIR / "spongebob.gif"
LOG_PATH = BASE_DIR / "crash_log.txt"

PORT = 8765
TOKEN = secrets.token_urlsafe(16)  # stops other sites posting to our forms

THEME = {
    "sidebar": "#16110f", "hover": "#2c211b", "active": "#a65d36", "brand": "#e3a977",
    "accent": "#b5652f", "accent_h": "#96501f", "danger": "#b3261e", "danger_h": "#8f1d17",
    "bg": "#f3efea", "card": "#fffdfb", "text": "#241c18", "muted": "#7a6c63",
    "good": "#3a7d44", "alt": "#f7f0e9",
    "gold": "#fff0c2", "silver": "#e8e4df", "bronze": "#f1d3bb",
}
