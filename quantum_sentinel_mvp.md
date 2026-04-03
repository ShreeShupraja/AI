# Quantum Sentinel — Portfolio-Ready MVP Blueprint

## 1) Product Vision
**Quantum Sentinel** is an anomaly-detection platform that combines classic machine learning with quantum-inspired ranking to help analysts identify suspicious transactions, clusters, and entity behavior quickly.

### Target Outcome for MVP
- A deployable app where approved users can upload CSV files and get anomaly insights in under 2 minutes.
- An admin console for user approvals and global monitoring.
- A differentiated “AI + Quantum” story that is honest for MVP scope (quantum simulator ranking).

---

## 2) MVP Scope (Buildable in 7 Days)

### In Scope
- Auth + approval workflow (admin and designated user roles)
- CSV upload, schema validation, preprocessing
- Anomaly scoring pipeline (Isolation Forest + optional Autoencoder toggle)
- Quantum-inspired re-ranking (Qiskit simulator)
- Dashboard widgets (risk table, top-10 quantum rank, heatmap/network)
- Export CSV/JSON reports
- Basic gamification badges
- Suggested actions and AI explanations

### Out of Scope (Phase 2)
- Streaming ingestion
- True quantum hardware execution guarantees
- Complex SOC integrations (SIEM/SOAR)
- Multi-tenant billing system

---

## 3) Suggested Architecture

## Frontend (React + TypeScript)
- React + Vite + Tailwind + MUI
- Zustand or Redux Toolkit for state
- Recharts + D3 (network graph)
- React Query for API state

## Backend (FastAPI + Python)
- FastAPI with routers: auth, users, datasets, anomalies, admin, reports
- Celery/Redis or FastAPI BackgroundTasks for analysis jobs
- ML service layer (scikit-learn models)
- Quantum ranking module (Qiskit simulator backend)

## Data Layer
- PostgreSQL + SQLAlchemy + Alembic migrations
- Object storage for uploaded files (S3-compatible; local MinIO for dev)

## Deploy
- Frontend: Vercel
- Backend: Render/Fly.io/AWS ECS
- PostgreSQL: Neon/Supabase/RDS
- Redis: Upstash/Render Redis
- Monitoring: Sentry + UptimeRobot + basic Prometheus metrics endpoint

---

## 4) Feature-Level Functional Spec

## A) Auth and Approval
- `POST /auth/signup` creates pending user (`approved=false`)
- `POST /auth/login` denies if unapproved
- Admin endpoints:
  - `GET /admin/users/pending`
  - `POST /admin/users/{id}/approve`
  - `POST /admin/users/{id}/reject`

## B) Upload Widget
- Drag/drop CSV
- Validation requirements:
  - Required: `transaction_id`, `timestamp`, `amount`
  - Optional: `user_id`, `merchant`, `location`, `device`, `channel`
- Preprocessing:
  - Missing numeric -> median imputation
  - Missing categorical -> `"unknown"`
  - Timestamp features: hour/day/weekend flags
  - One-hot encoding for categorical

## C) Risk Dashboard Widget
- Show paginated anomaly rows:
  - transaction_id, risk_score (0–1), entity fields, status
- Row click opens right-side detail panel:
  - Why suspicious
  - Similar anomaly links
  - Suggested action

## D) Quantum Rank Widget
- Select top-K anomalies by classical score
- Run quantum-inspired ranker on feature correlations
- Display top 10 with confidence and glow intensity

## E) Visualization Widget
- Heatmap by merchant/location/hour
- Network graph: nodes = user/merchant/device, edges = transaction links
- Cluster coloring by community detection (Louvain or label propagation)

## F) AI Explanation Widget
- Template-based explanation (safe default)
- Optional LLM summary mode with guardrails
- Example output:
  - “Transaction 44321 is unusual due to a 3.8x amount spike, unseen merchant pair, and off-hour geolocation shift.”

## G) Gamification
- Badge rules:
  - Fraud Hunter: reviewed ≥ 25 anomalies
  - Quantum Explorer: ran quantum rank ≥ 5 times
  - Cluster Sleuth: opened ≥ 10 cluster views

---

## 5) Data Model (Production-Friendly MVP)

## `users`
- id (uuid pk)
- username (unique)
- email (unique)
- password_hash
- role (`admin` | `user`)
- approved (bool)
- created_at

## `datasets`
- id (uuid pk)
- user_id (fk users)
- filename
- storage_uri
- uploaded_at
- processed (bool)
- row_count
- schema_json

## `analysis_runs`
- id (uuid pk)
- dataset_id (fk datasets)
- model_version
- quantum_enabled (bool)
- status (`queued|running|completed|failed`)
- started_at
- finished_at

## `anomalies`
- id (uuid pk)
- analysis_run_id (fk analysis_runs)
- transaction_id
- risk_score_classical
- risk_score_quantum
- risk_score_final
- reason_for_suspicion
- suggested_action
- cluster_id

## `badges`
- id (uuid pk)
- user_id (fk users)
- badge_name
- awarded_at

## `audit_logs`
- id (uuid pk)
- actor_user_id
- action
- entity_type
- entity_id
- metadata_json
- created_at

---

## 6) API Contract (Starter)

## Auth
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

## Datasets
- `POST /datasets/upload`
- `GET /datasets`
- `GET /datasets/{id}`

## Analysis
- `POST /analysis/{dataset_id}/run`
- `GET /analysis/{run_id}/status`
- `GET /analysis/{run_id}/anomalies`

## Quantum
- `POST /quantum/{run_id}/rerank`
- `GET /quantum/{run_id}/top?limit=10`

## Reports
- `GET /reports/{run_id}.csv`
- `GET /reports/{run_id}.json`

## Admin
- `GET /admin/users/pending`
- `POST /admin/users/{id}/approve`
- `GET /admin/analytics/overview`

---

## 7) Folder Structure

```txt
quantum-sentinel/
  apps/
    web/                         # React frontend
      src/
        pages/
        widgets/
          UploadWidget.tsx
          RiskDashboardWidget.tsx
          QuantumRankWidget.tsx
          VisualizationWidget.tsx
          AIExplanationWidget.tsx
        services/api.ts
        store/
    api/                         # FastAPI backend
      app/
        main.py
        core/
          config.py
          security.py
        db/
          models/
          migrations/
        routers/
          auth.py
          users.py
          datasets.py
          analysis.py
          quantum.py
          admin.py
          reports.py
        services/
          preprocessing.py
          anomaly_detection.py
          quantum_ranking.py
          explanations.py
          badges.py
        schemas/
        tasks/
  infra/
    docker/
      Dockerfile.api
      Dockerfile.web
    docker-compose.yml
  docs/
    architecture.md
    api.md
    runbook.md
```

---

## 8) ML + Quantum Pipeline (MVP Logic)

1. Load dataset and validate schema.
2. Preprocess and feature-engineer.
3. Compute classical anomaly score using Isolation Forest.
4. Select top-N suspicious rows.
5. Build feature-correlation graph and run quantum-inspired ranking (QAOA or amplitude/probability proxy on simulator).
6. Blend scores:
   - `final_score = 0.7 * classical + 0.3 * quantum`
7. Generate explanation + suggested action.
8. Persist results and return dashboard payload.

---

## 9) Security and Compliance Basics
- JWT auth with short-lived access + refresh tokens
- Password hashing with Argon2/Bcrypt
- Row-level ownership checks for datasets/reports
- File scanning + size/type limits on uploads
- Audit logs for admin and sensitive actions
- Secrets via environment variables, never in repo

---

## 10) Deployment Checklist
- [ ] Frontend env vars set (`VITE_API_URL`)
- [ ] Backend env vars set (DB URL, JWT secret, CORS)
- [ ] Alembic migrations applied
- [ ] Redis and worker running
- [ ] Health endpoints passing (`/healthz`, `/readyz`)
- [ ] Admin seed user created
- [ ] Sentry connected
- [ ] Smoke test run on production URL

---

## 11) 7-Day Build Plan (Execution-Ready)

## Day 1
- Bootstrap FastAPI + React repos
- Add auth, role model, and pending approval flow
- Setup PostgreSQL + Alembic

## Day 2
- Implement upload endpoint and preprocessing module
- Build Upload Widget with drag/drop and status toasts

## Day 3
- Implement Isolation Forest pipeline + persistence
- Build Risk Dashboard table + details drawer

## Day 4
- Build heatmap and transaction network graph
- Add report export endpoints

## Day 5
- Implement Qiskit simulator re-ranker
- Build Quantum Rank widget and top-10 view

## Day 6
- Implement AI explanation + suggested action logic
- Add gamification badge engine and user profile badges

## Day 7
- Admin analytics dashboard
- End-to-end QA, deploy frontend/backend, create demo script/video

---

## 12) Portfolio Packaging Tips
- Include architecture diagram and sequence diagram.
- Record a 2–3 minute walkthrough video.
- Publish sample sanitized datasets and benchmark notes.
- Add a “What I’d build next” section showing product thinking.
- Track metrics in README:
  - Mean processing time/dataset
  - Precision@K on labeled sample
  - User actions triggered from suggested actions

---

## 13) Stretch Enhancements (Post-MVP)
- Real-time stream ingestion (Kafka)
- Multi-tenant org/project workspaces
- Human-in-the-loop feedback to retrain model
- LLM-generated analyst reports with citation trails
- Integration hooks for Slack/Jira/SIEM
