---
paths:
  - "backend/tests/**/*.py"
---

# Test conventions (backend)

- Use pytest with the `client` fixture from `conftest.py`; no mocking of the database.
- One test file per route module; name tests `test_<behaviour>`.
- Keep tests fast and focused: for API endpoint tests, assert the HTTP status code of each response.
- Use fixed future dates (2030-...) so tests never depend on the current date.
