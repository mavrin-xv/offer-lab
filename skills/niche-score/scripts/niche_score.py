#!/usr/bin/env python3
"""Score niche candidates on Money, Channel and Pain (1 to 5 each, 15 max) with evidence caps.

The three dimensions:
  money    people in this niche pay for this kind of fix today (current spend, not market size)
  channel  you can reach them through an exact query, list or community you can name
  pain     they name the problem themselves, in their own words, without prompting

Caps (applied before the total, printed so you can see why):
  channel  no channel_query (an exact search, list or group)      -> capped at 2
  pain     no pain_quote (their words, not yours)                 -> capped at 3
  pain     fewer than 3 named instances (people, posts, threads)  -> capped at 3
  money    no money_reason (what they pay now, and to whom)        -> capped at 2

Verdict on the capped total:
  11 to 15  SHIP     build the offer for this niche
   8 to 10  ITERATE  find the missing evidence, then rescore
   under 8  KILL     drop it, or narrow it and score again
A niche with any dimension at 1 is held at ITERATE at best, whatever the total (one dead leg sinks the offer).

Input: CSV with a header row. Columns:
  niche, money, money_reason, channel, channel_query, pain, pain_quote, instances

Usage:
  python niche_score.py examples/data/niches.csv
  python niche_score.py niches.csv --format json
  python niche_score.py --template > niches.csv

Exit codes: 0 ok, 2 bad input.
"""
import argparse
import csv
import json
import sys

SHIP_AT = 11      # this pack's defaults, not a published standard; change them and say why
ITERATE_AT = 8
COLS = ["niche", "money", "money_reason", "channel", "channel_query", "pain", "pain_quote", "instances"]


def verdict(total, low):
    v = "SHIP" if total >= SHIP_AT else "ITERATE" if total >= ITERATE_AT else "KILL"
    if v == "SHIP" and low:
        v = "ITERATE"
    return v


def score_row(r, n):
    out = {"niche": r["niche"].strip(), "caps": []}
    for d in ("money", "channel", "pain"):
        try:
            v = int(float(r[d]))
        except (TypeError, ValueError):
            raise ValueError(f"line {n}: {d}={r[d]!r} is not a number")
        if not 1 <= v <= 5:
            raise ValueError(f"line {n}: {d}={v} is outside 1..5")
        out[d] = v
    try:
        inst = int(float(r.get("instances") or 0))
    except ValueError:
        raise ValueError(f"line {n}: instances={r['instances']!r} is not a number")
    if not (r.get("channel_query") or "").strip() and out["channel"] > 2:
        out["caps"].append(f"channel {out['channel']}->2: no exact query or list")
        out["channel"] = 2
    if not (r.get("pain_quote") or "").strip() and out["pain"] > 3:
        out["caps"].append(f"pain {out['pain']}->3: no quote in their words")
        out["pain"] = 3
    if inst < 3 and out["pain"] > 3:
        out["caps"].append(f"pain {out['pain']}->3: {inst} named instance(s), need 3")
        out["pain"] = 3
    if not (r.get("money_reason") or "").strip() and out["money"] > 2:
        out["caps"].append(f"money {out['money']}->2: no current spend named")
        out["money"] = 2
    out["total"] = out["money"] + out["channel"] + out["pain"]
    low = [d for d in ("money", "channel", "pain") if out[d] == 1]
    out["verdict"] = verdict(out["total"], low)
    if low and out["total"] >= SHIP_AT:
        out["caps"].append(f"held at ITERATE: {', '.join(low)} = 1")
    out["channel_query"] = (r.get("channel_query") or "").strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="CSV of niche candidates")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--template", action="store_true", help="print the CSV header and one example row")
    a = ap.parse_args()

    if a.template:
        print(",".join(COLS))
        print('"Stock count cleanup for online shops with 200+ SKUs",4,"pay a bookkeeper 300/month to fix it",'
              '4,"forum search: inventory count wrong",5,"my stock numbers never match",6')
        return
    if not a.file:
        ap.error("give a CSV file or --template")

    rows = []
    try:
        with open(a.file, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            missing = [c for c in ("niche", "money", "channel", "pain") if c not in (reader.fieldnames or [])]
            if missing:
                print(f"missing column(s): {', '.join(missing)}", file=sys.stderr)
                sys.exit(2)
            for n, r in enumerate(reader, start=2):
                rows.append(score_row(r, n))
    except (ValueError, OSError) as e:
        print(e, file=sys.stderr)
        sys.exit(2)

    rows.sort(key=lambda x: (-x["total"], x["niche"]))
    if a.format == "json":
        print(json.dumps(rows, indent=2))
        return
    print("| # | Niche | M | C | P | Total | Verdict |")
    print("|---|---|---|---|---|---|---|")
    for i, x in enumerate(rows, 1):
        print(f"| {i} | {x['niche']} | {x['money']} | {x['channel']} | {x['pain']} | {x['total']}/15 | {x['verdict']} |")
    notes = [(x["niche"], c) for x in rows for c in x["caps"]]
    if notes:
        print("\nCaps applied:")
        for niche, c in notes:
            print(f"- {niche}: {c}")
    print(f"\nSHIP {SHIP_AT}+, ITERATE {ITERATE_AT}-{SHIP_AT - 1}, KILL under {ITERATE_AT}. Scores are your judgement; the caps are not.")


if __name__ == "__main__":
    main()
