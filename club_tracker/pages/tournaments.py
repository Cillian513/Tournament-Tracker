"""Tournaments page, with the Active / Archived tabs."""
from ..helpers import esc
from ..templates import token_field


def page_tournaments(conn, q):
    view = "archived" if q.get("view") == "archived" else "active"
    counts = {r["archived"]: r["n"] for r in conn.execute(
        "SELECT archived, COUNT(*) AS n FROM tournaments GROUP BY archived")}
    tabs = ('<div class="chips" style="margin:0 0 14px">'
            f'<a class="chip{" on" if view == "active" else ""}" href="/tournaments">Active ({counts.get(0, 0)})</a>'
            f'<a class="chip{" on" if view == "archived" else ""}" href="/tournaments?view=archived">'
            f'Archived ({counts.get(1, 0)})</a></div>')
    form = f"""<div class="card"><h2>New tournament</h2>
<form class="row" method="post" action="/tournaments/create">{token_field()}
<label>Name<input name="name" placeholder="e.g. Autumn League 2026" required autocomplete="off"></label>
<label class="score">Win pts<input type="number" name="win" min="0" value="3" required></label>
<label class="score">Draw pts<input type="number" name="draw" min="0" value="1" required></label>
<label class="score">Loss pts<input type="number" name="loss" min="0" value="0" required></label>
<button class="btn" type="submit">Create tournament</button></form></div>"""
    rows = conn.execute(
        """SELECT t.id, t.name, t.win_pts, t.draw_pts, t.loss_pts, COUNT(r.id) AS matches,
                  COALESCE(MAX(r.week_no), 0) AS weeks
           FROM tournaments t LEFT JOIN results r ON r.tournament_id = t.id
           WHERE t.archived = ? GROUP BY t.id ORDER BY t.id""",
        (1 if view == "archived" else 0,)).fetchall()
    if rows:
        body = ""
        for r in rows:
            if view == "active":
                toggle = (f'<form class="inline" method="post" action="/tournaments/archive">{token_field()}'
                          f'<input type="hidden" name="id" value="{r["id"]}">'
                          f'<button class="btn alt" type="submit">Archive</button></form>')
            else:
                toggle = (f'<form class="inline" method="post" action="/tournaments/restore">{token_field()}'
                          f'<input type="hidden" name="id" value="{r["id"]}">'
                          f'<button class="btn alt" type="submit">Restore</button></form>')
            delete = (f'<form class="inline" method="post" action="/tournaments/delete" '
                      f'data-name="{esc(r["name"])}" data-matches="{r["matches"]}" '
                      f'onsubmit="return confirm(\'Delete \' + this.dataset.name + \' and its \' + this.dataset.matches + '
                      f'\' recorded matches? This cannot be undone.\')">{token_field()}'
                      f'<input type="hidden" name="id" value="{r["id"]}">'
                      f'<input type="hidden" name="view" value="{view}">'
                      f'<button class="btn danger" type="submit">Delete</button></form>')
            body += (f'<tr><td>{esc(r["name"])}</td>'
                     f'<td class="c">{r["win_pts"]} / {r["draw_pts"]} / {r["loss_pts"]}</td>'
                     f'<td class="c">{r["matches"]}</td><td class="c">{r["weeks"]}</td>'
                     f'<td class="c"><div class="actions">{toggle}{delete}</div></td></tr>')
        if view == "active":
            hint = ("Archive a finished tournament to tidy it away. Its results are kept and you can restore it "
                    "any time. Deleting removes its results for good.")
        else:
            hint = ("Archived tournaments are hidden from Record Results but still appear on the Leaderboard. "
                    "Restore one to add more results.")
        listing = (f'<div class="wrap"><table><thead><tr><th>Name</th><th class="c">Win / Draw / Loss</th>'
                   f'<th class="c">Matches</th><th class="c">Weeks played</th><th class="c"></th></tr></thead>'
                   f'<tbody>{body}</tbody></table></div><p class="hint">{hint}</p>')
    else:
        listing = ('<p class="empty">No active tournaments - create one above.</p>' if view == "active"
                   else '<p class="empty">Nothing archived yet.</p>')
    return ("Tournaments", "Create a league, then archive it when the season is over.",
            tabs + form + f'<div class="card">{listing}</div>')
