"""Database connection, tables and the common lookups."""
import sqlite3

from .config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);
CREATE TABLE IF NOT EXISTS tournaments (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL UNIQUE COLLATE NOCASE,
    win_pts  INTEGER NOT NULL DEFAULT 3,
    draw_pts INTEGER NOT NULL DEFAULT 1,
    loss_pts INTEGER NOT NULL DEFAULT 0,
    created  TEXT NOT NULL,
    archived INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS results (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_id INTEGER NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    week_no       INTEGER NOT NULL,
    played_on     TEXT NOT NULL,
    player1_id    INTEGER NOT NULL REFERENCES players(id),
    player2_id    INTEGER NOT NULL REFERENCES players(id),
    score1        INTEGER NOT NULL,
    score2        INTEGER NOT NULL
);
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    # older databases won't have the archived column yet
    columns = [r["name"] for r in conn.execute("PRAGMA table_info(tournaments)")]
    if "archived" not in columns:
        conn.execute("ALTER TABLE tournaments ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
        conn.commit()
    return conn


def get_tournaments(conn, archived=None):
    # None = everything (active first), False = active only, True = archived only
    if archived is None:
        return conn.execute("SELECT * FROM tournaments ORDER BY archived, id").fetchall()
    return conn.execute("SELECT * FROM tournaments WHERE archived = ? ORDER BY id",
                        (1 if archived else 0,)).fetchall()


def choose_tournament(rows, wanted):
    for r in rows:
        if str(r["id"]) == str(wanted):
            return r
    return rows[0]


def player_names(conn):
    return [r["name"] for r in conn.execute("SELECT name FROM players ORDER BY name")]
