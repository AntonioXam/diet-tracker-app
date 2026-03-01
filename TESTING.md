# Testing System for Diet Tracker

This project includes a comprehensive testing suite covering:

- **Unit tests** for utility functions (TMB calculation, deficit calculation, etc.)
- **Integration tests** for Flask API endpoints (using mocked Supabase)
- **End-to-end (E2E) tests** for frontend interactions (using Playwright)

## Prerequisites

- Python 3.9+
- Node.js (optional, only needed if you want to run frontend dev server)
- Pip (Python package manager)

## Installation

### Backend (API) Testing

1. Navigate to the `api` directory:

   ```bash
   cd diet-tracker-app/api
   ```

2. Install Python dependencies (including testing libraries):

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install Playwright browsers:

   ```bash
   python -m playwright install
   ```

## Running Tests

### Unit and Integration Tests

From the `api` directory, run:

```bash
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

Or run all backend tests at once:

```bash
python -m pytest tests/ -v
```

### End-to-End Tests

Ensure the frontend is built (the `frontend/index.html` file exists). Then run:

```bash
python -m pytest tests/e2e/ -v
```

To run E2E tests with a specific browser:

```bash
python -m pytest tests/e2e/ --browser chromium
```

### Coverage Report

Generate a coverage report for backend code:

```bash
python -m pytest --cov=app tests/ --cov-report=html
```

Open `htmlcov/index.html` in your browser.

## Test Structure

- `tests/unit/` – Unit tests for pure functions (no side‑effects)
- `tests/integration/` – Integration tests for Flask routes (mocked external services)
- `tests/e2e/` – End‑to‑end tests that simulate user interaction with the frontend

## Mocking Supabase

All integration tests mock the Supabase client using `pytest-mock`. The fixture `mock_supabase` in `tests/conftest.py` ensures that no real network calls are made.

If you add new endpoints that interact with Supabase, you should mock the appropriate table calls in your integration tests.

## Writing New Tests

### Unit Tests

Create a file `tests/unit/test_*.py`. Import the function you want to test from `app`. Use standard `assert` statements.

Example:

```python
from app import hash_password

def test_hash_password():
    assert hash_password('secret') == '...'
```

### Integration Tests

Create a file `tests/integration/test_*.py`. Use the `client` fixture (Flask test client) and `mock_supabase` fixture to mock database operations.

Example:

```python
def test_login(client, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [...]
    response = client.post('/api/login', json={'username': 'test'})
    assert response.status_code == 200
```

### E2E Tests

Create a file `tests/e2e/test_*.py`. Use Playwright's `page` fixture and `expect` assertions. Mock network requests with `page.route()` to avoid depending on a live backend.

Example:

```python
def test_modal_opens(page, frontend_url):
    page.goto(frontend_url)
    page.click('button:has-text("Registrarse")')
    expect(page.locator('#modal-register')).to_be_visible()
```

## Continuous Integration (CI)

To integrate this test suite into a CI pipeline (GitHub Actions, GitLab CI, etc.), ensure you:

1. Install Python dependencies.
2. Install Playwright browsers (`playwright install`).
3. Run the test commands above.

Example GitHub Actions workflow snippet:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r api/requirements-dev.txt
      - run: python -m playwright install
      - run: python -m pytest api/tests/ -v
```

## Troubleshooting

- **Playwright browsers not installed**: Run `python -m playwright install` with the appropriate browser flag (`--chromium`, `--firefox`, etc.).
- **Import errors**: Make sure you are running tests from the `api` directory, or that your `PYTHONPATH` includes the `api` folder.
- **Supabase connection errors in integration tests**: Check that `mock_supabase` fixture is being used and that all table calls are properly mocked.

## Coverage Goals

The current test suite aims to cover:

- All utility functions (100%)
- All API endpoints (happy path and error conditions)
- Critical user journeys (registration, login, plan viewing)

Run `pytest --cov=app` to see the current coverage percentage.