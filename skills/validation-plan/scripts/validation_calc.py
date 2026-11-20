#!/usr/bin/env python3
"""Plan a smoke test with numbers written down before it starts, then judge the result against them.

plan   How many visitors you need to tell a GO rate from a KILL rate.
       --go     the conversion rate that would make you build (for example 0.05 = 5%)
       --kill   the rate at or below which you stop (for example 0.02)
       Sample size for a one-sided test at 95% confidence and 80% power (normal approximation).
       Also prints the visitors you can buy or earn per day (--per-day) as days needed.

judge  Read a finished test. --visitors and --conversions, plus the same --go and --kill.
       Prints the conversion rate with a Wilson 95% interval and one of:
         GO           the whole interval is above the kill rate and the rate is at or above go
         KILL         the whole interval is below the go rate and the rate is at or below kill
         KEEP RUNNING fewer visitors than the plan said; do not decide yet
         UNCLEAR      enough visitors, still between the lines: apply the rule you wrote down
                      before the test (the default rule in this pack: UNCLEAR counts as KILL)
       Optional --preorders and --preorder-go: money beats signups; if paid pre-orders reach
       --preorder-go, the verdict is GO whatever the signup rate.

Thresholds are yours. Published "good" landing page rates (2 to 5% is often quoted) come from vendor
blogs, not studies; set your own from what the offer must earn to be worth building.

Usage:
  python validation_calc.py plan --go 0.05 --kill 0.02 --per-day 60
  python validation_calc.py judge --visitors 640 --conversions 29 --go 0.05 --kill 0.02
  python validation_calc.py judge --visitors 640 --conversions 12 --go 0.05 --kill 0.02 --preorders 3 --preorder-go 3

Exit codes: 0 GO, 1 KILL or UNCLEAR, 3 KEEP RUNNING, 2 bad input. "plan" exits 0.
"""
import argparse
import math
import sys

Z95, Z80 = 1.6449, 0.8416  # one-sided 95% confidence, 80% power


def sample_size(go, kill):
    num = Z95 * math.sqrt(kill * (1 - kill)) + Z80 * math.sqrt(go * (1 - go))
    return math.ceil((num / (go - kill)) ** 2)


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="visitors needed before the test")
    j = sub.add_parser("judge", help="verdict after the test")
    for s in (p, j):
        s.add_argument("--go", type=float, required=True, help="rate that means build, e.g. 0.05")
        s.add_argument("--kill", type=float, required=True, help="rate that means stop, e.g. 0.02")
    p.add_argument("--per-day", type=float, help="visitors per day you can send")
    j.add_argument("--visitors", type=int, required=True)
    j.add_argument("--conversions", type=int, required=True)
    j.add_argument("--preorders", type=int, default=0, help="paid pre-orders or deposits")
    j.add_argument("--preorder-go", type=int, help="paid pre-orders that mean GO on their own")
    a = ap.parse_args()

    if not 0 < a.kill < a.go < 1:
        print("need 0 < kill < go < 1, as shares (0.05 = 5%)", file=sys.stderr)
        sys.exit(2)
    n = sample_size(a.go, a.kill)

    if a.cmd == "plan":
        print(f"GO at {a.go:.1%} or more, KILL at {a.kill:.1%} or less.")
        print(f"Visitors needed: {n:,} (expect about {n * a.go:.0f} signups if the GO rate is true, "
              f"{n * a.kill:.0f} if the KILL rate is).")
        if a.per_day:
            print(f"At {a.per_day:g} visitors a day: {math.ceil(n / a.per_day)} days.")
        print("Write these numbers in the decision log now, before the first visitor.")
        return

    if a.visitors <= 0 or not 0 <= a.conversions <= a.visitors:
        print("need visitors > 0 and 0 <= conversions <= visitors", file=sys.stderr)
        sys.exit(2)
    rate = a.conversions / a.visitors
    lo, hi = wilson(a.conversions, a.visitors)
    if a.preorder_go and a.preorders >= a.preorder_go:
        v, why = "GO", f"{a.preorders} paid pre-orders reached the line of {a.preorder_go}"
    elif a.visitors < n:
        v, why = "KEEP RUNNING", f"{a.visitors:,} of {n:,} planned visitors; stopping early on a good day finds luck"
    elif lo > a.kill and rate >= a.go:
        v, why = "GO", "whole interval above the kill rate, rate at or above go"
    elif hi < a.go and rate <= a.kill:
        v, why = "KILL", "whole interval below the go rate, rate at or below kill"
    else:
        v, why = "UNCLEAR", "enough visitors, still between the lines; apply your pre-written rule (default: KILL)"
    print(f"{a.conversions} of {a.visitors:,} converted: {rate:.1%} (95% range {lo:.1%} to {hi:.1%})")
    print(f"Lines: GO {a.go:.1%}, KILL {a.kill:.1%}. Plan: {n:,} visitors.")
    if a.preorders:
        print(f"Paid pre-orders: {a.preorders}")
    print(f"VERDICT: {v}  ({why})")
    sys.exit({"GO": 0, "KEEP RUNNING": 3}.get(v, 1))


if __name__ == "__main__":
    main()
