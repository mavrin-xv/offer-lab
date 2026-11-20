---
name: offer-page
description: Turns a finished offer card into a one-page sales outline (hero, problem, mechanism, stack, proof, guarantee, price with anchor, objection FAQ, one call to action) and lints the draft for the mistakes that cost trust; placeholders left in, fake scarcity, a guarantee with no number or window, a missing price, hype words, a hero with no outcome, more "we" than "you", several calls to action and testimonials without permission. Use when someone says "write the sales page", "offer page", "landing page outline", "check my sales page", "what goes on the page", "review this page before I publish", or has a priced offer and needs a page to test it.
---

# Offer page

The page is the offer written down for a buyer who is not on a call. It is built from the card, section by section,
so it says nothing the card does not support. Writing starts only after the price is set.

## The outline

Use `templates/offer-page.md`. Each section takes its content from one place on the offer card.

| Section | Job | From the card |
|---|---|---|
| Hero (H1 and one line) | the outcome, for whom, how soon; 25 words or fewer, with a number | angle, dream outcome, time delay |
| Problem | the pain in the buyer's words and what it costs them | pain quote, anchor |
| How it works | the named mechanism in 3 or 4 steps | mechanism |
| What you get | the stack, each item next to the objection it answers | stack |
| Proof | what you can show: before and after, a pilot, the method | likelihood proof |
| Guarantee | name, number, window, consequence | guarantee |
| Price | one price, the anchor next to it, what happens after they pay | price sheet |
| Questions | the top objections as questions, answered plainly | objections |
| Call to action | one action, the same words everywhere it appears | |

## Procedure

1. Check the card: gates 1 to 5 passed. If not, send the user back to the missing stage.
2. Fill the template from the card. Use the buyer's words from interviews wherever you can.
3. Mark every scarcity or deadline line with an HTML comment that states the real limit:
   `<!-- scarcity: two people, each count takes a full day -->`. No reason means delete the line.
4. Mark every testimonial with "(permission: yes)" once the person agreed in writing. No proof yet? Say what you will
   do and what happens if you miss. Never invent a quote.
5. Lint:

   ```bash
   python3 scripts/offer_page_lint.py page.md
   ```

6. Fix every BLOCK, then the WARNs that matter. Read the page out loud once. Rewrite any line you stumble on.
7. Write the path and the lint result into offer card section 6. Then `validation-plan`.

## Rules

- One buyer, one outcome, one call to action.
- The hero says what the buyer gets, not what you are. "We are a team of experts" is not a hero.
- Price on the page. Hiding it behind a call filters out the buyers who would have bought.
- The guarantee wording on the page matches the card exactly.
- No hype words. Specific numbers and the buyer's own words do the work.
- No logos, "as seen in", review counts or results you cannot show the source for.
