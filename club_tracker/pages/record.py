"""Record Results page."""
from datetime import date

from ..database import choose_tournament, get_tournaments, player_names
from ..helpers import back, esc, name_html, positive_or
from ..templates import no_tournament_card, options, token_field


def page_record(conn, q):
    tournaments = get_tournaments(conn, archived=False)
    if not tournaments:
        return "Record Results", "Enter each match from this week's session.", no_tournament_card(conn)
    t = choose_tournament(tournaments, q.get("t"))
    weeks = [r["week_no"] for r in conn.execute(
        "SELECT DISTINCT week_no FROM results WHERE tournament_id = ? ORDER BY week_no", (t["id"],))]
    week = positive_or(q.get("w"), weeks[-1] if weeks else 1)
    existing = conn.execute(
        "SELECT played_on FROM results WHERE tournament_id = ? AND week_no = ? LIMIT 1",
        (t["id"], week)).fetchone()
    played_on = q.get("d") or (existing["played_on"] if existing else date.today().isoformat())

    shown_weeks = sorted(set(weeks) | {week})
    chips = "".join(
        f'<a class="chip{" on" if w == week else ""}" href="{esc(back("/record", t=t["id"], w=w))}">Week {w}</a>'
        for w in shown_weeks)
    if week in weeks:
        chips += (f'<a class="chip" href="{esc(back("/record", t=t["id"], w=max(shown_weeks) + 1))}">'
                  "+ New week</a>")

    selector = f"""<div class="card">
<form class="inline row" method="get" action="/record">
<label>Tournament<select name="t" onchange="this.form.submit()">
{options([(r["id"], r["name"]) for r in tournaments], t["id"])}</select></label>
<noscript><button class="btn" type="submit">Show</button></noscript></form>
<div class="chips">{chips}</div></div>"""

    names = "".join(f'<option value="{esc(n)}">' for n in player_names(conn))
    entry = f"""<div class="card"><h2>New match &ndash; Week {week}</h2>
<form method="post" action="/record/save">{token_field()}
<input type="hidden" name="t" value="{t['id']}"><input type="hidden" name="w" value="{week}">
<div class="row" style="margin-bottom:12px">
<label>Date played<input type="date" name="d" value="{esc(played_on)}" required></label></div>
<div class="row">
<label>Player 1<input name="p1" list="players" value="{esc(q.get('p1', ''))}" autocomplete="off" required autofocus></label>
<label class="score">Score<input type="number" name="s1" min="0" value="{esc(q.get('s1', '0'))}" required></label>
<span class="dash">&ndash;</span>
<label class="score">Score<input type="number" name="s2" min="0" value="{esc(q.get('s2', '0'))}" required></label>
<label>Player 2<input name="p2" list="players" value="{esc(q.get('p2', ''))}" autocomplete="off" required></label>
<button class="btn" type="submit">Save result</button></div>
<datalist id="players">{names}</datalist>
<p class="hint">New name? Just type it and they'll be added as a player.</p>
</form></div>"""

    rows = conn.execute(
        """SELECT r.id, a.name AS p1, b.name AS p2, r.score1, r.score2
           FROM results r JOIN players a ON a.id = r.player1_id JOIN players b ON b.id = r.player2_id
           WHERE r.tournament_id = ? AND r.week_no = ? ORDER BY r.id""", (t["id"], week)).fetchall()
    if rows:
        body_rows = "".join(
            f"""<tr><td class="c">{r['id']}</td><td>{name_html(r['p1'])}</td>
<td class="c">{r['score1']} &ndash; {r['score2']}</td><td>{name_html(r['p2'])}</td>
<td class="c"><form class="inline" method="post" action="/record/delete"
 onsubmit="return confirm('Delete this result?')">{token_field()}
<input type="hidden" name="id" value="{r['id']}"><input type="hidden" name="t" value="{t['id']}">
<input type="hidden" name="w" value="{week}"><button class="btn danger" type="submit">Delete</button>
</form></td></tr>""" for r in rows)
        listing = f"""<div class="wrap"><table><thead><tr><th class="c">ID</th><th>Player 1</th>
<th class="c">Score</th><th>Player 2</th><th class="c"></th></tr></thead><tbody>{body_rows}</tbody></table></div>"""
    else:
        listing = '<p class="empty">No results recorded for this week yet.</p>'
    results = f'<div class="card"><h2>Week {week} results</h2>{listing}</div>'

    return "Record Results", "Enter each match from this week's session.", selector + entry + results
