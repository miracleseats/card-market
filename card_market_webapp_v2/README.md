# Card Market Web App V2

Expanded UI based on the original Card Market project specification.

Includes a responsive homepage, card search, card profiles, interactive price-history charts, sales history, explainable valuation panels, research dashboard, methodology page, and the existing FastAPI/PostgreSQL backend.

## Run locally
1. Install Node.js, Python, and Docker Desktop.
2. `docker compose up -d db`
3. `cd backend`
4. `python -m venv .venv`
5. Windows: `.venv\\Scripts\\activate`
6. `pip install -r requirements.txt`
7. `python seed.py`
8. `uvicorn app.main:app --reload --port 8000`
9. New terminal: `cd frontend`
10. `npm install`
11. `npm run dev`
12. Open `http://localhost:3000`

All current prices and transactions are clearly demo/seed data. Public launch should connect authorized/licensed marketplace data or owner-supplied data and replace the demo valuation logic with the production methodology.
