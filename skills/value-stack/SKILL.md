---
name: value-stack
description: Builds the offer itself with Alex Hormozi's value equation (dream outcome times perceived likelihood, over time delay times effort): scores the four levers, finds the weakest, maps every buyer objection to a stack item that kills it, writes a named guarantee with a number, a window and a consequence, names the mechanism, and removes any scarcity that is not true. A script checks the stack and compares versions. Use when someone says "make the offer", "what should be in the package", "how do I make this irresistible", "add bonuses", "write a guarantee", "the offer feels weak", "nobody is buying", or has a position and now needs the thing to sell.
---

# Value stack

Buyers judge an offer by four things, from Alex Hormozi's *$100M Offers* (2021): how big the result is (dream
outcome), how sure they are it will happen to them (perceived likelihood), how long it takes (time delay), and what it
costs them in effort and sacrifice. Value goes up when the first two rise or the last two fall. Discounts are not on
the list.

```
value = (dream outcome x perceived likelihood) / (time delay x effort and sacrifice)
```

The pack scores each lever 1 to 10 from the buyer's side (10 for delay and effort means slow and painful). The index is
only for comparing versions of your own offer. It is not a market number.

## Procedure

1. Start from the positioning (offer card section 3). Write the dream outcome in the buyer's words, with a number or
   a date if you can.
2. List the objections: every reason a best-fit buyer would say no. Get them from interviews and lost deals, not
   imagination. Price is one; it is rarely the first.
3. Build the stack with [references/stack-and-guarantees.md](references/stack-and-guarantees.md): for each problem
   the buyer hits before, during and after the result, write a solution item. Then trim. Keep items that kill an
   objection and are cheap for you to deliver compared with their value to the buyer.
4. Write the guarantee: a name, a number (what result), a window (how long) and the consequence (what you do on a
   miss). Do not guarantee what you cannot control.
5. Name the mechanism: the method that produces the result, named so a rival could not say it word for word.
6. Scarcity or urgency only if it is true. Write the real reason (capacity, a cohort start date). If there is none,
   there is no scarcity.
7. Fill `templates/offer-stack.json` and run:

   ```bash
   python3 scripts/value_equation.py offer.json
   python3 scripts/value_equation.py offer-v1.json --compare offer-v2.json
   ```

8. Fix every BLOCK. Pull the weakest lever the script names, then run it again. Write the final stack to offer card
   section 4.

## What the script checks

| Check | Level |
|---|---|
| an objection no item, guarantee or proof kills | BLOCK |
| guarantee missing a number, a window or a consequence | BLOCK |
| scarcity with no reason | BLOCK |
| a stack item that kills no objection | WARN (cut candidate) |
| a stack item costing more than 20% of the price to deliver | WARN |
| unnamed guarantee or mechanism, or one a rival could say | WARN |

## Rules

- Raise likelihood with proof you have: a before and after, a written method, a pilot. Never with invented results.
- Cut delay and effort before adding items. "We do it, you approve it" often beats three bonuses.
- Each item kills an objection. An item that kills nothing makes the stack look padded.
- The guarantee names a consequence you can afford to pay every time it triggers.
- No fake deadlines, countdown timers that reset, or "only 3 left" that is not true. Buyers find out.
- Price comes next, in `price-test`. Do not discount to fix a weak stack; fix the lever.
