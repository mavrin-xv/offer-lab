#!/usr/bin/env python3
"""Check an offer against the value equation and the stack rules, and say which lever to pull next.

Value equation (Alex Hormozi, "$100M Offers"):
    value = (dream outcome x perceived likelihood) / (time delay x effort and sacrifice)
Score each lever 1 to 10 from the buyer's side. For time delay and effort, 10 means slow and painful.
The index is only useful to compare versions of your own offer. It is not a market number.

Checks:
  - weakest lever: the one with the most room to move the index
  - every stack item must kill a named objection; items that kill none are cut candidates
  - every listed objection must be killed by at least one item, the guarantee or the proof
  - guarantee: needs a number (what result), a window (how long) and what happens on a miss
  - mechanism: needs a name; if a competitor could say it word for word, it is not yours
  - scarcity or urgency: needs a real reason (capacity, a cohort date); otherwise it is fake, remove it
  - cost to deliver vs price: a stack item that costs more than 20% of price is flagged

Input: a JSON file, see examples/data/offer.json. --compare runs a second version and prints the change.

Usage:
  python value_equation.py examples/data/offer.json
  python value_equation.py offer-v1.json --compare offer-v2.json
  python value_equation.py offer.json --format json

Exit codes: 0 no blockers, 1 a blocker (missing guarantee terms, fake scarcity, an objection nobody answers), 2 bad input.
"""
import argparse
import json
import sys

LEVERS = ["dream_outcome", "likelihood", "time_delay", "effort"]


def analyse(d):
    s = {}
    for k in LEVERS:
        try:
            v = float(d[k]["score"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"{k}.score missing or not a number")
        if not 1 <= v <= 10:
            raise ValueError(f"{k}.score={v} outside 1..10")
        s[k] = v
    index = (s["dream_outcome"] * s["likelihood"]) / (s["time_delay"] * s["effort"])
    # room to move: numerator levers gain from going up, denominator levers from going down
    room = {"dream_outcome": 10 - s["dream_outcome"], "likelihood": 10 - s["likelihood"],
            "time_delay": s["time_delay"] - 1, "effort": s["effort"] - 1}
    gain = {}
    for k in LEVERS:
        t = dict(s)
        t[k] = min(10, s[k] + 1) if k in ("dream_outcome", "likelihood") else max(1, s[k] - 1)
        gain[k] = (t["dream_outcome"] * t["likelihood"]) / (t["time_delay"] * t["effort"]) - index
    weakest = max(gain, key=gain.get)

    blockers, warns = [], []
    price = float(d.get("price") or 0)
    objections = [o.strip().lower() for o in d.get("objections", [])]
    stack = d.get("stack", [])
    killed = set()
    for it in stack:
        ks = [k.strip().lower() for k in (it.get("kills") or [])]
        if not ks:
            warns.append(f"stack item '{it.get('item')}' kills no objection: cut it or name the objection")
        killed |= set(ks)
        c = float(it.get("cost_to_deliver") or 0)
        if price and c > 0.2 * price:
            warns.append(f"stack item '{it.get('item')}' costs {c:g} to deliver, over 20% of the {price:g} price")
    g = d.get("guarantee") or {}
    for k in g.get("kills", []):
        killed.add(k.strip().lower())
    for k in (d.get("likelihood", {}).get("proof_kills") or []):
        killed.add(k.strip().lower())
    open_obj = [o for o in objections if o not in killed]
    for o in open_obj:
        blockers.append(f"objection not answered by any item, the guarantee or proof: '{o}'")
    stray = sorted(killed - set(objections))
    if stray:
        warns.append("items kill objections not on the list (add them or fix the spelling): " + ", ".join(stray))

    if not g:
        warns.append("no guarantee; fine if deliberate, but say so on the page")
    else:
        for k, label in (("number", "number (what result, measured how)"), ("window_days", "window (days)"), ("on_miss", "consequence (what happens on a miss)")):
            if not g.get(k):
                blockers.append(f"guarantee has no {label}")
        if not g.get("name"):
            warns.append("guarantee has no name; a named guarantee is easier to remember and repeat")
    m = d.get("mechanism") or {}
    if not m.get("name"):
        warns.append("no named mechanism: why does it work when the last thing they tried did not?")
    elif m.get("competitor_could_say", True):
        warns.append(f"mechanism '{m['name']}' could be said word for word by a rival; make it specific to how you work")
    sc = d.get("scarcity")
    if sc and sc.get("claim") and not sc.get("reason"):
        blockers.append(f"scarcity '{sc['claim']}' has no real reason (capacity, a date); remove it or state the reason")
    stack_value = sum(float(it.get("perceived_value") or 0) for it in stack)
    return {"scores": s, "index": round(index, 2), "weakest_lever": weakest,
            "gain_if_moved_1": {k: round(v, 2) for k, v in gain.items()}, "room": room,
            "stack_value": stack_value, "price": price, "blockers": blockers, "warnings": warns}


def show(name, r):
    s = r["scores"]
    print(f"{name}: index {r['index']}  = ({s['dream_outcome']:g} x {s['likelihood']:g}) / "
          f"({s['time_delay']:g} x {s['effort']:g})")
    for k in LEVERS:
        arrow = "up" if k in ("dream_outcome", "likelihood") else "down"
        mark = "  <- pull this one next" if k == r["weakest_lever"] else ""
        print(f"  {k:<14} {s[k]:>4g}   moving it 1 {arrow} adds {r['gain_if_moved_1'][k]:+.2f}{mark}")
    if r["price"] and r["stack_value"]:
        print(f"  stack value {r['stack_value']:g} vs price {r['price']:g} ({r['stack_value'] / r['price']:.1f}x); "
              "perceived values are your estimates, never print them as facts")
    for b in r["blockers"]:
        print(f"  BLOCK {b}")
    for w in r["warnings"]:
        print(f"  WARN  {w}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="offer JSON")
    ap.add_argument("--compare", help="a second version of the offer to compare with")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args()
    try:
        r1 = analyse(json.load(open(a.file, encoding="utf-8")))
        r2 = analyse(json.load(open(a.compare, encoding="utf-8"))) if a.compare else None
    except (OSError, ValueError) as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    if a.format == "json":
        print(json.dumps({"offer": r1, "compare": r2}, indent=2))
    else:
        show(a.file, r1)
        if r2:
            print()
            show(a.compare, r2)
            print(f"\nIndex {r1['index']} -> {r2['index']} ({r2['index'] - r1['index']:+.2f}); "
                  f"blockers {len(r1['blockers'])} -> {len(r2['blockers'])}")
    last = r2 or r1
    sys.exit(1 if last["blockers"] else 0)


if __name__ == "__main__":
    main()
