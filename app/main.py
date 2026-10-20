"""Login & Authentication Service for AgentOps Target Demo."""

from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="User Authentication Service",
    description="Microservice handling user authentication and token verification",
    version="1.0.0",
)


class LoginRequest(BaseModel):
    username: str
    password: str


# In-memory mock user store
USER_DATABASE: Dict[str, str] = {
    "alice": "correct_horse_battery_staple",
    "bob": "secure_password_123",
}


@app.get("/health")
def health_check():
    """Service health probe."""
    return {"status": "ok", "service": "auth-service"}


@app.post("/login")
def login(request: LoginRequest):
    """
    Authenticate user with username and password.
    
    Returns JWT mock token on success.
    Throws 401 Unauthorized on invalid credentials.
    """
    # BUG: Currently returns 200 OK with error payload instead of raising HTTPException(401)
    if request.username not in USER_DATABASE or USER_DATABASE[request.username] != request.password:
        return {"token": None, "error": "Invalid credentials"}

    return {
        "token": f"jwt_mock_token_for_{request.username}",
        "token_type": "bearer",
        "username": request.username,
    }


@app.get("/users/me")
def get_user_profile(username: str):
    """Retrieve user metadata."""
    if username not in USER_DATABASE:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username, "role": "engineer"}
