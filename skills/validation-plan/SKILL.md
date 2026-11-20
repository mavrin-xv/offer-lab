---
name: validation-plan
description: Plans and judges the test that decides whether to build an offer. Picks the cheapest test that asks for a real commitment (Mom Test interviews, a JTBD switch interview, a smoke-test page, a fake-door button, paid pre-orders, a concierge pilot), writes the GO and KILL lines into a decision log before the test starts, sizes the test with a script, and judges the result with a confidence interval so a lucky week does not become a business. Use when someone says "how do I validate this", "test the idea", "smoke test", "landing page test", "interview questions", "is this enough signups", "did the test work", "should I build it now", or has a page and no paying buyers yet.
---

# Validation plan

The test exists to change a decision. So the decision and its lines are written down first, and the test is the
cheapest one that asks the buyer for something they value: time, reputation or money (the Mom Test currencies).

## The ladder (cheapest first)

| Test | Asks for | Good for | Read with |
|---|---|---|---|
| Problem interviews (Mom Test) | 20 minutes | is the pain real, what do they do now | [references/interviews.md](references/interviews.md) |
| Switch interview (JTBD) | 30 minutes, recent buyers of any answer | why people switch, what holds them back | same file |
| Smoke test page | an email or a signup | will strangers raise a hand for this offer | `validation_calc.py` |
| Fake door | a click on a "buy" or "book" button | which option or price they pick | `validation_calc.py` |
| Paid pre-order or deposit | money | will they pay | count against your pre-order line |
| Concierge pilot | money and access | can you deliver, and does it work | the guarantee number |

Methods, gotchas and honesty rules: [references/smoke-tests.md](references/smoke-tests.md).

## Procedure

1. Write the decision: "If GO, we will ___. If KILL, we will ___." Use `templates/decision-log.md`.
2. Pick the cheapest test on the ladder that answers it. Interviews come first if gates 1 and 2 are thin.
3. Write the lines before the test. GO: the rate or count that makes the offer worth building. KILL: the line below
   which you stop. Also what you do if the result is in between (this pack's default: treat it as KILL).
4. Size it:

   ```bash
   python3 scripts/validation_calc.py plan --go 0.05 --kill 0.02 --per-day 60
   ```

5. Run the test without changing the page, price or traffic source halfway. A change starts a new test.
6. Judge it:

   ```bash
   python3 scripts/validation_calc.py judge --visitors 640 --conversions 36 --go 0.05 --kill 0.02
   ```

7. Write the verdict, the numbers and the decision into the log, dated. Update offer card section 7.

## Rules

- Lines first, data second. Lines changed after seeing data mean the test is void; write that in the log.
- Money beats signups. Three paid pre-orders say more than 300 emails.
- Interview for the past, not the future: "the last time this happened" instead of "would you use".
- A fake door tells people the truth right after they click: it is not ready, here is what happens next, nothing
  was charged.
- Rates quoted as "good" in vendor blogs (often 2 to 5% for a landing page) are not studies. Set your lines from what
  the offer has to earn.
- Keep running until the planned sample is reached. Stopping early on a good day finds luck.
