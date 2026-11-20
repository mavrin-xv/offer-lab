#!/usr/bin/env python3
"""Count which claims every competitor already makes, so you can see where a new claim still has room.

Each competitor gets one markdown file (copy templates/competitor-pack.md). Under "## Claims" and
"## Complaints", one item per line, each starting with a short theme tag in square brackets:

  ## Claims
  - [auto-sync] Stock syncs across every channel automatically (source: homepage hero)
  ## Complaints
  - [support] "Took 9 days to answer a ticket" (source: app store review, 2 stars)

Your own candidate claims go in one more file with a "## Candidate claims" section in the same format.

Triage per theme (number of competitors that claim it):
  3 or more   SATURATED    do not lead with it; it is table stakes at best
  1 to 2      CONTESTED    lead only with proof the others cannot show
  0           WHITE SPACE  open, but check it matters to the buyer before you lead with it
Complaint themes are listed separately: a theme rivals claim but buyers complain about is a gap you can prove.
Claims without "(source: ...)" are flagged: a competitor pack without sources is a guess.

Usage:
  python claim_triage.py examples/data/competitors/ --ours examples/data/our-claims.md
  python claim_triage.py packs/*.md --format json

Exit codes: 0 ok, 2 bad input (no files, no claims found).
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ITEM = re.compile(r"^\s*[-*]\s*\[([a-z0-9 _-]+)\]\s*(.+)$", re.I)


def sections(text):
    cur, out = None, defaultdict(list)
    for line in text.splitlines():
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            cur = h.group(1).strip().lower()
            continue
        m = ITEM.match(line)
        if m and cur:
            out[cur].append((m.group(1).strip().lower().replace(" ", "-"), m.group(2).strip()))
    return out


def name_of(path, text):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).replace("Competitor:", "").strip() if m else path.stem


def plural(n):
    return "rival" if n == 1 else "rivals"


def status(n):
    return "SATURATED" if n >= 3 else "CONTESTED" if n >= 1 else "WHITE SPACE"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="competitor pack files or a folder of them")
    ap.add_argument("--ours", help="file with a '## Candidate claims' section")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args()

    files = []
    for p in map(Path, a.paths):
        files += sorted(p.glob("*.md")) if p.is_dir() else [p]
    files = [f for f in files if not a.ours or f.resolve() != Path(a.ours).resolve()]
    if not files:
        print("no competitor files found", file=sys.stderr)
        sys.exit(2)
    missing = [str(f) for f in files + ([Path(a.ours)] if a.ours else []) if not f.is_file()]
    if missing:
        print("file not found: " + ", ".join(missing), file=sys.stderr)
        sys.exit(2)

    claims, complaints, unsourced = defaultdict(set), defaultdict(set), []
    examples = {}
    for f in files:
        t = f.read_text(encoding="utf-8")
        who = name_of(f, t)
        s = sections(t)
        for tag, line in s.get("claims", []):
            claims[tag].add(who)
            examples.setdefault(tag, line)
            if "source:" not in line.lower():
                unsourced.append(f"{who}: [{tag}] {line}")
        for tag, line in s.get("complaints", []):
            complaints[tag].add(who)
    if not claims:
        print("no '## Claims' items with [tag] found; see --help for the format", file=sys.stderr)
        sys.exit(2)

    ours = []
    if a.ours:
        for tag, line in sections(Path(a.ours).read_text(encoding="utf-8")).get("candidate claims", []):
            n = len(claims.get(tag, ()))
            gap = tag in complaints
            ours.append({"tag": tag, "claim": line, "competitors": n, "status": status(n),
                         "rivals_get_complaints": sorted(complaints.get(tag, ())) if gap else []})

    themes = [{"tag": t, "competitors": len(w), "who": sorted(w), "status": status(len(w))}
              for t, w in claims.items()]
    themes.sort(key=lambda x: (-x["competitors"], x["tag"]))
    result = {"competitors": len(files), "themes": themes, "ours": ours,
              "complaint_themes": {t: sorted(w) for t, w in complaints.items()}, "unsourced": unsourced}
    if a.format == "json":
        print(json.dumps(result, indent=2))
        return

    print(f"{len(files)} competitor packs.\n")
    print("| Theme | Rivals claiming | Status | Example |")
    print("|---|---|---|---|")
    for x in themes:
        ex = re.sub(r"\s*\(source:.*?\)\s*$", "", examples[x["tag"]])
        print(f"| {x['tag']} | {x['competitors']} | {x['status']} | {ex[:60]} |")
    if complaints:
        print("\nWhat buyers complain about:")
        for t, w in sorted(complaints.items(), key=lambda kv: -len(kv[1])):
            claimed = f", yet {len(claims[t])} {plural(len(claims[t]))} claim it" if t in claims else ""
            print(f"- [{t}] at {len(w)} {plural(len(w))}{claimed}")
    if ours:
        print("\nYour candidate claims:")
        for o in ours:
            gap = f"; rivals get complaints here ({', '.join(o['rivals_get_complaints'])}), prove it" if o["rivals_get_complaints"] else ""
            print(f"- {o['status']:<11} [{o['tag']}] {o['claim']}  ({o['competitors']} {plural(o['competitors'])}){gap}")
    if unsourced:
        print("\nClaims with no source (go back and capture where you saw it):")
        for u in unsourced:
            print(f"- {u}")


if __name__ == "__main__":
    main()
