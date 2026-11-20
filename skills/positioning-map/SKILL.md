---
name: positioning-map
description: Builds a positioning for an offer from evidence using April Dunford's components (competitive alternatives, unique attributes, value, best-fit customers, market category, plus relevant trends), then triages every competitor claim into saturated, contested or white space and generates angle options that pass a 7-point gate. Treats "do nothing" as a competitor. Use when someone says "how do I stand out", "what makes us different", "positioning", "who are we competing with", "what should the headline say", "find an angle", "everyone says the same thing", or pastes competitor pages.
---

# Positioning map

Positioning is the context you put the offer in so the right buyer sees why it is worth it. It is decided before
copy, and copy comes from it. This skill follows April Dunford's method from *Obviously Awesome* (2019), read through
public summaries (see Credits in the README). It adds two things the book leaves to judgement: a claim triage across
competitors and a pass or fail gate for the angle.

## The components

| Component | Question | Evidence |
|---|---|---|
| Competitive alternatives | What would the buyer do if you did not exist? | buyer interviews, lost deals; include doing nothing |
| Unique attributes | What do you have that the alternatives lack? | features, method, delivery, people; each with proof |
| Value (and proof) | What do those attributes let the buyer do? | themes grouped from the attributes |
| Best-fit customers | Who cares a lot about that value? | won deals, `icp_traits.py` in `niche-score` |
| Market category | What frame makes the value obvious? | where buyers would look for you |
| Relevant trends (optional) | Is there a shift that makes this matter now? | only if it is real and the buyer feels it |

Details, the 10 steps and the 3 category styles: [references/dunford-method.md](references/dunford-method.md).

## Procedure

1. Start with your best current buyers if you have any; if not, use the niche from the offer card.
2. List competitive alternatives from the buyer's side. Write one pack per alternative with
   `templates/competitor-pack.md`: their claims and the complaints buyers make about them, each with a source.
   Doing nothing gets a pack too (`examples/data/competitors/do-nothing.md` shows one).
3. Write your candidate claims in a file with a `## Candidate claims` section, tagged the same way.
4. Triage:

   ```bash
   python3 scripts/claim_triage.py competitors/*.md --ours our-claims.md
   ```

   SATURATED means 3 or more rivals say it; do not lead with it. CONTESTED means 1 or 2 do; lead only with proof
   they cannot match. WHITE SPACE nobody claims; it is a candidate if buyers care. A theme where buyers complain about
   every rival is the strongest lead you can find, if you can prove you fix it.
5. Fill the components in `templates/positioning.md`. Attributes without proof go to a "to prove" list, not the map.
6. Generate angle options with the 8 generators in [references/angles.md](references/angles.md). Pick the buyer's
   awareness stage first; it decides how much the angle explains.
7. Run each option through the 7-point gate (same file). Keep the 2 or 3 that pass. A human picks one.

## Rules

- Alternatives come from what buyers say, not from a search for "competitors". If they would use a spreadsheet,
  the spreadsheet is the rival.
- An attribute without proof you can show today is not on the map.
- Do not position against a rival by name on the page unless you can prove the comparison and would be happy for
  them to read it.
- Trends only when the buyer already feels them. A trend you have to explain is a second sale.
- Two different best-fit buyers means two positionings. Pick one per offer card.

## Output

The filled positioning template, the triage table, 2 or 3 gated angles, and the "to prove" list, written to offer card
section 3.
