# API & Microservices Test Harness

A lightweight backend/API test automation framework for **contract validation, regression testing, and API quality assurance** of REST services, demonstrated against the public [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) API.

---

## Live Test Execution Report

### [View the Latest Allure Test Report](https://rajivkumarinfo.github.io/python-api-automation-framework/)

**Interactive HTML report of the latest automated test execution.**

The Allure report provides visibility into test results, failures, execution times, tracebacks, and contract/schema validation results.

**Report includes:**

* Passed, failed, and skipped tests
* Test execution statistics
* Individual test details
* Execution duration
* Failure information and tracebacks
* Contract and schema validation results

---

## Highlights

* **Custom API Client** — Centralized HTTP communication, authentication, logging, and retry handling.
* **Contract & Schema Validation** — JSON Schema validation to detect breaking API changes early.
* **Fixtures & Parametrization** — Reusable fixtures and data-driven tests with minimal code duplication.
* **Resilience & Retries** — Transport-level retries and flaky-test retries handled separately.
* **Parallel Execution** — Tests can run across multiple workers using `pytest-xdist`.
* **Allure Reporting** — Interactive HTML reports with execution details, failures, tracebacks, and test statistics.
* **CI/CD Integration** — GitHub Actions for automated test execution and build gating.

---

## Tech Stack

| Concern            | Tool                     |
| ------------------ | ------------------------ |
| Test runner        | PyTest                   |
| HTTP client        | Requests wrapper         |
| Contract checks    | JSON Schema              |
| Reporting          | Allure                   |
| Resilience         | urllib3 Retry + Tenacity |
| Test data          | Faker + JSON fixtures    |
| Parallel execution | pytest-xdist             |
| CI/CD              | GitHub Actions           |

---

## Project Layout

```text
.
├── src/                 # API client, schemas, and utilities
├── tests/               # Fixtures, test data, and test cases
├── .github/             # GitHub Actions workflows
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Setup

### Prerequisites

* Python 3.10+
* pip
* Allure Commandline — required only for generating and viewing reports locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows — Command Prompt**

```cmd
.venv\Scripts\activate
```

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running Tests

### Full Test Suite

Run the complete test suite using four parallel workers:

```bash
pytest -n 4 -v --tb=long
```

* `-n 4` — Run tests using four parallel workers
* `-v` — Enable verbose output
* `--tb=long` — Display detailed tracebacks

### Smoke Tests

Run only the critical smoke tests:

```bash
pytest -m smoke -v --tb=short
```

### Contract / Schema Tests

Run contract and schema validation tests using four parallel workers:

```bash
pytest -m contract -n 4 -v --tb=long
```

---

## Allure Reporting

Allure is used to generate an interactive HTML report from the automated test execution.

### Generate Allure Results

Run the tests and store the raw results in the `allure-results` directory:

```bash
pytest --alluredir=allure-results
```

> This command generates the raw Allure results. It does not generate the HTML report itself.

### View the Allure Report Locally

Generate and open the interactive report in your browser:

```bash
allure serve allure-results
```

### Generate a Static Report

To generate a report in the `allure-report` directory:

```bash
allure generate allure-results -o allure-report --clean
```

---

## CI/CD

The project is integrated with **GitHub Actions** for automated test execution.

The CI pipeline can:

1. Install project dependencies
2. Execute the API test suite
3. Run tests in parallel
4. Generate Allure test results
5. Publish the Allure HTML report
6. Apply configured quality gates

---

## Test Execution Flow

```text
Test Cases
    │
    ▼
PyTest
    │
    ├── Smoke Tests
    ├── Regression Tests
    └── Contract / Schema Tests
    │
    ▼
API Client
    │
    ├── Authentication
    ├── Logging
    └── Retry Handling
    │
    ▼
Test Results
    │
    ▼
Allure Results
    │
    ▼
Allure HTML Report
    │
    ▼
GitHub Pages
```

---

## Example Commands

```bash
# Full test suite
pytest -n 4 -v --tb=long

# Smoke tests
pytest -m smoke -v --tb=short

# Contract / schema tests
pytest -m contract -n 4 -v --tb=long

# Generate Allure results
pytest --alluredir=allure-results

# Generate and serve Allure report
allure serve allure-results
```

---

## API Under Test

This framework is demonstrated against the public **Restful-Booker** API.

API documentation:

[Restful-Booker API Documentation](https://restful-booker.herokuapp.com/apidoc/index.html)

---

## Live Report

### [View the Latest Allure Test Report](https://rajivkumarinfo.github.io/python-api-automation-framework/)

The published report contains the results of the latest automated test execution.
