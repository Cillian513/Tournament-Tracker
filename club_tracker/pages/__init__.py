"""One module per page. PAGES maps the url name to the function that builds it."""
from .leaderboard import page_leaderboard
from .players import page_players
from .record import page_record
from .tournaments import page_tournaments

PAGES = {"record": page_record, "leaderboard": page_leaderboard,
         "players": page_players, "tournaments": page_tournaments}