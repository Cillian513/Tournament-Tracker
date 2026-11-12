"""Leaderboard page."""
from ..database import choose_tournament, get_tournaments
from ..helpers import back, esc, name_html, positive_or
from ..standings import calculate_standings
from ..templates import no_tournament_card, tournament_options


def page_leaderboard(conn, q):
    tournaments = get_tournaments(conn)
    if not tournaments:
        return "Leaderboard", "Dare to be the best", no_tournament_card()
    t = choose_tournament(tournaments, q.get("t"))
    max_week = conn.execute("SELECT MAX(week_no) AS w FROM results WHERE tournament_id = ?",
                            (t["id"],)).fetchone()["w"] or 1
    week = positive_or(q.get("w"), max_week)

    controls = f"""<div class="card"><form class="inline row" method="get" action="/leaderboard">
<label>Tournament<select name="t" onchange="this.form.submit()">
{tournament_options(tournaments, t["id"])}</select></label>
<label>Standings after week<input type="number" name="w" min="1" value="{week}" style="width:90px"></label>
<button class="btn" type="submit">Show</button>
<a class="btn" style="margin-left:auto" href="{esc(back('/export', t=t['id']))}">Export results to CSV</a>
</form></div>"""

    table = calculate_standings(conn, t, week)
    if table:
        medal = {1: ("gold", "1st" '<img class="trophy" src="trophy" alt="Trophy">'), 2: ("silver", "2nd"), 3: ("bronze", "3rd")}
        rows = ""
        for i, s in enumerate(table, 1):
            cls, label = medal.get(i, ("", str(i)))
            diff = s["F"] - s["A"]
            dcls = "pos" if diff > 0 and i > 3 else "neg" if diff < 0 and i > 3 else ""
            rows += (f'<tr class="{cls}"><td class="c">{label}</td><td>{name_html(s["name"])}</td>'
                     f'<td class="c">{s["P"]}</td><td class="c">{s["W"]}</td><td class="c">{s["D"]}</td>'
                     f'<td class="c">{s["L"]}</td><td class="c">{s["F"]}</td><td class="c">{s["A"]}</td>'
                     f'<td class="c {dcls}">{diff:+d}</td><td class="c">{s["Pts"]}</td></tr>')
        board = f"""<div class="wrap"><table><thead><tr><th class="c">Position</th><th>Player</th>
<th class="c">Played</th><th class="c">Wins</th><th class="c">Draws</th><th class="c">Losses</th><th class="c">For</th>
<th class="c">Against</th><th class="c">Difference</th><th class="c">Points</th></tr></thead><tbody>{rows}</tbody></table></div>"""
    else:
        board = '<p class="empty">No results recorded for this tournament yet.</p>'
    badge = ' <span class="badge">Archived</span>' if t["archived"] else ""
    card = f'<div class="card"><h2>{esc(t["name"])} &ndash; after week {week}{badge}</h2>{board}</div>'
    return "Leaderboard", "Gold, silver and bronze mark the top three.", controls + card
