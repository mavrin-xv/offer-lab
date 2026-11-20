---
name: price-test
description: Sets and tests a price for an offer: picks the value metric, anchors on the cost of the problem, designs good-better-best tiers, runs Van Westendorp and Gabor-Granger surveys through a script that shows the acceptable range and the revenue peak, reads symptoms like "sales are slow" or "everyone says yes" as pricing signals, and plans price changes without breaking trust. Treats survey answers as stated willingness to pay, to be checked with real money. Use when someone says "what should I charge", "how do I price this", "is my price too low", "should I raise prices", "pricing tiers", "price survey", "Van Westendorp", "everyone says yes", or "nobody is buying".
---

# Price test

Price is part of the offer, not a number added at the end. It says who the offer is for, and it decides whether the
business works at all. This skill finds a range from evidence, picks one point, and then tests that point with money.

Surveys measure what people say they would pay. People say yes more often in a survey than at a checkout. Every
survey result here is a range to test, never the price.

## Procedure

1. **Value metric.** Pick the unit the price scales with: per shop, per seat, per month, per project, per result.
   It should grow with the value the buyer gets and be easy for them to predict.
2. **Anchor.** Write the cost of the problem in the buyer's own numbers (hours times their rate, refunds, lost sales)
   and the price of the alternatives, including what they pay a person to do it. A common heuristic puts the price
   at roughly 10 to 20% of the value delivered; it is a starting point, not a rule.
3. **Bucket.** Decide roughly which bucket the offer lives in: about 10, about 100, or about 1000 a month (or a
   one-off project). Each bucket has its own sales motion; see
   [references/pricing-playbook.md](references/pricing-playbook.md).
4. **Tiers (optional).** Good, better, best. The middle is the one you want sold. Tiers differ by outcome or by how
   much you do for them, not by feature count.
5. **Survey (optional, 30 or more best-fit buyers).** Design and read it with
   [references/surveys.md](references/surveys.md):

   ```bash
   python3 scripts/price_survey.py vw vw-survey.csv
   python3 scripts/price_survey.py gg gg-survey.csv --top-box 1
   ```

6. **Pick one point** and write the reason into `templates/price-sheet.md`. A reason is the anchor, the survey range
   or a real paid result. "Competitors charge X" is context, not a reason.
7. **Test with money.** Pre-orders, a paid pilot, or two prices to two matched groups. Hand this to `validation-plan`.

## Read the symptoms

| You see | It often means | Try |
|---|---|---|
| everyone says yes at once | the price is too low for the value | raise it for the next buyers and watch the close rate |
| interest, then silence at the price | the anchor was never set, or the wrong buyer | show the cost of the problem before the price |
| "too expensive" from best-fit buyers | the value is not proven yet | lower the risk (guarantee, pilot) before the price |
| "too expensive" from poor-fit buyers | normal | do not change the price for them |
| buyers pick the cheapest tier | the middle tier does not differ by outcome | rebuild tiers around results |
| churn after month 2 | the value shows up once | price it as a project, or design the monthly part |

## Rules

- Service before software. Sell the work by hand at a real price first; build a product once the steps repeat.
- One price per offer at a time on the page. A range invites the bottom of it.
- Raising prices: tell existing buyers 60 to 90 days ahead and keep their old price for a stated time (grandfather
  them). New buyers get the new price at once.
- Never discount to fix a weak offer. Fix the lever in `value-stack`.
- Show survey output with its sample size and the words "stated, not paid".
