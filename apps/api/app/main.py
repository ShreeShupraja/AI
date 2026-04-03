from datetime import datetime
from typing import Literal

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Quantum Sentinel API", version="0.2.0")

ADMIN_TOKEN = "dev-admin-token"


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Literal["admin", "user"]
    approved: bool


class AnalysisRunRequest(BaseModel):
    dataset_name: str
    quantum_enabled: bool = True


class AnalysisRunResponse(BaseModel):
    run_id: str
    status: Literal["queued", "completed"]
    anomalies_found: int


USERS: dict[int, dict[str, object]] = {
    1: {
        "id": 1,
        "username": "admin",
        "email": "admin@quantumsentinel.dev",
        "password": "admin123",
        "role": "admin",
        "approved": True,
    }
}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "quantum-sentinel-api"}


@app.post("/auth/signup", response_model=UserOut)
def signup(payload: SignupRequest) -> UserOut:
    existing = [u for u in USERS.values() if u["email"] == payload.email]
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    next_id = max(USERS.keys()) + 1
    user = {
        "id": next_id,
        "username": payload.username,
        "email": str(payload.email),
        "password": payload.password,
        "role": "user",
        "approved": False,
    }
    USERS[next_id] = user

    return UserOut(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        approved=user["approved"],
    )


@app.post("/auth/login")
def login(payload: LoginRequest) -> dict[str, str]:
    user = next((u for u in USERS.values() if u["email"] == payload.email), None)
    if user is None or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user["approved"]:
        raise HTTPException(status_code=403, detail="Awaiting admin approval")

    return {
        "access_token": f"dev-token-user-{user['id']}",
        "token_type": "bearer",
        "role": str(user["role"]),
    }


@app.get("/admin/users/pending", response_model=list[UserOut])
def pending_users(x_admin_token: str = Header(default="")) -> list[UserOut]:
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    pending = [u for u in USERS.values() if not u["approved"]]
    return [
        UserOut(
            id=u["id"],
            username=u["username"],
            email=u["email"],
            role=u["role"],
            approved=u["approved"],
        )
        for u in pending
    ]


@app.post("/admin/users/{user_id}/approve", response_model=UserOut)
def approve_user(user_id: int, x_admin_token: str = Header(default="")) -> UserOut:
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["approved"] = True
    return UserOut(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        role=user["role"],
        approved=user["approved"],
    )


@app.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)) -> dict[str, str | int]:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    row_count = max(content.count(b"\n") - 1, 0)

    return {
        "filename": file.filename,
        "rows_detected": row_count,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
        "status": "accepted",
    }


@app.post("/analysis/run", response_model=AnalysisRunResponse)
def run_analysis(payload: AnalysisRunRequest) -> AnalysisRunResponse:
    return AnalysisRunResponse(
        run_id=f"run-{int(datetime.utcnow().timestamp())}",
        status="completed",
        anomalies_found=7 if payload.quantum_enabled else 5,
    )
