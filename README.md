# Screen ledger

Screen ledger is a shared log and live view of who is using which desktop screen on a shared Grok Bot computer.

When several agents share one computer with a few virtual desktops (X displays), nothing says who holds which screen. Screen ledger gives each agent a way to claim and release a screen, and shows what is actually running on every screen.

## Commands

```
python3 scripts/screen-ledger.py claim <agent> [--display N] [--note TEXT]
python3 scripts/screen-ledger.py release <agent> [--note TEXT]
python3 scripts/screen-ledger.py status
```

`status` lists every screen with its uptime, open windows, Chrome age and any claim. `log [N]` prints the last N claims and releases.

The log file is `/home/box/tools/screen-ledger.jsonl`. Set the `SCREEN_LEDGER_FILE` environment variable to use another path.

## Requirements

Linux with Xvfb screens, `python3` and `xdotool`.

## Install

This repository is an [Agent Plugins](https://agent-plugins.org) 1.0.0 plugin. Install it from a marketplace that lists it, or copy it by hand:

- **Whole plugin:** copy this repository into your agent's plugins folder.
- **Skill only:** copy `skills/screen-ledger/` (the `SKILL.md` and the `scripts/` folder) into your agent's skills folder, or paste `SKILL.md` into the Grok Bot skill editor and copy `scripts/screen-ledger.py` to a path the agents can run.

## License

[MIT](LICENSE)
