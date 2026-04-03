# Quantum Sentinel — Deployable MVP Scaffold

This repository includes a deployable full-stack starter for Quantum Sentinel:

- `apps/api`: FastAPI backend with auth approval flow stubs, CSV upload, and analysis run endpoint
- `apps/web`: React + Vite frontend starter
- `docker-compose.yml`: local full-stack startup
- `render.yaml`: cloud deployment blueprint
- `quantum_sentinel_mvp.md`: complete product blueprint

## Quick Start (Docker)

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Web: `http://localhost:5173`

## Quick Start (Local Dev)

## API
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r apps/api/requirements.txt
uvicorn app.main:app --app-dir apps/api --reload --host 0.0.0.0 --port 8000
```

## Web
```bash
cd apps/web
npm install
npm run dev
```

If needed:
```bash
export VITE_API_BASE_URL=http://localhost:8000
```

## API Endpoints (Current Scaffold)

- `GET /healthz`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /admin/users/pending` (requires `x-admin-token: dev-admin-token`)
- `POST /admin/users/{user_id}/approve` (requires `x-admin-token: dev-admin-token`)
- `POST /datasets/upload` (CSV only)
- `POST /analysis/run`

## Run Backend Tests

```bash
pip install -r apps/api/requirements.txt
pytest apps/api/tests -q
```

## Deploy Online (Render)

1. Push repo to GitHub.
2. In Render, create a Blueprint project using this repo.
3. Render reads `render.yaml` and provisions backend + frontend services.
4. Set `VITE_API_BASE_URL` to your backend public URL.

## Notes

- This is a functional starter and deployment scaffold.
- For production: replace in-memory users with PostgreSQL, secure secrets, and JWT/session handling.
