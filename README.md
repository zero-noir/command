# Startup Ops Workspace — Rebuilt

A clean founder/operator workspace for converting meeting notes, paid-media observations, product feedback, finance constraints, and strategy notes into decisions, actions, risks and metrics.

## AI mode
Offline mode works immediately. For real model output, set in `apps/api/.env`:

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
```

or Gemini:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
```

## Run
```bash
cd apps/api && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && uvicorn main:app --reload
cd apps/web && npm install --registry=https://registry.npmjs.org/ && npm run dev -- --host 0.0.0.0
```
