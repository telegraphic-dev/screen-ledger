#!/usr/bin/env python3
"""Shared screen ledger for the box desktops.

Usage:
  screen-ledger.py status                         live view of every screen plus open claims
  screen-ledger.py claim <agent> [--display N] [--note TEXT]
  screen-ledger.py release <agent> [--note TEXT]
  screen-ledger.py log [N]                        last N ledger events (default 20)
"""
import json, os, re, subprocess, sys, time, glob

LEDGER = "/home/box/tools/screen-ledger.jsonl"
STALE_HOURS = 2

def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return ""

def read_ledger():
    rows = []
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            line = line.strip()
            if line:
                try: rows.append(json.loads(line))
                except Exception: pass
    return rows

def append(ev):
    ev["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(LEDGER, "a") as f:
        f.write(json.dumps(ev) + "\n")

def open_claims(rows):
    claims = {}
    for r in rows:
        if r["event"] == "claim":
            claims[r["agent"]] = r
        elif r["event"] == "release":
            claims.pop(r["agent"], None)
    return claims

def displays():
    out = []
    for line in sh("ps -eo pid,etimes,args --no-headers").splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)\s+Xvfb :(\d+) ", line)
        if m: out.append((int(m.group(3)), int(m.group(2))))
    return sorted(out)

def windows(n):
    names = []
    for w in sh(f"DISPLAY=:{n} xdotool search --onlyvisible --name . 2>/dev/null").split():
        t = sh(f"DISPLAY=:{n} xdotool getwindowname {w} 2>/dev/null").strip()
        if t and t not in ("Xfwm4", "plank") and t not in names:
            names.append(t)
    return names

def chrome_age(n):
    best = None
    for line in sh("ps -eo etimes,args --no-headers").splitlines():
        m = re.match(r"\s*(\d+)\s+(.*)", line)
        if not m: continue
        age, args = int(m.group(1)), m.group(2)
        if f"DISPLAY=:{n} " in args and "chrome" in args and "box-bounded-log" in args:
            best = age if best is None else max(best, age)
    return best

def hm(sec):
    return f"{sec//3600}h{(sec%3600)//60:02d}m"

def status():
    rows = read_ledger()
    claims = open_claims(rows)
    by_display = {}
    for c in claims.values():
        if c.get("display") is not None:
            by_display.setdefault(str(c["display"]), []).append(c)
    print(f"Screens on the box ({time.strftime('%Y-%m-%d %H:%M %Z')}):")
    for n, up in displays():
        wins = windows(n)
        age = chrome_age(n)
        state = "FREE" if not wins else "HAS WINDOWS"
        print(f"\n:{n}  up {hm(up)}  {state}")
        if age is not None:
            flag = ""
            if age > STALE_HOURS*3600 and str(n) not in by_display:
                flag = "  <- Chrome older than %dh with no ledger claim: possibly left over" % STALE_HOURS
            print(f"   Chrome running {hm(age)}{flag}")
        for t in wins: print(f"   window: {t}")
        for c in by_display.get(str(n), []):
            print(f"   claimed by {c['agent']} since {c['ts']} {('- ' + c['note']) if c.get('note') else ''}")
    others = [c for c in claims.values() if c.get("display") is None]
    if others:
        print("\nOpen claims without a screen number:")
        for c in others:
            print(f"   {c['agent']} since {c['ts']} {('- ' + c['note']) if c.get('note') else ''}")
    print("\nNote: the ledger only knows what agents report. The live view above is ground truth.")

def main():
    a = sys.argv[1:]
    if not a or a[0] == "status": return status()
    if a[0] in ("claim", "release") and len(a) >= 2:
        ev = {"event": a[0], "agent": a[1]}
        i = 2
        while i < len(a):
            if a[i] == "--display": ev["display"] = int(a[i+1]); i += 2
            elif a[i] == "--note": ev["note"] = a[i+1]; i += 2
            else: i += 1
        append(ev); print("ok", json.dumps(ev)); return
    if a[0] == "log":
        n = int(a[1]) if len(a) > 1 else 20
        for r in read_ledger()[-n:]: print(json.dumps(r))
        return
    print(__doc__)

main()
