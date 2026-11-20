#!/usr/bin/env python3
"""Give an offer idea a GO / TEST / WAIT / KILL verdict from the evidence you actually have.

The default is TEST. An idea earns GO only with commitment evidence; talk alone never gets there.

Evidence types and their weight (from the Mom Test commitment ladder: time, reputation, money):
  paid          money changed hands: a pre-order, deposit, paid pilot             weight 5
  commitment    a calendar slot, an intro, a signed letter of intent, a data share weight 3
  past_spend    they told you what they already pay for this problem, with a number weight 2
  conversation  a specific story about the last time the problem happened        weight 1
  desk          forum threads, reviews, search results you found yourself         weight 1
  compliment    "great idea", "I would definitely buy"                            weight 0 (logged, ignored)

Rules, in order:
  KILL  a failure mode is marked fatal and has no fix
  KILL  10 or more conversations and none of them names the problem unprompted
  WAIT  a blocker outside your control (a platform change, a law, a missing partner) is open
  GO    at least 1 paid item, or 3 or more commitments, and the top failure modes each have a test or a fix
  TEST  everything else (default)
Red-flag phrases in the claims ("everyone needs this", "no competition", "zero risk", "guaranteed")
are printed and push a GO down to TEST until they are removed or backed.

Input: a JSON file, see examples/data/idea.json.

Usage:
  python reality_check.py examples/data/idea.json
  python reality_check.py idea.json --format json
  python reality_check.py --template > idea.json

Exit codes: 0 GO or TEST, 1 KILL or WAIT, 2 bad input.
"""
import argparse
import json
import re
import sys

WEIGHT = {"paid": 5, "commitment": 3, "past_spend": 2, "conversation": 1, "desk": 1, "compliment": 0}
RED = [r"everyone needs", r"no competition", r"no competitors", r"zero risk", r"guaranteed", r"can'?t fail",
       r"production[- ]ready", r"zero issues", r"huge market", r"billion[- ]dollar"]

TEMPLATE = {
    "idea": "Monthly stock count cleanup for online shops with 200+ SKUs, flat fee",
    "claims": ["shops lose sales when counts are wrong"],
    "evidence": [
        {"type": "conversation", "note": "owner described last month's oversell, unprompted", "pain_named": True},
        {"type": "compliment", "note": "said they would definitely buy"}
    ],
    "failure_modes": [
        {"risk": "shops will not share store access", "fatal": False, "test": "ask 5 owners for read-only access"}
    ],
    "competition": ["a bookkeeper", "an inventory app", "do nothing"],
    "blockers": [],
    "effort_weeks": 3,
    "reward_note": "5 clients at the flat fee covers the month"
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="idea JSON")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--template", action="store_true", help="print an example idea JSON")
    a = ap.parse_args()
    if a.template:
        print(json.dumps(TEMPLATE, indent=2))
        return
    if not a.file:
        ap.error("give an idea JSON file or --template")
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"cannot read {a.file}: {e}", file=sys.stderr)
        sys.exit(2)

    ev = d.get("evidence", [])
    bad = [e.get("type") for e in ev if e.get("type") not in WEIGHT]
    if bad:
        print(f"unknown evidence type(s): {', '.join(map(str, bad))}; use {', '.join(WEIGHT)}", file=sys.stderr)
        sys.exit(2)
    count = {k: sum(1 for e in ev if e["type"] == k) for k in WEIGHT}
    score = sum(WEIGHT[e["type"]] for e in ev)
    convs = [e for e in ev if e["type"] == "conversation"]
    named = sum(1 for e in convs if e.get("pain_named"))
    fm = d.get("failure_modes", [])
    fatal = [f for f in fm if f.get("fatal") and not (f.get("fix") or f.get("test"))]
    untested = [f for f in fm[:3] if not (f.get("fix") or f.get("test"))]
    blockers = [b for b in d.get("blockers", []) if b]
    text = " ".join([d.get("idea", "")] + d.get("claims", []))
    flags = sorted({m.group(0) for rx in RED for m in re.finditer(rx, text, re.I)})
    comp = d.get("competition", [])

    reasons = []
    if fatal:
        v = "KILL"
        reasons.append(f"fatal failure mode with no fix: {fatal[0]['risk']}")
    elif len(convs) >= 10 and named == 0:
        v = "KILL"
        reasons.append(f"{len(convs)} conversations, none named the problem unprompted")
    elif blockers:
        v = "WAIT"
        reasons.append(f"open blocker: {blockers[0]}")
    elif (count["paid"] >= 1 or count["commitment"] >= 3) and not untested:
        v = "GO"
        reasons.append(f"{count['paid']} paid, {count['commitment']} commitment(s); top risks have a test or fix")
    else:
        v = "TEST"
        if count["paid"] == 0 and count["commitment"] < 3:
            reasons.append(f"no money and {count['commitment']} commitment(s); need 1 paid or 3 commitments")
        if untested:
            reasons.append(f"{len(untested)} of the top 3 failure modes {'has' if len(untested) == 1 else 'have'} no test: {untested[0]['risk']}")
    if v == "GO" and flags:
        v = "TEST"
        reasons.append("red-flag claims must be removed or backed first")
    if not any(re.search(r"nothing|do nothing|spreadsheet|manual|status quo", c, re.I) for c in comp):
        reasons.append("competition list has no 'do nothing' or manual workaround; add it (it is usually the real rival)")

    out = {"verdict": v, "reasons": reasons, "evidence_score": score, "evidence_count": count,
           "conversations_naming_pain": f"{named}/{len(convs)}", "red_flags": flags,
           "failure_modes_without_test": [f["risk"] for f in fm if not (f.get("fix") or f.get("test"))]}
    if a.format == "json":
        print(json.dumps(out, indent=2))
    else:
        print(f"Idea: {d.get('idea', '?')}\n")
        print(f"VERDICT: {v}")
        for r in reasons:
            print(f"  - {r}")
        print(f"\nEvidence score {score} (paid x5, commitment x3, past spend x2, conversation and desk x1, compliments x0)")
        print("  " + ", ".join(f"{k} {n}" for k, n in count.items()))
        print(f"  conversations that named the pain unprompted: {named}/{len(convs)}")
        if count["compliment"]:
            print(f"  {count['compliment']} compliment(s) ignored: they cost the speaker nothing")
        if flags:
            print("Red-flag phrases: " + ", ".join(flags))
        if out["failure_modes_without_test"]:
            print("Failure modes with no test yet: " + "; ".join(out["failure_modes_without_test"]))
        print(f"Effort: {d.get('effort_weeks', '?')} weeks. Reward: {d.get('reward_note', '?')}")
    sys.exit(1 if v in ("KILL", "WAIT") else 0)


if __name__ == "__main__":
    main()
