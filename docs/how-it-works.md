# How it works

offer-lab is eight skills and seven small scripts. The skills tell an agent what to ask, what to collect and when a
stage is done. The scripts check the parts a person tends to fudge: whether a score has evidence, whether an
objection has an answer, whether a test result is luck.

## The offer card

Every offer gets one card (`skills/offer-pipeline/templates/offer-card.md`). Each stage reads it, does its work and
writes its section back. The card carries a status field, so an agent picking up the work later knows where it
stopped and which gate is open.

One buyer per card. If the niche splits into two buyers, that is two cards, because the positioning, the stack and
the price will differ.

## Seven gates

| Stage | Skill | Gate passes when |
|---|---|---|
| 1 Niche | `niche-score` | SHIP after evidence caps |
| 2 Reality | `idea-reality-check` | GO or TEST, top 3 failure modes have tests |
| 3 Positioning | `positioning-map` | lead claim is white space or proven, angle passes 7 lines |
| 4 Value stack | `value-stack` | `value_equation.py` exits 0 |
| 5 Price | `price-test` | one price point with a value metric, an anchor and a reason |
| 6 Page | `offer-page` | `offer_page_lint.py` exits 0, read out loud once |
| 7 Validation | `validation-plan` | lines written first, `validation_calc.py judge` says GO |

The full checklists are in `skills/offer-pipeline/references/gates.md`.

## Why evidence caps

People score their own ideas high. The pack does not argue with the score; it asks for the evidence and lowers the
score when the evidence is missing. A Channel of 5 with no query written down becomes 2. A Pain of 5 with no quote in
the buyer's words becomes 3. The reality check weights a paid pre-order at 5 and a compliment at 0, following the Mom
Test idea that only commitments (time, reputation, money) count.

## Why lines before data

A test read after the fact can be made to say anything: a 4.5% rate looks fine if you wanted to build and weak if you
did not. So `validation_calc.py plan` sizes the test from GO and KILL lines written down first, and `judge` compares
the result's 95% interval with those lines. A result between the lines is UNCLEAR, and the default rule treats it as
KILL.

## Exit codes

Every script exits non-zero when something blocks, so an agent (or a CI job) can stop on it:

| Script | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `niche_score.py`, `icp_traits.py`, `claim_triage.py`, `price_survey.py` | ran | | bad input | |
| `reality_check.py` | GO or TEST | KILL or WAIT | bad input | |
| `value_equation.py` | no blockers | blocker | bad input | |
| `offer_page_lint.py` | no blockers | blocker | bad input | |
| `validation_calc.py judge` | GO | KILL or UNCLEAR | bad input | KEEP RUNNING |

## What stays with the human

The agent proposes; a person approves the niche, the price and the page, and sends the traffic. The pack does not
post, email, buy ads or take payments.
