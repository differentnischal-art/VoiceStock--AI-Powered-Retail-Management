# Samita Retail MVP

## Architecture

- FastAPI is the source of truth for products, stock, checkout, transactions, and daily reports.
- SQLite + SQLAlchemy provides a zero-setup local database.
- The browser dashboard provides inventory search, cart operations, checkout, low-stock visibility, and daily metrics.
- Browser speech recognition sends transcript text to `/api/voice/parse`; voice never writes directly to the database and uses the same cart/checkout path.

## Run

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and say **“Add 5 chocolates”**. Ambiguous matches are presented for selection.

## MVP API

`GET/POST/PUT/DELETE /api/products`, `POST /api/checkout`, `GET /api/transactions`, `GET /api/reports/daily`, and `GET /api/voice/parse?text=...`.
