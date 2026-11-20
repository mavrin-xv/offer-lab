# Smoke tests, fake doors and pre-orders

## Smoke test page

A page that describes the offer as if it exists, with one call to action that records interest (an email, a booked
call, a signup). Build it with `offer-page` so the page matches the offer you would deliver.

- Send best-fit traffic: the channel from the niche card, not friends. Mixed traffic gives a rate that means nothing.
- Keep one variable per test. Changing the headline and the price together tells you nothing about either.
- Count visitors as unique people who saw the offer, not page loads.

## Fake door

A button for an option that does not exist yet ("Book the monthly plan"). It measures which option or price people
pick. After the click, show the truth at once: it is not ready, what happens next, nothing was charged. Never collect
payment details on a fake door.

## Pre-orders and deposits

The strongest test short of delivery. Take money for a stated start date, with a full refund if you do not start. A
few pre-orders from best-fit buyers outweigh any signup rate. Set the pre-order line in advance too.

## Concierge pilot

Deliver the result by hand for 1 to 3 paying buyers. It tests delivery, the guarantee number and the hours it takes,
which sets the capacity line used for honest scarcity.

## Setting lines

- GO: what rate or count makes the offer worth building, worked back from what it must earn. Example: "5% of
  best-fit visitors sign up, or 3 paid pre-orders".
- KILL: the rate at which you stop. Example: 2%.
- In between: decide now. This pack's default treats UNCLEAR as KILL, so a weak result is not kept alive by hope.

Published benchmark rates come from vendor blogs and vary widely (2 to 5% is often quoted for landing pages). They are
not research findings. Use them only as a sanity check.

## Reading results

`validation_calc.py judge` reports the rate with a Wilson 95% interval. Small samples have wide intervals: 6 signups
from 100 visitors is somewhere between about 3% and 13%. That is why the plan sets the sample size first.
