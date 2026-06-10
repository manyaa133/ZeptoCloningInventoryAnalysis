# Zepto Cloning Inventory Analysis

A Zepto-inspired inventory analytics dashboard with:
- FastAPI backend
- React + Vite frontend
- analytics cards, category charts, and stock status

## Backend

1. Open PowerShell in `backend`
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Start the server:
   ```powershell
   uvicorn main:app --reload --port 8000
   ```

Available endpoints:
- `GET /inventory`
- `GET /inventory/stats`
- `GET /inventory/categories`
- `GET /inventory/low-stock`

## Frontend

1. Open PowerShell in `frontend/my-project`
2. Install packages:
   ```powershell
   npm install
   ```
3. Start the dev server:
   ```powershell
   npm run dev
   ```

The frontend uses `VITE_API_URL` from `frontend/my-project/.env`.

## Notes

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:5173`
- CORS is configured for both localhost and 127.0.0.1 origins.
