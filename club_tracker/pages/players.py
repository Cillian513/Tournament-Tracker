"""Players page."""
from ..helpers import name_html
from ..templates import token_field


def page_players(conn, q):
    add = f"""<div class="card"><h2>Add a player</h2>
<form class="row" method="post" action="/players/add">{token_field()}
<label>Name<input name="name" required autofocus autocomplete="off"></label>
<button class="btn" type="submit">Add player</button></form></div>"""
    rows = conn.execute(
        """SELECT p.id, p.name,
                  (SELECT COUNT(*) FROM results r WHERE r.player1_id = p.id OR r.player2_id = p.id) AS matches
           FROM players p ORDER BY p.name""").fetchall()
    if rows:
        body = ""
        for r in rows:
            remove = (f'<form class="inline" method="post" action="/players/remove" '
                      f'onsubmit="return confirm(\'Remove this player?\')">{token_field()}'
                      f'<input type="hidden" name="id" value="{r["id"]}">'
                      f'<button class="btn danger" type="submit">Remove</button></form>'
                      if r["matches"] == 0 else "")
            body += (f'<tr><td>{name_html(r["name"])}</td><td class="c">{r["matches"]}</td>'
                     f'<td class="c">{remove}</td></tr>')
        listing = (f'<div class="wrap"><table><thead><tr><th>Name</th><th class="c">Matches played</th>'
                   f'<th class="c"></th></tr></thead><tbody>{body}</tbody></table></div>')
    else:
        listing = '<p class="empty">No players yet.</p>'
    return "Players", "Everyone in the club.", add + f'<div class="card">{listing}</div>'
