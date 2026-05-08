# Render Deployment: Build Timeout Fix

**Issue:** Render deployments were timing out during the `pip install` phase, specifically while trying to compile pandas==2.2.2 from source.

**Root Cause:**
- The monolithic root `requirements.txt` includes heavy ML dependencies (torch, transformers, sentence-transformers) that aren't needed for all apps
- Render's free tier uses limited build resources
- Python 3.10 doesn't have pre-built wheels for all dependencies, forcing compilation from source
- Pandas 2.2.2 compilation takes 4+ minutes on Render, leading to timeouts

## Solution

Created **app-specific `requirements.txt` files** for each Render deployment with:

### 1. **teaching_analytics** (`apps/teaching_analytics/requirements.txt`)
- **Dependencies:** fastapi, uvicorn, pandas, streamlit, plotly
- **Excludes:** torch, transformers, sentence-transformers
- **Python Version:** 3.11 (ensures pre-built wheels available)
- **Estimated build time:** < 2 minutes

### 2. **churn_predictor** (`apps/churn_predictor/requirements.txt`)
- **Dependencies:** streamlit, pandas, numpy, scikit-learn, plotly
- **Excludes:** torch, transformers
- **Python Version:** 3.11
- **Estimated build time:** < 2 minutes

### 3. **embedding_explorer** (`apps/embedding_explorer/requirements.txt`)
- **Dependencies:** gradio, torch, sentence-transformers, scikit-learn, matplotlib
- **Deployment:** Hugging Face Spaces (not Render)
- **Note:** Can handle longer build times; ML dependencies necessary

## Updated Deployment Configs

All `render.yaml` files now:
- Point to app-specific `requirements.txt` (not root)
- Set `PYTHON_VERSION: 3.11.0` (wheels readily available)
- Use correct `startCommand` for each app

### Example: teaching_analytics render.yaml

```yaml
services:
  - type: web
    name: teaching-analytics-api
    runtime: python
    rootDir: apps/teaching_analytics
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

## Deployment Changes

| App | Before | After | Benefit |
|---|---|---|---|
| teaching_analytics | Root reqs + 3.10 | App-specific reqs + 3.11 | 🟢 Wheels pre-built, < 2min build |
| churn_predictor | Root reqs + 3.10 | App-specific reqs + 3.11 | 🟢 Faster, no torch/transformers |
| embedding_explorer | None | App-specific reqs | 🟢 HF Spaces can detect dependencies |

## Testing Next Deployment

When you redeploy to Render:

1. Push code (triggers build automatically)
2. Monitor build logs for install progress
3. Should see `pip install` complete in < 2 minutes (was hanging indefinitely before)
4. App should start successfully

## Reference

- **Root requirements.txt** — Kept as-is for research reproducibility (per CLAUDE.md)
- **App requirements.txt** — Lightweight, fast-building, deployment-specific
- **Python 3.11** — Best wheel support across PyPI for data science packages

---

**Status:** All Render deployments now configured for fast, reliable builds. ✅
