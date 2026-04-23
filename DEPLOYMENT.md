# Deployment Guide

This project is set up for:

- Backend: FastAPI on Render
- Frontend: Streamlit Community Cloud

## 1. Prepare GitHub

Push this repository to GitHub. Do not commit `.env` or `.streamlit/secrets.toml`; both are ignored by `.gitignore`.

If a real API key was ever committed or pasted into a shared place, rotate it before deployment.

## 2. Deploy Backend On Render

This repository includes `render.yaml`, so the easiest path is Render Blueprint deployment.

1. Open Render and create a new Blueprint from this GitHub repo.
2. Render will use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Health check: `/health`
3. When Render asks for secret values, set:
   - `GEMINI_API_KEY`: your Gemini key
4. Keep:
   - `GEMINI_MODEL=gemini-2.5-flash`
   - `PYTHON_VERSION=3.11.11`
5. After deployment, verify:
   - `https://your-render-service-name.onrender.com/health`
   - `https://your-render-service-name.onrender.com/docs`

## 3. Deploy Frontend On Streamlit Cloud

1. Open Streamlit Community Cloud and create a new app from this GitHub repo.
2. Set the entrypoint file to:
   - `frontend/streamlit_app.py`
3. Keep the root directory unset.
4. In Secrets, add:

```toml
BACKEND_API_URL = "https://your-render-service-name.onrender.com"
```

Do not include a trailing slash.

## 4. Deploy Frontend On Render

If you deploy the Streamlit frontend on Render instead of Streamlit Cloud, create a separate Web Service with:

- Root directory: `frontend`
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT`

Environment variables:

```env
BACKEND_API_URL=https://hsbc-ominiaidatafabric.onrender.com
PYTHON_VERSION=3.11.11
```

For this POC, project history is saved through the backend API into the backend
service's local `project_repository/history.json` file.

## 5. Local Development

Start the backend locally:

```bash
uvicorn api:app --reload
```

Then start the frontend:

```bash
streamlit run streamlit_app.py
```

The frontend defaults to `http://127.0.0.1:8000` when `BACKEND_API_URL` is not set.

## 6. Important Notes

- Render free services can sleep when idle, so the first frontend request may be slow.
- Render free services use an ephemeral filesystem. The POC history API saves to backend-local JSON, so history can still reset if the backend service redeploys or restarts.
- The Streamlit app calls the backend server-side with Python `requests`, so browser CORS is not needed for the current frontend flow.
- Keep all real credentials in Render environment variables or Streamlit secrets.
- Streamlit Cloud should use `frontend/streamlit_app.py` as the app file. That lets it install only `frontend/requirements.txt` instead of the backend dependencies in the root `requirements.txt`.
- If Render logs show `Using Python version 3.14.3 (default)` and `pydantic-core` fails to build, the Python pin was not applied. Confirm `.python-version` is pushed to GitHub or set `PYTHON_VERSION=3.11.11` in the Render service environment variables, then clear the build cache and redeploy.
