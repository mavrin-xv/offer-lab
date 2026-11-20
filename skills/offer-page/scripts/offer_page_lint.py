#!/usr/bin/env python3
"""Lint an offer page draft (markdown) before anyone sees it.

Sections it looks for, by H2 heading words (the outline in templates/offer-page.md):
  problem      problem, pain, why, sound familiar
  mechanism    how it works, method, mechanism, process
  stack        what you get, included, inside, the offer
  proof        proof, results, case, before and after, who
  guarantee    guarantee, risk, promise
  price        price, pricing, cost, invest
  faq          faq, questions, objections
The hero is the H1 plus the first paragraph under it.

BLOCK (exit 1):
  - placeholder text left in: [testimonial], TODO, TBD, lorem, XX, ???
  - a scarcity or deadline line ("only 3 spots", "ends tonight", "last chance") with no
    <!-- scarcity: reason --> comment that states the real limit
  - no price anywhere (a number next to a currency sign, or "per month")
  - a guarantee section with no number or no window in it
WARN:
  - missing sections from the outline
  - hype words (unlock, seamless, game-changer, supercharge, revolutionize, effortless, ...)
  - hero longer than 25 words, or hero with no outcome number or timeframe
  - more "we/our" than "you/your" in the page
  - more than one distinct call to action text
  - testimonials (lines in quotes followed by a name) with no "(permission: yes)" note

Usage:
  python offer_page_lint.py examples/offer-page.md
  python offer_page_lint.py page.md --format json

Exit codes: 0 no blockers, 1 at least one BLOCK, 2 bad input.
"""
import argparse
import json
import re
import sys

SECTIONS = {
    "problem": r"problem|pain|\bwhy\b|sound familiar",
    "mechanism": r"how it works|method|mechanism|process",
    "stack": r"what you get|included|inside|the offer",
    "proof": r"proof|result|case|before and after|who it|who this",
    "guarantee": r"guarantee|risk|promise",
    "price": r"price|pricing|cost|invest",
    "faq": r"faq|questions|objection",
}
HYPE = ["unlock", "seamless", "game-changer", "game changer", "supercharge", "revolutioniz", "effortless",
        "skyrocket", "10x", "cutting-edge", "next-level", "world-class", "best-in-class", "secret", "hack"]
SCARCITY = r"only \d+ (spots|seats|places)|spots left|ends (tonight|today|soon)|last chance|limited time|hurry|before it'?s gone"
PLACEHOLDER = r"\[testimonial\]|\bTODO\b|\bTBD\b|lorem ipsum|\bXX+\b|\?\?\?"
CTA = r"^\s*(?:\*\*)?\[([^\]]{3,60})\]\((?:#|https?://)[^)]*\)(?:\*\*)?\s*$|^\s*>\s*\*\*CTA:\*\*\s*(.+)$"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="offer page draft in markdown")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    a = ap.parse_args()
    try:
        text = open(a.file, encoding="utf-8").read()
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    lines = text.splitlines()
    block, warn = [], []

    heads = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    found = {k: next((h for _, h in heads if re.search(rx, h, re.I)), None) for k, rx in SECTIONS.items()}
    for k, h in found.items():
        if not h:
            warn.append(f"no {k} section (looked for an H2 with: {SECTIONS[k].replace(chr(92) + 'b', '').replace('|', ', ')})")

    h1 = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if h1 is None:
        warn.append("no H1: the hero needs a headline")
    else:
        para = []
        for l in lines[h1 + 1:]:
            if l.startswith("#"):
                break
            if l.strip():
                para.append(l.strip())
            elif para:
                break
        hero = lines[h1][2:] + " " + " ".join(para)
        nw = len(re.findall(r"\w+", hero))
        if nw > 25:
            warn.append(f"hero is {nw} words (headline + first paragraph); aim for 25 or fewer")
        if not re.search(r"\d", hero):
            warn.append("hero has no number: name the outcome or the timeframe")

    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in re.finditer(PLACEHOLDER, body, re.I):
        block.append(f"placeholder left in: '{m.group(0)}'")
    notes = re.findall(r"<!--\s*scarcity:\s*(.+?)-->", text, re.I | re.S)
    for m in re.finditer(SCARCITY, body, re.I):
        if not notes:
            block.append(f"scarcity line '{m.group(0)}' with no <!-- scarcity: reason --> note; state the real limit or remove it")
    if not re.search(r"[$€£]\s?\d|\d\s?(usd|eur|gbp)\b|\d+\s*(per|/)\s*(month|mo|year|shop|seat)", body, re.I):
        block.append("no price on the page")
    if found["guarantee"]:
        start = next(i for i, h in heads if h == found["guarantee"])
        end = next((i for i, _ in heads if i > start), len(lines))
        g = "\n".join(lines[start:end])
        if not re.search(r"\d", g):
            block.append("guarantee section has no number: what result, measured how")
        if not re.search(r"\d+\s*(day|week|month)s?|within", g, re.I):
            block.append("guarantee section has no window (how many days)")

    low = body.lower()
    for w in HYPE:
        if w in low:
            warn.append(f"hype word: '{w}'")
    we = len(re.findall(r"\b(we|our|us)\b", low))
    you = len(re.findall(r"\b(you|your)\b", low))
    if we > you:
        warn.append(f"'we/our/us' {we} times vs 'you/your' {you}: write about the buyer")
    ctas = set()
    for l in lines:
        m = re.match(CTA, l)
        if m:
            ctas.add((m.group(1) or m.group(2)).strip().lower())
    if len(ctas) > 1:
        warn.append(f"{len(ctas)} different calls to action: {sorted(ctas)}; pick one")
    if not ctas:
        warn.append("no call to action line found (a lone markdown link, or a '> **CTA:** ...' line)")
    for i, l in enumerate(lines):
        if re.match(r'^\s*>?\s*["“].{10,}["”]', l):
            nxt = " ".join(lines[i:i + 2])
            if re.search(r"[-\u2014]\s*\w+", nxt) and "permission: yes" not in nxt.lower():
                warn.append(f"line {i + 1}: testimonial with no '(permission: yes)' note")

    res = {"blockers": block, "warnings": warn, "sections": found, "cta": sorted(ctas)}
    if a.format == "json":
        print(json.dumps(res, indent=2))
    else:
        print(f"{a.file}: {len(block)} BLOCK, {len(warn)} WARN")
        print("Sections: " + ", ".join(f"{k} {'ok' if v else 'missing'}" for k, v in found.items()))
        for b in block:
            print(f"  BLOCK {b}")
        for w in warn:
            print(f"  WARN  {w}")
    sys.exit(1 if block else 0)


if __name__ == "__main__":
    main()
