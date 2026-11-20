# Price surveys: Van Westendorp and Gabor-Granger

Both measure stated willingness to pay. Use them to find a range and a likely peak, then test with money.

## Who to ask

30 or more people who match the best-fit buyer. Fewer gives curves that jump around. Friends and followers who
would never buy distort the answers in both directions.

Describe the offer the same way to everyone: the outcome, what is included, the guarantee. A price question about
an offer they do not understand measures confusion.

## Van Westendorp (four questions)

At what price would this offer be:

1. so cheap you would doubt the quality? (too_cheap)
2. a bargain, a great buy for the money? (cheap)
3. getting expensive, but you would still consider it? (expensive)
4. so expensive you would not consider it? (too_expensive)

CSV: `respondent,too_cheap,cheap,expensive,too_expensive`. The script drops rows where the four answers do not rise
in order and says how many it dropped.

Reading it: the acceptable range runs from PMC to PME. OPP is the price where the fewest people reject it as too cheap
or too expensive; it is not the revenue peak. Published guides use different intersection conventions and get
different numbers from the same data. The script uses the one Wikipedia describes and says so.

## Gabor-Granger (would you buy at this price?)

Show each person several prices (in a random order) and ask yes or no, or a 1 to 5 likelihood. CSV:
`respondent,price,answer`.

The script prints the share buying at each price and a revenue index (price times share). On a 1 to 5 scale, count
only 5 as a yes by default; people who say 4 buy far less often than they say. Use `--top-box 2` to see the
optimistic view.

## Then

- If the Gabor-Granger peak is inside the Van Westendorp range, test that point and one step above it.
- If your chosen price is above the peak, keep it only if the guarantee and proof are strong, and test it against
  the peak with real money.
- Write the sample size and "stated, not paid" next to any number you quote.
