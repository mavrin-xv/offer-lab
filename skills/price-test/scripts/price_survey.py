#!/usr/bin/env python3
"""Read a price survey: Van Westendorp ranges or a Gabor-Granger demand curve.

vw  Van Westendorp Price Sensitivity Meter. Each respondent gives four prices:
      too_cheap      so cheap you would doubt the quality
      cheap          a bargain
      expensive      getting expensive, but you would still consider it
      too_expensive  too expensive to consider
    Curves (share of respondents at price p):
      too cheap     share whose too_cheap >= p        not cheap      1 - share whose cheap >= p
      too expensive share whose too_expensive <= p    not expensive  1 - share whose expensive <= p
    Intersections (one convention, the one Wikipedia describes; others exist and give different numbers):
      PMC  point of marginal cheapness     too cheap  x  not cheap
      PME  point of marginal expensiveness too expensive x not expensive
      OPP  optimal price point             too cheap  x  too expensive
      IPP  indifference price point        cheap (share >= p) x expensive (share <= p)
    Acceptable range is PMC to PME. OPP is where the fewest people reject the price, not where revenue peaks.
    Rows where the four answers are not in rising order are dropped and counted.

gg  Gabor-Granger. Each row is one answer to "would you buy at this price?": respondent, price, answer.
    Answer is yes/no, or 1 to 5 purchase likelihood. On a 1 to 5 scale only 5 counts as yes by default
    (--top-box 2 counts 4 and 5). Prints share buying and a revenue index (price x share) per price.

Both are stated willingness to pay. People say yes more often in a survey than at a checkout.
Treat the output as a range to test with real money, not as the price.

Usage:
  python price_survey.py vw examples/data/vw-survey.csv
  python price_survey.py gg examples/data/gg-survey.csv
  python price_survey.py gg gg.csv --top-box 2 --format json

Exit codes: 0 ok, 2 bad input.
"""
import argparse
import csv
import json
import sys
from collections import defaultdict


def num(v, n, col):
    try:
        return float(str(v).replace(",", "").replace("$", "").strip())
    except ValueError:
        raise ValueError(f"line {n}: {col}={v!r} is not a number")


def cross(grid, f, g):
    """First price where f - g changes sign, linearly interpolated."""
    prev = None
    for p in grid:
        d = f(p) - g(p)
        if prev is not None and (d == 0 or (d > 0) != (prev[1] > 0)):
            p0, d0 = prev
            return p if d == d0 else p0 + (p - p0) * (d0 / (d0 - d))
        prev = (p, d)
    return None


def vw(path):
    rows, dropped = [], 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            v = [num(r[c], n, c) for c in ("too_cheap", "cheap", "expensive", "too_expensive")]
            if not (v[0] <= v[1] <= v[2] <= v[3]):
                dropped += 1
                continue
            rows.append(v)
    if len(rows) < 2:
        raise ValueError("need at least 2 consistent answers")
    N = len(rows)
    lo, hi = min(x[0] for x in rows), max(x[3] for x in rows)
    step = (hi - lo) / 2000 or 1
    grid = [lo + i * step for i in range(2001)]
    too_cheap = lambda p: sum(x[0] >= p for x in rows) / N
    cheap = lambda p: sum(x[1] >= p for x in rows) / N
    not_cheap = lambda p: 1 - cheap(p)
    expensive = lambda p: sum(x[2] <= p for x in rows) / N
    not_exp = lambda p: 1 - expensive(p)
    too_exp = lambda p: sum(x[3] <= p for x in rows) / N
    res = {"respondents": N, "dropped_inconsistent": dropped,
           "PMC": cross(grid, too_cheap, not_cheap), "PME": cross(grid, too_exp, not_exp),
           "OPP": cross(grid, too_cheap, too_exp), "IPP": cross(grid, cheap, expensive)}
    return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in res.items()}


def gg(path, top_box):
    by = defaultdict(lambda: [0, 0])
    with open(path, encoding="utf-8-sig", newline="") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            p = num(r["price"], n, "price")
            ans = str(r["answer"]).strip().lower()
            if ans in ("yes", "y", "true", "no", "n", "false"):
                yes = ans in ("yes", "y", "true")
            else:
                s = num(ans, n, "answer")
                if not 1 <= s <= 5:
                    raise ValueError(f"line {n}: answer {s:g} outside 1..5")
                yes = s > 5 - top_box
            by[p][0] += yes
            by[p][1] += 1
    if not by:
        raise ValueError("no answers")
    table = []
    for p in sorted(by):
        y, t = by[p]
        table.append({"price": p, "answers": t, "buy_share": round(y / t, 3), "revenue_index": round(p * y / t, 2)})
    best = max(table, key=lambda x: x["revenue_index"])
    return {"table": table, "best_revenue_price": best["price"], "top_box": top_box}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("method", choices=["vw", "gg"])
    ap.add_argument("file", help="survey CSV")
    ap.add_argument("--top-box", type=int, default=1, choices=[1, 2],
                    help="gg on a 1-5 scale: 1 counts only 5 as yes (default), 2 counts 4 and 5")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args()
    try:
        r = vw(a.file) if a.method == "vw" else gg(a.file, a.top_box)
    except (OSError, ValueError, KeyError) as e:
        print(f"bad input: {e}", file=sys.stderr)
        sys.exit(2)
    if a.format == "json":
        print(json.dumps(r, indent=2))
        return
    if a.method == "vw":
        f = lambda v: f"{v:,.0f}" if v is not None else "no crossing"
        print(f"Van Westendorp, {r['respondents']} consistent answers ({r['dropped_inconsistent']} dropped)\n")
        print(f"  Acceptable range  {f(r['PMC'])} to {f(r['PME'])}   (PMC to PME)")
        print(f"  Optimal (OPP)     {f(r['OPP'])}   fewest people reject it; not proof of the revenue peak")
        print(f"  Indifference (IPP){f(r['IPP']):>6}   as many call it cheap as call it expensive")
        if r["respondents"] < 30:
            print(f"\n  NOTE: {r['respondents']} answers is a small sample; read the range as rough")
    else:
        print(f"Gabor-Granger ({'only 5' if a.top_box == 1 else '4 and 5'} counted as yes on 1-5 answers)\n")
        print("| Price | Answers | Would buy | Revenue index |")
        print("|---|---|---|---|")
        for x in r["table"]:
            mark = "  <- highest" if x["price"] == r["best_revenue_price"] else ""
            print(f"| {x['price']:,.0f} | {x['answers']} | {x['buy_share']:.0%} | {x['revenue_index']:,.0f}{mark} |")
    print("\nStated, not paid. Test the range with a real checkout or a pre-order before you print a price.")


if __name__ == "__main__":
    main()
