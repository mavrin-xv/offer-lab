# Walkthrough: one offer from niche to test verdict

Northwind Ops, its shops, its rivals, every deal, survey answer, quote and number below are invented for this
example. The outputs are real: each block is what the script prints on the files in `examples/data/`.

Northwind Ops is a two-person studio. They can clean up stock counts across sales channels by hand. They want to know
who to sell that to, for how much, and whether to build it out.

## 1. Niche

Five candidates, each scored on Money, Channel and Pain with a reason (`examples/data/niches.csv`).

```bash
python3 skills/niche-score/scripts/niche_score.py examples/data/niches.csv
```

```
| # | Niche | M | C | P | Total | Verdict |
|---|---|---|---|---|---|---|
| 1 | Stock count cleanup for online shops with 200+ SKUs | 4 | 4 | 5 | 13/15 | SHIP |
| 2 | Returns and refund tracking for apparel shops | 4 | 4 | 4 | 12/15 | SHIP |
| 3 | Bookkeeping catch-up for dental clinics | 4 | 2 | 3 | 9/15 | ITERATE |
| 4 | Chatbot for local restaurants | 3 | 4 | 2 | 9/15 | ITERATE |
| 5 | Notion workspace setup for solo creators | 2 | 3 | 3 | 8/15 | ITERATE |

Caps applied:
- Bookkeeping catch-up for dental clinics: pain 4->3: no quote in their words
```

The dental idea had a pain score of 4 with no quote behind it, so it dropped to 3. Stock count cleanup goes forward.

Later, with 26 deals logged (13 won, 13 lost), the buyer profile is checked against deals it has not seen:

```bash
python3 skills/niche-score/scripts/icp_traits.py examples/data/deals.csv
```

```
Fit traits: 200+ skus, founder runs ops, pays a bookkeeper, sells on 2+ channels, stock mismatch last quarter
Disqualifiers: under 50 skus, no stock mismatch, single channel, agency manages ops, price shopper

Holdout: 9/10 predicted right (90%).
```

"Uses spreadsheets" shows up in 38% of won and 75% of lost deals. It is in the table but is neither a fit trait nor
a disqualifier.

## 2. Reality check

Four owner conversations, one past spend, two commitments, some desk research and one compliment
(`examples/data/idea.json`).

```bash
python3 skills/idea-reality-check/scripts/reality_check.py examples/data/idea.json
```

```
VERDICT: TEST
  - no money and 2 commitment(s); need 1 paid or 3 commitments
  - 1 of the top 3 failure modes has no test: one cleanup is enough, nobody renews

Evidence score 13 (paid x5, commitment x3, past spend x2, conversation and desk x1, compliments x0)
  paid 0, commitment 2, past_spend 1, conversation 4, desk 1, compliment 1
  conversations that named the pain unprompted: 3/4
  1 compliment(s) ignored: they cost the speaker nothing
Red-flag phrases: Everyone needs
```

Two jobs come out of it: find a test for renewals (the stack adds a monthly returns map), and remove "everyone needs
this" from the claims.

## 3. Positioning

One pack per rival, including doing nothing, plus Northwind's candidate claims.

```bash
python3 skills/positioning-map/scripts/claim_triage.py examples/data/competitors --ours examples/data/our-claims.md
```

```
| Theme | Rivals claiming | Status | Example |
|---|---|---|---|
| never-oversell | 3 | SATURATED | Fewer stock surprises at month end |
| auto-sync | 2 | CONTESTED | One stock number, everywhere you sell |
...
What buyers complain about:
- [counts-drift] at 4 rivals
- [setup-pain] at 2 rivals
...
Your candidate claims:
- WHITE SPACE [counts-drift] Your stock counts match the shelf on the 1st of every month, returns and bundles included  (0 rivals); rivals get complaints here (...), prove it
- CONTESTED   [done-for-you] We do the monthly count cleanup for you  (1 rival)
- CONTESTED   [auto-sync] Automatic sync across channels  (2 rivals)
- WHITE SPACE [audit-trail] A one-page report of every count we changed and why  (0 rivals)

Claims with no source (go back and capture where you saw it):
- Countly Sync (invented): [integrations] Works with the channels you already use
```

"Never oversell" is taken three times over. Nobody claims that counts stay right, and buyers complain about drift at
every rival, so that becomes the lead, with the audit report as proof.

## 4. Value stack

Version 1 was what the studio would have shipped by instinct (`offer-v1.json`). Version 2 answers each objection
(`offer.json`).

```bash
python3 skills/value-stack/scripts/value_equation.py examples/data/offer-v1.json --compare examples/data/offer.json
```

```
examples/data/offer-v1.json: index 0.67  = (6 x 4) / (6 x 6)
  likelihood        4   moving it 1 up adds +0.17  <- pull this one next
  BLOCK objection not answered by any item, the guarantee or proof: 'i do not want an outsider in my store'
  BLOCK objection not answered by any item, the guarantee or proof: 'will it stay fixed'
  BLOCK objection not answered by any item, the guarantee or proof: 'too expensive'
  BLOCK guarantee has no number (what result, measured how)
  BLOCK scarcity 'Only 3 spots left' has no real reason (capacity, a date); remove it or state the reason
  WARN  stack item 'Weekly strategy call' kills no objection: cut it or name the objection
  ...
examples/data/offer.json: index 9.33  = (8 x 7) / (3 x 2)
  effort            2   moving it 1 down adds +9.33  <- pull this one next

Index 0.67 -> 9.33 (+8.66); blockers 5 -> 0
```

The weekly call went (it answered nothing and cost a quarter of the price). In came read-only access with a written
policy, the returns map, and the Shelf-Match Guarantee: a 50-SKU spot check within 1 unit, inside 7 days, or the month is
redone free. Scarcity stayed, now with its reason: 4 new shops a month, because each count takes a full day.

## 5. Price

38 best-fit shop owners answered the four Van Westendorp questions; two rows were inconsistent and dropped. 30 answered
Gabor-Granger at five prices.

```bash
python3 skills/price-test/scripts/price_survey.py vw examples/data/vw-survey.csv
python3 skills/price-test/scripts/price_survey.py gg examples/data/gg-survey.csv
```

```
Van Westendorp, 38 consistent answers (2 dropped)
  Acceptable range  230 to 570   (PMC to PME)
  Optimal (OPP)     250   fewest people reject it; not proof of the revenue peak
  Indifference (IPP)   350   as many call it cheap as call it expensive

| Price | Answers | Would buy | Revenue index |
| 250 | 30 | 80% | 200 |
| 350 | 30 | 60% | 210  <- highest |
| 450 | 30 | 37% | 165 |
...
Stated, not paid.
```

The studio planned 450. The survey says 350 earns the most on stated answers, and 450 is still inside the range. With
a guarantee in place they keep 450 on the page and plan to test it against 350 with real pre-orders.

## 6. Page

```bash
python3 skills/offer-page/scripts/offer_page_lint.py examples/offer-page-draft.md
python3 skills/offer-page/scripts/offer_page_lint.py examples/offer-page.md
```

```
examples/offer-page-draft.md: 4 BLOCK, 8 WARN
  BLOCK placeholder left in: '[testimonial]'
  BLOCK scarcity line 'Only 3 spots' with no <!-- scarcity: reason --> note; state the real limit or remove it
  BLOCK guarantee section has no number: what result, measured how
  BLOCK guarantee section has no window (how many days)
  WARN  hero is 36 words (headline + first paragraph); aim for 25 or fewer
  WARN  'we/our/us' 9 times vs 'you/your' 4: write about the buyer
  WARN  2 different calls to action: ['book a call', 'start free trial']; pick one
  ...
examples/offer-page.md: 0 BLOCK, 0 WARN
```

The final page opens with "Stock counts that match the shelf on the 1st of every month". Its pilot quote is invented
for this example and marked "(permission: yes)" to show the format; a real page needs real written permission.

## 7. Test

The lines go into the decision log before any traffic: GO at 5% of best-fit visitors booking a count, KILL at 2%, and
in between counts as KILL.

```bash
python3 skills/validation-plan/scripts/validation_calc.py plan --go 0.05 --kill 0.02 --per-day 60
```

```
GO at 5.0% or more, KILL at 2.0% or less.
Visitors needed: 191 (expect about 10 signups if the GO rate is true, 4 if the KILL rate is).
At 60 visitors a day: 4 days.
```

Three possible endings, on the same 640 visitors:

```
36 of 640 converted: 5.6% (95% range 4.1% to 7.7%)
VERDICT: GO  (whole interval above the kill rate, rate at or above go)

29 of 640 converted: 4.5% (95% range 3.2% to 6.4%)
VERDICT: UNCLEAR  (enough visitors, still between the lines; apply your pre-written rule (default: KILL))

12 of 640 converted: 1.9% (95% range 1.1% to 3.2%)
Paid pre-orders: 3
VERDICT: GO  (3 paid pre-orders reached the line of 3)
```

The last one is the point of the ladder: three shops paying up front outweigh a weak signup rate.
