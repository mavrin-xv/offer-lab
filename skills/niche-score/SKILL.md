---
name: niche-score
description: Scores niche candidates on three dimensions (Money, Channel, Pain, 1 to 5 each) with evidence caps that stop wishful scores, returns SHIP, ITERATE or KILL, and writes a channel map, a service angle and kill criteria for the winner. With 10 or more won and lost deals it finds the traits that separate buyers from non-buyers and tests that profile on held-out deals. Use when someone says "which niche should I pick", "who should I sell to", "score these niches", "is this market worth it", "who is my ideal customer", "ICP", or lists several possible audiences for one skill.
---

# Niche score

A niche is worth an offer when three things are true at once: they already pay to fix this (Money), you can reach
them through a channel you can name (Channel), and they describe the problem in their own words (Pain). Market size
is not on the list. A huge market you cannot reach, or one that does not pay, scores low.

The scores are your judgement. The caps are not: `scripts/niche_score.py` lowers any score the evidence does not
support and says why.

## Two modes

- **Cold mode** (no customers yet): score candidates from desk research and conversations. Most first offers start here.
- **Evidence mode** (10 or more won and 10 or more lost deals): find the traits that separate won from lost, then
  check them on deals the profile has not seen. See [references/evidence-mode.md](references/evidence-mode.md).

## Procedure (cold mode)

1. Write each candidate as a claim: "[buyer type] with [size or trait] who [situation]". "Small businesses" is not a
   niche. "Online shops with 200+ SKUs selling on two or more channels" is.
2. For each candidate, collect before you score:
   - **Money:** what they pay today for this problem, and to whom (a bookkeeper, an app, an agency, their own
     evenings). Current spend, not what they might pay.
   - **Channel:** three exact queries, lists or communities where they gather. "Social media" is not a channel.
     "Forum search for 'inventory count wrong' in two seller communities" is.
   - **Pain:** a quote in their words, and the number of distinct people or threads where you saw it.
3. Score with the rubric in [references/scoring-rubric.md](references/scoring-rubric.md). Write one reason per
   dimension. Fill `templates/niche-sheet.md` or a CSV (`python3 scripts/niche_score.py --template`).
4. Run the scorer:

   ```bash
   python3 scripts/niche_score.py niches.csv
   ```

5. For the top candidate, write:
   - **Channel map:** the three exact queries or lists, and what you will post or send there first.
   - **Service angle:** "[outcome verb] [object] for [buyer] in [timeframe]". Example: "Match stock counts to the shelf
     for shops with 200+ SKUs, every month by the 1st."
   - **Price band:** a rough range from what they pay today (the real price comes in `price-test`).
   - **Kill criteria:** what you would have to see in the next two weeks to drop it (for example "fewer than 3 of 10
     owners name the problem unprompted").
6. Optional segment table: region by business type by size, with an estimated count per cell and the source you
   could list them from. Mark every estimate as an estimate.

## Verdicts

| Total after caps | Verdict | Next |
|---|---|---|
| 11 to 15 | SHIP | take it to `idea-reality-check` |
| 8 to 10 | ITERATE | collect the missing evidence named in the caps, rescore |
| under 8 | KILL | drop it, or narrow it and score again |

Any dimension at 1 holds the niche at ITERATE whatever the total. A niche with a perfect channel and no money is
still a niche with no money.

## Rules

- Channel without an exact query, list or community scores 2 at most.
- Pain without a quote in the buyer's words scores 3 at most. Fewer than 3 named instances: 3 at most.
- Money without a named current spend scores 2 at most.
- How well a niche fits your brand or your taste is not a dimension. Write it down separately if it matters to you.
- Do not average your way out of a 1. Fix it or drop the niche.

## Output

The scored table with caps, the channel map, service angle, price band and kill criteria for the winner, written to
the offer card section 1.
