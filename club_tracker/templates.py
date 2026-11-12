"""The page frame (sidebar, flash message) and shared form bits."""
from .config import CLUB_NAME, LOGO_PATH, TOKEN
from .helpers import esc, name_html
from .styles import CSS


NAV = [("record", "Record Results"), ("leaderboard", "Leaderboard"),
       ("players", "Players"), ("tournaments", "Tournaments")]


def token_field():
    return f'<input type="hidden" name="token" value="{TOKEN}">'


def options(items, selected):
    return "".join(
        f'<option value="{esc(v)}"{" selected" if str(v) == str(selected) else ""}>{esc(label)}</option>'
        for v, label in items)


def tournament_options(rows, selected):
    def opts(items):
        return "".join(f'<option value="{r["id"]}"{" selected" if str(r["id"]) == str(selected) else ""}>'
                       f'{esc(r["name"])}</option>' for r in items)
    active = [r for r in rows if not r["archived"]]
    archived = [r for r in rows if r["archived"]]
    if not archived:
        return opts(active)
    out = f'<optgroup label="Active">{opts(active)}</optgroup>' if active else ""
    return out + f'<optgroup label="Archived">{opts(archived)}</optgroup>'


def layout(active, title, subtitle, body, msg=None, kind="ok"):
    nav = "".join(f'<a class="{"active" if key == active else ""}" href="/{key}">{label}</a>'
                  for key, label in NAV)
    flash = f'<div class="flash {kind}">{name_html(msg)}</div>' if msg else ""
    has_logo = LOGO_PATH.exists()
    logo = '<img class="logo" src="/logo" alt="">' if has_logo else ""
    favicon = '<link rel="icon" href="/logo">' if has_logo else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{favicon}<title>{esc(title)} - {esc(CLUB_NAME)}</title><style>{CSS}</style></head>
<body>
<nav><div class="head">{logo}<div class="brand">{esc(CLUB_NAME)}</div></div>{nav}<div class="spacer"></div>
<form method="post" action="/quit" onsubmit="return confirm('Stop the tracker? Your data is saved.')">
{token_field()}<button type="submit">Quit</button></form></nav>
<main><h1>{esc(title)}</h1><p class="sub">{esc(subtitle)}</p>{flash}{body}</main>
</body></html>"""


def no_tournament_card(conn=None):
    archived = conn.execute("SELECT COUNT(*) FROM tournaments WHERE archived = 1").fetchone()[0] if conn else 0
    if archived:
        return ('<div class="card"><p class="empty">No active tournaments right now.</p>'
                '<a class="btn" href="/tournaments">Create a new tournament</a> '
                '<a class="btn alt" href="/tournaments?view=archived">View archived tournaments</a></div>')
    return ('<div class="card"><p class="empty">No tournaments yet.</p>'
            '<a class="btn" href="/tournaments">Create your first tournament</a></div>')
