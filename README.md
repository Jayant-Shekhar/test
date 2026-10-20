# User Authentication Service (`test`)

A microservice providing authentication and user management APIs, used as a target service for **AgentOps**.

## Architecture & Endpoints

- `GET /health` - Service health status check
- `POST /login` - User authentication (accepts `username`, `password`)
- `GET /users/me` - Profile lookup

## Known Seeded Bug

In `app/main.py`:
- When invalid credentials are submitted to `/login`, the endpoint currently returns HTTP 200 with an error object instead of raising an `HTTPException(status_code=401, detail="Invalid credentials")`.
- Automated test `tests/test_api.py::test_login_invalid_password` catches this failure and expects HTTP 401.

## Running Tests

```bash
pip install -r requirements.txt
pytest
```
