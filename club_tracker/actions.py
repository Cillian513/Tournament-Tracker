"""What happens when a form is posted."""
import sqlite3
from datetime import date

from .database import get_tournaments
from .helpers import UserError, back, clean_name, positive_or, to_int


def post_save_result(conn, f):
    keep = {"t": f.get("t"), "w": f.get("w")}
    try:
        rows = get_tournaments(conn)
        t = next((r for r in rows if str(r["id"]) == str(f.get("t"))), None)
        if not t:
            raise UserError("Please choose a tournament first.")
        if t["archived"]:
            raise UserError("That tournament is archived. Restore it on the Tournaments page to add results.")
        week = to_int(f.get("w"), "Week", 1, 99)
        try:
            played_on = date.fromisoformat(f.get("d", "").strip()).isoformat()
        except ValueError:
            raise UserError("Please enter the date as a valid date.")
        n1, n2 = clean_name(f.get("p1", "")), clean_name(f.get("p2", ""))
        if not n1 or not n2:
            raise UserError("Please enter both players.")
        if n1.lower() == n2.lower():
            raise UserError("A player can't play themselves.")
        s1, s2 = to_int(f.get("s1"), "Score"), to_int(f.get("s2"), "Score")

        added, ids = [], []
        for name in (n1, n2):
            row = conn.execute("SELECT id, name FROM players WHERE name = ?", (name,)).fetchone()
            if row:
                ids.append(row["id"])
            else:
                ids.append(conn.execute("INSERT INTO players (name) VALUES (?)", (name,)).lastrowid)
                added.append(name)
        conn.execute(
            """INSERT INTO results (tournament_id, week_no, played_on, player1_id, player2_id, score1, score2)
               VALUES (?,?,?,?,?,?,?)""", (t["id"], week, played_on, ids[0], ids[1], s1, s2))
        conn.commit()
        msg = f"Saved: {n1} {s1} - {s2} {n2}."
        if added:
            msg += " New player added: " + ", ".join(added) + "."
        return back("/record", **keep, msg=msg, kind="ok")
    except UserError as e:
        conn.rollback()
        return back("/record", **keep, d=f.get("d"), p1=f.get("p1"), p2=f.get("p2"),
                    s1=f.get("s1"), s2=f.get("s2"), msg=str(e), kind="err")


def post_delete_result(conn, f):
    conn.execute("DELETE FROM results WHERE id = ? AND tournament_id = ?",
                 (positive_or(f.get("id"), 0), positive_or(f.get("t"), 0)))
    conn.commit()
    return back("/record", t=f.get("t"), w=f.get("w"), msg="Result deleted.", kind="ok")


def post_add_player(conn, f):
    name = clean_name(f.get("name", ""))
    if not name:
        return back("/players", msg="Name can't be empty.", kind="err")
    try:
        conn.execute("INSERT INTO players (name) VALUES (?)", (name,))
        conn.commit()
        return back("/players", msg=f"Added {name}.", kind="ok")
    except sqlite3.IntegrityError:
        return back("/players", msg=f"{name} is already in the list.", kind="err")


def post_remove_player(conn, f):
    pid = positive_or(f.get("id"), 0)
    cur = conn.execute(
        """DELETE FROM players WHERE id = ?
           AND NOT EXISTS (SELECT 1 FROM results WHERE player1_id = ? OR player2_id = ?)""",
        (pid, pid, pid))
    conn.commit()
    return back("/players", kind="ok" if cur.rowcount else "err",
                msg="Player removed." if cur.rowcount else "That player has recorded matches, so can't be removed.")


def post_create_tournament(conn, f):
    try:
        name = clean_name(f.get("name", ""))
        if not name:
            raise UserError("Please enter a tournament name.")
        win, draw, loss = (to_int(f.get(k), label, 0, 1000)
                           for k, label in (("win", "Win points"), ("draw", "Draw points"), ("loss", "Loss points")))
        conn.execute(
            "INSERT INTO tournaments (name, win_pts, draw_pts, loss_pts, created) VALUES (?,?,?,?,?)",
            (name, win, draw, loss, date.today().isoformat()))
        conn.commit()
        return back("/tournaments", msg=f"Created '{name}'.", kind="ok")
    except UserError as e:
        return back("/tournaments", msg=str(e), kind="err")
    except sqlite3.IntegrityError:
        return back("/tournaments", msg="A tournament with that name already exists.", kind="err")


def post_delete_tournament(conn, f):
    view = "archived" if f.get("view") == "archived" else None
    tid = positive_or(f.get("id"), 0)
    row = conn.execute(
        """SELECT t.name, (SELECT COUNT(*) FROM results r WHERE r.tournament_id = t.id) AS matches
           FROM tournaments t WHERE t.id = ?""", (tid,)).fetchone()
    if not row:
        return back("/tournaments", view=view, msg="That tournament no longer exists.", kind="err")
    conn.execute("DELETE FROM tournaments WHERE id = ?", (tid,))  # results go with it
    conn.commit()
    return back("/tournaments", view=view, kind="ok",
                msg=f"Deleted '{row['name']}' and its {row['matches']} recorded match(es).")


def set_archived(conn, f, archived):
    tid = positive_or(f.get("id"), 0)
    row = conn.execute("SELECT name FROM tournaments WHERE id = ?", (tid,)).fetchone()
    view = None if archived else "archived"  # stay on the same tab
    if not row:
        return back("/tournaments", view=view, msg="That tournament no longer exists.", kind="err")
    conn.execute("UPDATE tournaments SET archived = ? WHERE id = ?", (1 if archived else 0, tid))
    conn.commit()
    msg = (f"Archived '{row['name']}'. You can find it under Archived." if archived
           else f"Restored '{row['name']}'. It's active again.")
    return back("/tournaments", view=view, msg=msg, kind="ok")


def post_archive_tournament(conn, f):
    return set_archived(conn, f, True)


def post_restore_tournament(conn, f):
    return set_archived(conn, f, False)


POST_ROUTES = {"/record/save": post_save_result, "/record/delete": post_delete_result,
               "/players/add": post_add_player, "/players/remove": post_remove_player,
               "/tournaments/create": post_create_tournament,
               "/tournaments/delete": post_delete_tournament,
               "/tournaments/archive": post_archive_tournament,
               "/tournaments/restore": post_restore_tournament}
