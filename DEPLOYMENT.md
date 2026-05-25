# 🚀 Deployment Guide — Render (Free Hosting)

## Prerequisites

- GitHub account (free)
- Render account (free tier available at render.com)
- Git installed locally

## Step 1: Initialize Git Repository

```bash
cd c:\Users\ASUS\Downloads\mlcsjm\fertilizer_prediction_deployment
git init
git add .
git commit -m "Initial commit: Fertilizer Prediction System"
git branch -M main
```

## Step 2: Push to GitHub

Create a new repository on GitHub (https://github.com/new), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/fertilizer-prediction.git
git push -u origin main
```

## Step 3: Deploy on Render

1. **Sign up at render.com** (free tier)
2. **Click "New +" → "Web Service"**
3. **Connect GitHub** and select your repository
4. **Configure:**
   - **Name:** fertilizer-prediction
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn fertilizer_deployment/app:app`
   - **Instance Type:** Free tier (sufficient for demo)

5. **Deploy** — Render will automatically deploy when you push to main

## Step 4: Access Your Application

After deployment completes (2-5 minutes):

- **Web UI:** https://your-service-name.onrender.com
- **Health Check:** https://your-service-name.onrender.com/health
- **API Docs:** https://your-service-name.onrender.com/model_info

## Additional Configuration

### Environment Variables (if needed)

In Render dashboard → Environment:

- `FLASK_DEBUG=0` (default, production safe)
- `PORT=10000` (Render assigns automatically)

### Free Tier Limitations

- Auto-spins down after 15 mins of inactivity (cold start ~30s on first request)
- Max 2 services per account
- Limited to 0.5 GB RAM

### Upgrade for Production

- **Plus Tier ($7/mo):** Always-on, better resources
- **Pro Tier ($12/mo+):** Auto-scaling, priority support

## Troubleshooting

**If deployment fails:**

1. Check build logs in Render dashboard
2. Ensure `Procfile` exists and is correct
3. Verify all model files are in git repo
4. Run locally first: `python fertilizer_deployment/app.py`

**If app crashes after deployment:**

1. Check logs: Render dashboard → Logs
2. Ensure PORT environment variable is used (already set in app.py)
3. Verify model files loaded correctly

## Alternative Platforms

| Platform            | Free Tier | Cold Start | Model Size |
| ------------------- | --------- | ---------- | ---------- |
| **Render**          | Yes       | ~30s       | 200MB OK   |
| Railway             | Yes       | ~5s        | 200MB OK   |
| Hugging Face Spaces | Yes       | ~10s       | 200MB OK   |
| AWS EC2 (t2.micro)  | 1 yr free | ~5s        | 200MB OK   |
| Azure App Service   | Free      | ~10s       | 200MB OK   |

**Recommended: Render** — best free tier with model support and reliability.
