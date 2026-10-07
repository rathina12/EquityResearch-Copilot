# Contributing

Contributions are welcome across valuation logic, research workflows, APIs, tests, and documentation.

## Setup
Create a Python environment, install `requirements.txt`, then run `pytest`.

## Engineering guidance
Financial calculations should be deterministic and explainable. Validate invalid inputs explicitly, avoid silently inventing market data, and keep assumptions visible in returned results or documentation.

## Pull request checklist
- [ ] `pytest` passes.
- [ ] New valuation behavior has tests.
- [ ] Boundary and invalid-input cases are covered.
- [ ] External data assumptions are documented.
- [ ] No API keys, credentials, or private financial data are committed.
