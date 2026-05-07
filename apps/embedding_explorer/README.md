# Semantic Embedding Explorer

**Platform:** Hugging Face Spaces (Gradio)
**Module:** MKTS 420 — Introduction to Deep Learning, Week 3

## Purpose
Research demo and teaching tool for exploring how transformer models embed marketing text.
Supports pairwise similarity comparison and PCA visualisation of embedding clusters.

## Run locally
```bash
cd apps/embedding_explorer
pip install -r ../../requirements.txt
python app.py
```

## Deploy on Hugging Face Spaces
Automated via `.github/workflows/deploy-hf-spaces.yml` on push to `main`.

Update `YOUR_HF_USERNAME` in the workflow file before first deploy.
Set `HF_TOKEN` in GitHub repository secrets.

## Deployed URL
<!-- Update when live -->
https://huggingface.co/spaces/YOUR_HF_USERNAME/embedding-explorer
