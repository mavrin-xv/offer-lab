# AGENTS.md

Notes for coding agents (Claude Code, Codex, Cursor, others) working on this repository.

## What this is

Eight Agent Skills that take an idea from niche choice to a judged validation test. The product is the `SKILL.md` text plus small stdlib Python scripts. There is no server, no database and no network access.

## Layout

- `skills/<name>/SKILL.md`: what the agent does and when. Frontmatter has `name` (same as the folder) and `description` only. Keep each under 500 lines; long material goes in `references/`.
- `skills/<name>/scripts/*.py`: Python 3.8+, standard library only, each with `--help` and documented exit codes. `offer-pipeline` is a router and has no script.
- `skills/<name>/templates/`: files the agent copies and fills (offer card, niche sheet, reality check, competitor pack, positioning, offer stack JSON, price sheet, offer page, decision log, interview guide).
- `examples/data/`: an invented two-person studio (Northwind Ops), its niches, deals, idea, rivals (Stockwise, Countly Sync, Acme Bookkeeping, doing nothing), two offer versions and two surveys.
- `examples/offer-page-draft.md` and `examples/data/offer-v1.json`: problems planted on purpose (placeholder, fake scarcity, vague guarantee, hype words, two calls to action, unanswered objections). Do not fix them. `examples/data/vw-survey.csv` has two inconsistent rows on purpose (R07, R23).

## Rules

- No invented proof in templates or examples presented as real. Everything in `examples/` is labelled invented.
- No real companies, people or brands in examples. Use Northwind, Acme and the invented rivals.
- Survey output always carries "stated, not paid".
- Thresholds and weights are defaults; if you change one, say so in the script's help and in the README Configure table.

## Checks before you finish

```bash
E=examples/data
S=skills
for f in $S/*/scripts/*.py; do python3 "$f" --help >/dev/null || echo "FAIL $f"; done
python3 $S/niche-score/scripts/niche_score.py $E/niches.csv                        # 2 SHIP, 3 ITERATE, 1 cap (dental pain 4->3)
python3 $S/niche-score/scripts/icp_traits.py $E/deals.csv                          # 5 fit, 5 disqualifiers, holdout 9/10
python3 $S/idea-reality-check/scripts/reality_check.py $E/idea.json                # TEST, evidence score 13, exit 0
python3 $S/positioning-map/scripts/claim_triage.py $E/competitors --ours $E/our-claims.md   # never-oversell SATURATED, counts-drift WHITE SPACE at 4 rivals, 1 unsourced
python3 $S/value-stack/scripts/value_equation.py $E/offer-v1.json --compare $E/offer.json  # 0.67 -> 9.33, blockers 5 -> 0, exit 0
python3 $S/value-stack/scripts/value_equation.py $E/offer-v1.json; echo $?          # 5 BLOCK, exit 1
python3 $S/price-test/scripts/price_survey.py vw $E/vw-survey.csv                  # 2 dropped, range 230 to 570, OPP 250, IPP 350
python3 $S/price-test/scripts/price_survey.py gg $E/gg-survey.csv                  # highest revenue index at 350
python3 $S/offer-page/scripts/offer_page_lint.py examples/offer-page-draft.md; echo $?   # 4 BLOCK, 8 WARN, exit 1
python3 $S/offer-page/scripts/offer_page_lint.py examples/offer-page.md; echo $?         # 0 BLOCK, 0 WARN, exit 0
python3 $S/validation-plan/scripts/validation_calc.py plan --go 0.05 --kill 0.02 --per-day 60   # 191 visitors, 4 days
python3 $S/validation-plan/scripts/validation_calc.py judge --visitors 640 --conversions 29 --go 0.05 --kill 0.02; echo $?   # UNCLEAR, exit 1
bash -n install.sh
```

If you change a rule or a weight, update the expected results here and the outputs in `examples/walkthrough.md` and the README quick start.
