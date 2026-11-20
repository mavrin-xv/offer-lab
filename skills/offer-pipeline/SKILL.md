---
name: offer-pipeline
description: Takes a business idea or a skill someone wants to sell to a priced, tested offer through seven gated stages (niche, reality check, positioning, value stack, price, offer page, validation) and routes each stage to the right skill in this pack. Keeps one offer card so nothing is decided twice. Use when someone says "help me make an offer", "what should I sell", "turn my skill into a product", "I have an idea for a service", "is this offer any good", "take this from idea to launch", or starts any offer, pricing or validation task without naming a stage.
---

# Offer pipeline

One offer, one card, seven gates. The card (`templates/offer-card.md`) is the single place where decisions live.
Every stage reads it first and writes its result back.

The order matters. Most offers fail before the copy: the wrong buyer, a pain nobody pays to fix, or a price picked
after the work was built. So the pack scores the market first, prices before it builds, and asks for money before
anyone writes a line of product.

## Route the request

| The user has or asks for | Go to | Gate |
|---|---|---|
| a skill or an idea, no buyer yet; "which niche", a list of options | `niche-score` | 1 |
| a chosen niche and an idea; "is this worth doing", "sanity check this" | `idea-reality-check` | 2 |
| a GO or TEST idea; "how do I stand out", competitors, "what do we say" | `positioning-map` | 3 |
| a position; "make the offer", "what goes in it", "guarantee", "bonuses" | `value-stack` | 4 |
| an offer; "what should I charge", tiers, a survey, "sales are slow" | `price-test` | 5 |
| a priced offer; "write the page", "sales page outline", a draft page | `offer-page` | 6 |
| a page or an offer; "how do I test this", interviews, a smoke test, results | `validation-plan` | 7 |

If the request skips a stage, check the card for the earlier gate. A missing gate is the first job, unless the user
says it was done elsewhere; then write "done outside", their words and the date into the card.

Validation is not only the last step. Interviews (the stage 7 methods) feed the evidence for stages 1 and 2. The gate
at stage 7 is the paid test: real money, or a signup line written down before the test.

## Gates

Full checklists: [references/gates.md](references/gates.md). In short:

1. **Niche:** `niche_score.py` verdict SHIP (11 of 15 or more after caps) for the chosen niche.
2. **Reality:** `reality_check.py` says GO or TEST, the top 3 failure modes each have a test, and "do nothing" is on
   the competition list.
3. **Positioning:** the 5+1 components are filled from evidence; the lead claim is WHITE SPACE, or CONTESTED with
   proof, in `claim_triage.py`; the angle passes the 7-point gate.
4. **Value stack:** `value_equation.py` exits 0: every objection answered, the guarantee has a number, a window and a
   consequence, no fake scarcity.
5. **Price:** one price point (not a range), a value metric, an anchor, and a reason that is not "competitors charge X".
6. **Page:** `offer_page_lint.py` exits 0 and a human has read it out loud once.
7. **Validation:** thresholds were written into the decision log before the test; `validation_calc.py judge` says GO.

## Procedure

1. Find or create the offer card. Fill in who is selling and what they can deliver today.
2. Ask what the seller can already deliver by hand. Sell that first, as a service, before any software or course.
   A product comes after about ten paid runs of the service, when the steps are known and repeatable.
3. Run the stage the request needs, through its skill. Write the result into the card.
4. Check the gate. If it fails, say which line failed and what evidence would make it pass. Do not move the status on.
5. End every turn with the card status and the single next action.

## Rules

- Evidence over opinion. A compliment is not evidence. Money, time and introductions are.
- One buyer per offer. Two buyers means two cards.
- No invented proof: no made-up testimonials, numbers, logos or "as seen in". If there is no proof yet, the page
  says what you will do and what happens if you fail.
- Scarcity and deadlines only when they are true, with the real reason written down.
- Price before building. If nobody will pay for the description, they will not pay for the finished thing.
- A human approves the niche, the price and the page. The agent proposes.

## Output

At each stop: the card section that changed, the gate result (pass or the failing line), and one next action.
