"""Works out the league table from the results."""


def calculate_standings(conn, tournament, up_to_week=None):
    query, params = "SELECT * FROM results WHERE tournament_id = ?", [tournament["id"]]
    if up_to_week is not None:
        query += " AND week_no <= ?"
        params.append(up_to_week)
    names = {r["id"]: r["name"] for r in conn.execute("SELECT id, name FROM players")}
    stats = {}
    for r in conn.execute(query, params):
        for pid, mine, theirs in ((r["player1_id"], r["score1"], r["score2"]),
                                  (r["player2_id"], r["score2"], r["score1"])):
            s = stats.setdefault(pid, {"name": names[pid], "P": 0, "W": 0, "D": 0,
                                       "L": 0, "F": 0, "A": 0, "Pts": 0})
            s["P"] += 1
            s["F"] += mine
            s["A"] += theirs
            if mine > theirs:
                s["W"] += 1
                s["Pts"] += tournament["win_pts"]
            elif mine == theirs:
                s["D"] += 1
                s["Pts"] += tournament["draw_pts"]
            else:
                s["L"] += 1
                s["Pts"] += tournament["loss_pts"]
    return sorted(stats.values(),
                  key=lambda s: (-s["Pts"], -(s["F"] - s["A"]), -s["F"], s["name"].lower()))
