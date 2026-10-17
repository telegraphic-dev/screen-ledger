---
name: Screen ledger
description: >-
  Use before you dispatch a computerUse subagent or open the box browser, when a
  browser or desktop screen reports 'in use', and when someone asks who is using
  which screen on the shared computer. Records which agent holds a screen and
  shows what is running on every screen.
---
# Screen ledger

The box has several desktop screens (X displays), shared by every agent. Nothing records who holds which one, so this skill adds a small shared log plus a live view. The script lives at `/home/box/tools/screen-ledger.py` and the log at `/home/box/tools/screen-ledger.jsonl`. Both are on the shared filesystem, so every agent sees the same data.

## When you take or finish a screen
1. Before dispatching browser or desktop work, claim a screen with your agent name and a short note about the task:
   `python3 /home/box/tools/screen-ledger.py claim <your agent name> --note "what you are doing"`
   Add `--display N` once you know which screen number your session uses.
2. When the work is done, or the user hands the screen back, release it, and close the browser window if you opened one:
   `python3 /home/box/tools/screen-ledger.py release <your agent name> --note "done"`
3. If a task fails or is cancelled, release anyway. A claim you forget to release is the main reason a screen looks taken.

## When a screen looks busy, or someone asks who has what
1. Run `python3 /home/box/tools/screen-ledger.py status`.
2. The live view is the ground truth: for each screen it shows how long it has been up, whether it is free or has windows open, how long Chrome has been running, and the window titles.
3. A Chrome older than two hours with no ledger claim is flagged as possibly left over. Window titles usually show whose work it is (for example a Cloudflare page or an a2a.exposed dashboard).
4. `python3 /home/box/tools/screen-ledger.py log 20` shows the latest claims and releases, so you can see who held a screen last.

## Rules
- Only close a browser or session that you opened yourself. For one that looks left over, ask the owning agent through SendToAgent, or ask the user.
- Do not drive screens with input automation such as xdotool. The script only lists window names.
- The ledger holds only what agents report. If it disagrees with the live view, trust the live view.
- Gotcha: a screen with no windows can still be assigned to an agent, so a free-looking screen is not proof that a session cannot claim it.
