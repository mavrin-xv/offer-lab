# Evidence mode: a buyer profile from won and lost deals

Use this once you have sold something. It replaces guesses about the ideal customer with traits that actually showed
up more often in the deals you won.

## What you need

- 10 or more won deals and 10 or more lost deals. Fewer works, but the script says the profile is weak.
- For each deal, the traits you knew before the outcome: size, channels, who runs operations, what they already pay
  for, what triggered the first call. Traits you learned after the deal closed leak the answer; leave them out.
- Rows in time order, oldest first. The newest deals are held out.

Format (`examples/data/deals.csv`):

```
deal,outcome,traits
D01,won,200+ skus; founder runs ops; pays a bookkeeper
D02,lost,under 50 skus; single channel; price shopper
```

## Steps

1. Hold out the newest 5 won and 5 lost deals. Do not look at them yet.
2. Run the script on the rest:

   ```bash
   python3 scripts/icp_traits.py deals.csv
   ```

3. Fit traits: at least 2x more common in won deals and present in at least 30% of them.
4. Disqualifiers: at least 2x more common in lost deals, present in at least 30% of them, and in under 30% of won.
   Keep 3 to 5. A long disqualifier list turns good buyers away.
5. The script scores the held-out deals. If it gets 6 or fewer of 10 right, the profile is not better than a guess.
   Collect more deals or better traits before you use it.
6. Write the profile in one sentence ("founder-run shops on two or more channels with 200+ SKUs that already pay a
   bookkeeper") and the disqualifiers as a list sales can check on the first call.

## Traps

- Survivorship: if you only recorded traits for won deals, the lost rows are empty and everything looks like a fit.
- Small numbers: a trait in 2 of 3 won deals is 67%, and it means nothing.
- Shared traits: a trait common in both groups ("uses spreadsheets") is not a signal either way.
