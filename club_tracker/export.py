"""CSV export."""
import csv
import io

from .database import choose_tournament, get_tournaments


def export_csv(conn, q):
    rows = get_tournaments(conn)
    if not rows:
        return None, b""
    t = choose_tournament(rows, q.get("t"))
    data = conn.execute(
        """SELECT r.week_no, r.played_on, a.name AS p1, r.score1, r.score2, b.name AS p2
           FROM results r JOIN players a ON a.id = r.player1_id JOIN players b ON b.id = r.player2_id
           WHERE r.tournament_id = ? ORDER BY r.week_no, r.id""", (t["id"],)).fetchall()
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Week", "Date", "Player 1", "Score 1", "Score 2", "Player 2"])
    w.writerows([tuple(r) for r in data])
    safe = "".join(c if c.isalnum() else "_" for c in t["name"])
    return f"{safe}_results.csv", out.getvalue().encode("utf-8-sig")  # so excel reads it properly
