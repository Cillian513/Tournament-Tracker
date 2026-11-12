# Club Tournament Tracker

A small program for running tournaments at a local club. It keeps track of
players, records results week by week, works out the league table, and draws
knockout brackets.

It opens in your web browser, but everything runs on your own computer. Nothing
is uploaded anywhere and no internet connection is needed.

## What it does

- **Leagues** - record matches week by week and get a points table. You choose
  the points for a win, draw and loss when you create the league.
- **Knockout brackets** - single elimination. Pick the players and the bracket
  is drawn for you, with byes handed out automatically if the numbers don't
  fit. Type each score into the diagram and the winner moves on by itself.
- **Leaderboard** - the table after any week, so you can see how the standings
  looked earlier in the season. A trophy sits beside first place.
- **Archive** - tuck finished tournaments away without losing their results.
- **CSV export** - save a league's results to open in Excel or share.
- **Players** - one list of everyone in the club, shared by every tournament.

## What you need

Python 3.8 or newer. That's all - there is nothing to install.

## Getting started

1. Put the files in one folder, laid out as shown below.
2. Open a terminal in that folder.
3. Run:

   ```
   python3 club_tracker_window.py
   ```

   (On Windows it's usually `python club_tracker_window.py`.)

4. Your browser opens on the tracker. If it doesn't, go to
   http://127.0.0.1:8765 yourself.
5. When you're finished, click **Quit** at the bottom of the sidebar, or press
   Ctrl+C in the terminal. Your data is saved after every change, so closing
   the browser tab on its own loses nothing.


## Using it

### Players

Add everyone on the **Players** page. You can also just type a new name when
recording a result or creating a bracket and they're added automatically. A
player can only be removed if they haven't played in anything.

### Leagues

1. On **Tournaments**, create a league and set the points for a win, draw and
   loss.
2. On **Record Results**, pick the league and a week, then enter each match:
   player 1, their score, player 2, their score. Use the week buttons to move
   between weeks, and **+ New week** to start the next one.
3. Check the **Leaderboard**. Change "standings after week" to see the table at
   any earlier point. Ties on points are split by score difference, then by
   total scored.

Made a mistake? Press **Delete** beside the result in that week's list and
enter it again.

### Knockout brackets

1. On **Tournaments**, open **New knockout bracket**.
2. Give it a name, tick the players, and add any new names (one per line).
3. Choose **Random draw**, or **Seed in listed order** if you want to decide the
   seeding yourself. In listed order, ticked players go A to Z and then new
   names as you typed them, best seed first.
4. Press **Create bracket**. You land on the **Bracket** page.

On the bracket page:

- Each match with both players known has two score boxes. Type the scores and
  press **Save** - the winner moves into the next round automatically.
- A match can't end level. Someone has to win.
- If the number of players isn't 2, 4, 8, 16, 32 or 64, the top seeds get a bye
  (they go straight through round one).
- Made a typo? You can re-enter a score, or press **Clear result**, as long as
  the next round hasn't been played yet. Once it has, clear that later result
  first.
- **Redraw bracket** reshuffles everything, but only while nobody has played.
- When the final is decided, the champion appears at the top with the trophy.

A bracket takes between 2 and 64 players.

### Archiving and deleting

On **Tournaments** there are Active and Archived tabs.

- **Archive** moves a finished tournament out of the way. Its results are kept
  and you can **Restore** it whenever you like. Archived leagues disappear from
  Record Results but still show on the Leaderboard. Archived brackets are
  read-only.
- **Delete** removes the tournament and all its results for good. It asks first.
  Players are never deleted this way.
