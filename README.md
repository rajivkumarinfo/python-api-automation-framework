# API & Microservices Test Harness

[![API Tests](https://github.com/rajivkumarinfo/python-api-automation-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/rajivkumarinfo/python-api-automation-framework/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10-blue)

A lightweight **Python** backend/API test automation framework for **contract validation, regression testing, and API quality assurance** of REST services, demonstrated against the public [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) API.

**Live Allure report:** https://rajivkumarinfo.github.io/python-api-automation-framework/

## Highlights

- **Centralized API client** - handles auth, logging and retries in one place
- **Contract testing** - JSON Schema validation catches breaking API changes
- **Reusable fixtures and parametrized tests** - less duplication, easier maintenance
- **Resilience** - transport-level retries (urllib3 Retry, Tenacity) kept separate from flaky-test reruns (pytest-rerunfailures)
- **Parallel execution** - pytest-xdist
- **Test data** - Faker plus JSON fixtures
- **Reporting** - Allure, published to GitHub Pages from CI
- **CI/CD** - GitHub Actions on every push and pull request to `main`

## Tech stack

Python · Pytest · Requests · JSON Schema · Allure · pytest-xdist · Faker · Tenacity · GitHub Actions

## Project structure

```text
.
├── src/
│   ├── client/
│   │   ├── base_client.py       # HTTP session, logging, retries
│   │   └── booking_client.py    # Restful-Booker endpoint methods
│   ├── schemas/
│   │   └── booking_schema.py    # JSON Schemas for contract validation
│   ├── utils/
│   │   ├── retry.py             # retry helper (Tenacity)
│   │   └── schema_validator.py  # schema validation helper
│   └── config.py                # environment-driven settings
├── tests/
│   ├── data/
│   │   └── booking_payloads.json  # test data
│   ├── conftest.py    # shared fixtures
│   ├── test_ping.py
│   ├── test_auth.py
│   ├── test_booking_crud.py
│   └── test_booking_contract.py
├── .github/workflows/ # CI pipeline
├── pytest.ini
└── requirements.txt
```

## Getting started

Requires **Python 3.10** (the version used in CI).

```bash
git clone https://github.com/rajivkumarinfo/python-api-automation-framework.git
cd python-api-automation-framework

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

The Allure command-line tool is only needed if you want to generate the HTML report locally.

## Running the tests

```bash
# Full suite, in parallel
pytest -n 4 -v --tb=long

# Smoke tests
pytest -m smoke -v --tb=short

# Contract / schema tests
pytest -m contract -n 4 -v --tb=long
```

Available markers (defined in `pytest.ini`): `smoke`, `crud`, `contract`, `regression`, `flaky`. Failed tests are rerun once automatically (`--reruns 1`).

## Reporting

```bash
# Generate Allure results
pytest --alluredir=allure-results

# View the report locally
allure serve allure-results
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on pushes and pull requests to `main`, and can also be started manually. It:

1. Installs dependencies on Python 3.10
2. Runs the suite in parallel with coverage reporting
3. Generates Allure results, restoring previous history for trend charts
4. Builds the Allure HTML report and publishes it to GitHub Pages

## About

Built to demonstrate how I design API test automation: a layered client, contract-driven checks and CI-published reporting. It runs against a public API only.
