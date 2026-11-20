---
name: idea-reality-check
description: Gives an offer or business idea a GO, TEST, WAIT or KILL verdict from the evidence actually collected, weighting money and commitments over talk and ignoring compliments. Lists the top three ways it fails with a test for each, the real competition including doing nothing, timing, and effort against reward. The default verdict is TEST; GO has to be earned. Use when someone says "is this idea any good", "sanity check this", "should I build this", "reality check", "will this work", "be honest about this idea", or is about to spend weeks building something nobody has paid for.
---

# Idea reality check

The job is to find out what kills the idea before the seller spends weeks on it. The default verdict is TEST.
GO needs money or real commitments. Enthusiasm, compliments and "I would definitely buy" count for nothing, because
they cost the speaker nothing.

## Inputs

- The idea in one sentence: what, for whom, how it is paid for.
- The evidence so far, each item typed (see the ladder below).
- What the seller fears could go wrong.

## The evidence ladder

From the Mom Test (Rob Fitzpatrick): people show they mean it by giving up something they value: time, reputation
or money.

| Type | Example | Weight |
|---|---|---|
| paid | a pre-order, a deposit, a paid pilot | 5 |
| commitment | a booked screen share, an intro to a peer, a letter of intent, access to their data | 3 |
| past_spend | "we pay our bookkeeper about 300 a month, a third of it on this" | 2 |
| conversation | a specific story about the last time it happened | 1 |
| desk | forum threads, reviews, search results you found yourself | 1 |
| compliment | "great idea", "I would use that" | 0 |

## Procedure

1. Write the idea and the evidence into a JSON file (`python3 scripts/reality_check.py --template`).
2. List failure modes. Start from [references/failure-modes.md](references/failure-modes.md); keep the 3 most likely
   for this idea, mark any that would be fatal, and write a test or a fix for each.
3. List the real competition from the buyer's side: other providers, the tool they half use, a person they already
   pay, and doing nothing. Doing nothing is usually the strongest rival.
4. Run it:

   ```bash
   python3 scripts/reality_check.py idea.json
   ```

5. Write the result with `templates/reality-check.md`: verdict, the reasons, the failure modes and their tests,
   competition, timing (why now, or what has to change first), effort in weeks against the reward in plain words.
6. Turn every TEST into a concrete next step for `validation-plan` (who to talk to, what to ask for).

## Verdicts

| Verdict | Means | Next |
|---|---|---|
| GO | 1 paid item or 3 commitments, and the top risks have tests | `positioning-map` |
| TEST | the default: some signal, not enough commitment | `validation-plan`, then run this again |
| WAIT | a blocker outside your control is open | write the trigger that would reopen it |
| KILL | a fatal failure mode with no fix, or 10 conversations and nobody names the pain | stop; write why in the decision log |

## Red flags

These phrases in the idea or the claims push a GO back to TEST until they are removed or backed: "everyone needs
this", "no competition", "zero risk", "guaranteed", "production ready", "huge market". Each one usually hides the
question nobody asked.

## Rules

- Do not argue the seller into or out of the idea. Show the evidence and the verdict it supports.
- No market-size numbers as evidence. They say nothing about this buyer paying this seller.
- If the seller has no evidence at all, the verdict is TEST and the first job is five conversations, not a page.
- Write the verdict even when it is KILL. A dated KILL saves the same idea from coming back next month untested.
