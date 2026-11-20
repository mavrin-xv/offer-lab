#!/usr/bin/env python3
"""Find the traits that separate won deals from lost ones, then test the profile on held-out deals.

Method:
  1. Hold out the last N won and last N lost deals (default 5 + 5). They are not used to build the profile.
  2. On the rest, count how often each trait appears in won and in lost deals.
  3. Keep a trait as "fit" when it is at least --ratio times (default 2) more common in won deals
     and appears in at least --min-share (default 30%) of won deals.
  4. Mark a trait as a "disqualifier" when it is at least --ratio times more common in lost deals,
     appears in at least --min-share of lost deals and in under --min-share of won deals.
     Keep the strongest --max-dq (default 5): a long list of disqualifiers rejects good buyers.
  5. Score each held-out deal: predicted won when it has at least half of the fit traits and no disqualifier.
     Print the hit rate. If the profile does no better than guessing on the holdout, do not use it.

Input: CSV with columns deal, outcome (won or lost), traits (separated by ; ). Rows in time order, oldest first.
You want 10 or more won and 10 or more lost deals. With fewer, the script still runs and says so.

Usage:
  python icp_traits.py examples/data/deals.csv
  python icp_traits.py deals.csv --holdout 3 --ratio 1.5
  python icp_traits.py deals.csv --format json

Exit codes: 0 ok, 2 bad input.
"""
import argparse
import csv
import json
import sys
from collections import Counter


def load(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            o = (r.get("outcome") or "").strip().lower()
            if o not in ("won", "lost"):
                raise ValueError(f"line {n}: outcome must be won or lost, got {o!r}")
            traits = {t.strip().lower() for t in (r.get("traits") or "").split(";") if t.strip()}
            rows.append({"deal": (r.get("deal") or f"row{n}").strip(), "won": o == "won", "traits": traits})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="CSV of deals: deal, outcome, traits")
    ap.add_argument("--holdout", type=int, default=5, help="won and lost deals to hold out each (default 5)")
    ap.add_argument("--ratio", type=float, default=2.0, help="how many times more common a trait must be (default 2)")
    ap.add_argument("--min-share", type=float, default=0.3, help="minimum share within its group (default 0.3)")
    ap.add_argument("--max-dq", type=int, default=5, help="keep at most this many disqualifiers (default 5)")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args()

    try:
        rows = load(a.file)
    except (ValueError, OSError) as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    won = [r for r in rows if r["won"]]
    lost = [r for r in rows if not r["won"]]
    notes = []
    if len(won) < 10 or len(lost) < 10:
        notes.append(f"only {len(won)} won and {len(lost)} lost deals; 10 + 10 is the floor for a usable profile")
    h = a.holdout if len(won) > a.holdout and len(lost) > a.holdout else 0
    if h == 0 and a.holdout:
        notes.append("too few deals to hold any out; the profile is untested")
    train_w, test_w = (won[:-h], won[-h:]) if h else (won, [])
    train_l, test_l = (lost[:-h], lost[-h:]) if h else (lost, [])

    cw = Counter(t for r in train_w for t in r["traits"])
    cl = Counter(t for r in train_l for t in r["traits"])
    nw, nl = max(len(train_w), 1), max(len(train_l), 1)
    table, fit, dq = [], [], []
    for t in sorted(set(cw) | set(cl)):
        sw, sl = cw[t] / nw, cl[t] / nl
        ratio_w = sw / sl if sl else float("inf")
        ratio_l = sl / sw if sw else float("inf")
        kind = ""
        if ratio_w >= a.ratio and sw >= a.min_share:
            kind = "fit"
            fit.append(t)
        elif ratio_l >= a.ratio and sl >= a.min_share and sw < a.min_share:
            kind = "disqualifier"
            dq.append((ratio_l, sl, t))
        table.append({"trait": t, "won_share": round(sw, 2), "lost_share": round(sl, 2), "kind": kind})
    dq = [t for _, _, t in sorted(dq, reverse=True)[:a.max_dq]]
    for x in table:
        if x["kind"] == "disqualifier" and x["trait"] not in dq:
            x["kind"] = ""

    def predict(r):
        need = max(1, (len(fit) + 1) // 2)
        return len(r["traits"] & set(fit)) >= need and not (r["traits"] & set(dq))

    test = [(r, predict(r)) for r in test_w + test_l]
    hits = sum(1 for r, p in test if p == r["won"])
    result = {
        "deals": {"won": len(won), "lost": len(lost), "held_out": len(test)},
        "fit_traits": fit, "disqualifiers": dq, "traits": table,
        "holdout": [{"deal": r["deal"], "actual": "won" if r["won"] else "lost",
                     "predicted": "won" if p else "lost"} for r, p in test],
        "holdout_hit_rate": round(hits / len(test), 2) if test else None,
        "notes": notes,
    }
    if a.format == "json":
        print(json.dumps(result, indent=2))
        return

    print(f"Deals: {len(won)} won, {len(lost)} lost. Profile built on {len(train_w)} + {len(train_l)}, "
          f"tested on {len(test)} held out.\n")
    print("| Trait | In won | In lost | Kind |")
    print("|---|---|---|---|")
    for x in sorted(table, key=lambda x: (x["kind"] == "", -abs(x["won_share"] - x["lost_share"]))):
        print(f"| {x['trait']} | {x['won_share']:.0%} | {x['lost_share']:.0%} | {x['kind']} |")
    print(f"\nFit traits: {', '.join(fit) or 'none'}")
    print(f"Disqualifiers: {', '.join(dq) or 'none'}")
    if test:
        print(f"\nHoldout: {hits}/{len(test)} predicted right ({hits / len(test):.0%}).")
        for r, p in test:
            mark = "ok  " if p == r["won"] else "MISS"
            print(f"  {mark} {r['deal']}: actual {'won' if r['won'] else 'lost'}, predicted {'won' if p else 'lost'}")
        if hits / len(test) <= 0.6:
            print("Profile does not beat a coin flip by much on the holdout. Collect more deals before using it.")
    for n in notes:
        print(f"NOTE: {n}")


if __name__ == "__main__":
    main()
