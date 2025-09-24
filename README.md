## ⚡ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/credit-card-recommender.git
cd credit-card-recommender
```

### 2. Run the backend (Flask)
The backend will initialize the SQLite DB automatically using backend/cards.sql (if present).
```bash
python3 app.py
# Backend listens on http://127.0.0.1:5000 by default
```

### 3. Serve the frontend
Do NOT open index.html via file://. Serve it over HTTP:
```bash
cd frontend
python3 -m http.server 8000
# Open http://127.0.0.1:8000 in your browser
```

### 4. Quick API test
Example curl to exercise the recommend endpoint:
```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"score":720,"age":30,"income":60000}'
```

### Troubleshooting
- If the frontend shows "unable to reach backend", ensure the backend is running on 127.0.0.1:5000 and that you served the frontend over HTTP (not file://).
- Database seed/migration is attempted at backend startup; check backend logs for errors.
- To change ports, update the app.run() call in backend/app.py and the frontend fetch URLs in frontend/index.html.
