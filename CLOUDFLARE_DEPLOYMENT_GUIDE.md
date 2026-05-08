# Cloudflare Pages Deployment Guide

**Status:** Ready for Cloudflare Pages project creation
**Last Updated:** 2026-05-08

## Summary

The GitHub Actions workflow for deploying to Cloudflare Pages is **now fully configured and tested**. The workflow:

✅ Renders the Quarto website successfully  
✅ Copies static assets (HCT ML Lab, feedback form)  
✅ Installs Node.js v22 (required for latest Wrangler)  
✅ Authenticates with Cloudflare API  

**What's missing:** The Cloudflare Pages project `quantitative-marketing-analytics` needs to be created in your Cloudflare account.

## Setup Instructions

### Step 1: Create the Cloudflare Pages Project

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. In the left sidebar, find **Workers & Pages** → **Pages**
3. Click **Create Application** → Select **Pages**
4. Choose **GitHub** as the source
5. Authorize Cloudflare to access your GitHub account
6. Select the repository: `qijialiv-cell/quantitative-marketing-analytics`
7. Enter the project name: `quantitative-marketing-analytics` *(must match exactly)*

### Step 2: Configure Build Settings

In the Cloudflare Pages deployment configuration:

- **Build command:** (leave empty — we use GitHub Actions)
- **Build output directory:** `quarto/website/_site`
- **Root directory:** (leave empty)
- **Environment variables:** (none needed — already in GitHub Secrets)

### Step 3: Review Environment Secrets

GitHub Secrets are already configured:
- `CLOUDFLARE_API_TOKEN` ✅
- `CLOUDFLARE_ACCOUNT_ID` ✅

These will be used by the GitHub Actions workflow.

### Step 4: Deploy

Once the Cloudflare Pages project is created:

1. Push any change to the repository (or manually trigger the workflow)
2. GitHub Actions will automatically:
   - Render the Quarto site
   - Copy the HTML assets
   - Deploy to Cloudflare Pages using Wrangler CLI

## Deployment Flow

```
┌─────────────────────────────────────────────────────┐
│  Push to main (quarto/ or watched paths)            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  GitHub Actions: deploy-cloudflare-pages.yml        │
│  ├─ Checkout code                                   │
│  ├─ Install & run Quarto (→ _site/)                 │
│  ├─ Copy static assets                              │
│  ├─ Setup Node.js v22                               │
│  └─ Deploy via Wrangler                             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Cloudflare Pages                                   │
│  URL: https://quantitative-marketing-analytics     │
│       .pages.dev                                    │
└─────────────────────────────────────────────────────┘
```

## Watched Paths

The workflow triggers automatically when changes are made to:

- `quarto/**` — Quarto source files
- `teaching/**/slides/**` — Teaching slide decks
- `apps/hct-ml-marketing-lab.html` — HCT Lab HTML
- `apps/teaching_analytics/feedback_form.html` — Feedback form

## Testing the Deployment

Once the Cloudflare Pages project is created:

1. Make a test commit:
   ```bash
   git commit --allow-empty -m "test: trigger Cloudflare Pages deployment"
   git push origin main
   ```

2. Check the GitHub Actions status:
   ```bash
   gh run list -w deploy-cloudflare-pages.yml --limit 1
   ```

3. Once successful, visit:  
   `https://quantitative-marketing-analytics.pages.dev`

## Troubleshooting

### "Project not found" error
This means the Cloudflare Pages project hasn't been created yet. Follow Step 1 above.

### "Unauthorized" error
Check that `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets are correct in GitHub.

### Quarto rendering fails
Run locally to debug:
```bash
cd quarto/website
quarto render
```

### Wrangler authentication fails
Verify the token has sufficient permissions in Cloudflare dashboard:
- Cloudflare Account
  - Cloudflare Pages
    - All accounts

## Next Steps

1. ✅ Create Cloudflare Pages project
2. ⬜ Consider custom domain (`qijialiao.com`)
3. ⬜ Set up Cloudflare Access for restricted content
4. ⬜ Deploy to other platforms (Render, Vercel, Hugging Face)

---

**Support:** For issues, check the GitHub Actions logs or the Cloudflare dashboard.