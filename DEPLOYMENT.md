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
   - `streamlit_app.py`
3. In Advanced settings, choose Python `3.11`.
4. In Secrets, add:

```toml
BACKEND_API_URL = "https://your-render-service-name.onrender.com"
```

Do not include a trailing slash.

## 4. Local Development

Start the backend locally:

```bash
uvicorn api:app --reload
```

Then start the frontend:

```bash
streamlit run streamlit_app.py
```

The frontend defaults to `http://127.0.0.1:8000` when `BACKEND_API_URL` is not set.

## 5. Important Notes

- Render free services can sleep when idle, so the first frontend request may be slow.
- The Streamlit app calls the backend server-side with Python `requests`, so browser CORS is not needed for the current frontend flow.
- Keep all real credentials in Render environment variables or Streamlit secrets.
- If Render logs show `Using Python version 3.14.3 (default)` and `pydantic-core` fails to build, the Python pin was not applied. Confirm `.python-version` is pushed to GitHub or set `PYTHON_VERSION=3.11.11` in the Render service environment variables, then clear the build cache and redeploy.
