# Data Modeling API

This folder contains an end-to-end AI data modeling workflow built for FastAPI Swagger usage.

## Architecture

- `orchestrator.py`: stage-based router for conceptual, logical, and physical flows
- `tools.py`: one-shot core banking glossary prompt context and generation tools
- `prompts.py`: detailed prompts for each modeling stage
- `schemas.py`: request and response contracts used by Swagger
- `api.py`: FastAPI entry point
- `rag.py`: legacy optional RAG helper, not used by the active API flow

For a more junior-friendly walkthrough of the codebase, see `ARCHITECTURE.md`.

## Recommended demo path

Use Swagger at `http://127.0.0.1:8000/docs` and call:

1. `POST /orchestrate` with the business requirement
2. Review the returned conceptual JSON, Mermaid text, and artifact links
3. Open `conceptual_view_url` to visualize the ER diagram
4. Use the returned download links for JSON and Mermaid artifacts
5. Send an approval request to `POST /orchestrate` with the same `artifact_id`
   to generate logical and physical outputs

## Run

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

## Deployment

Use `render.yaml` to deploy the FastAPI backend on Render, then deploy
`frontend/streamlit_app.py` on Streamlit Community Cloud with
`BACKEND_API_URL` set to the Render service URL. See `DEPLOYMENT.md` for the
full checklist.

Create a local `.env` file in the repository root:

```bash
cp .env.example .env
```

Then set:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env`; it is ignored by `.gitignore`.

## Example Swagger request

```json
{
  "requirement": "Design a retail banking data model where a customer can hold multiple accounts and each account can have many transactions.",
  "artifact_id": null
}
```

## Gemini setup

- Store `GEMINI_API_KEY` in `.env`
- Optional: set `GEMINI_MODEL` if you want a model other than the configured default

## Notes

- Conceptual generation sends the full core banking glossary into the prompt as one-shot context instead of using RAG retrieval.
- Conceptual modeling should use a structured output schema, not a physical database schema.
- Mermaid is generated from the conceptual model structure using `utils/mermaid_builder.py`.
