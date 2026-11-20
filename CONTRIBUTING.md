# Contributing

Useful contributions, roughly in order:

1. **Real outcomes.** A niche that scored SHIP and failed, an idea the reality check sent to TEST that later sold, a smoke test whose verdict was wrong in hindsight. Include the inputs (anonymised) and what happened. This is how the thresholds and weights get better than defaults.
2. **Survey data formats.** If you ran a Van Westendorp or Gabor-Granger survey in a form tool and `price_survey.py` cannot read the export, send the header row and two anonymised lines.
3. **Framework fidelity.** If a summary in `references/` gets Dunford, Hormozi, Fitzpatrick or the Jobs to be Done material wrong, point to the page in the book or the primary source.
4. **Failure modes and angle generators** from other kinds of offers (courses, productized services, B2B software). Each one with a sign and the cheapest test.
5. **Platform reports.** macOS and Linux runs of the checks in [AGENTS.md](AGENTS.md); so far only Windows with Git Bash has been tested.

Before a pull request, run the checks in [AGENTS.md](AGENTS.md). Keep examples on Northwind Ops, Acme and the invented rivals.

Scripts stay on the Python standard library and offline. No tracking, no network calls, no paid services.
