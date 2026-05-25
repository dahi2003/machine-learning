# 🚀 Deploy to Render — Complete Instructions for dahi2003

Your **Fertilizer Prediction System** is ready. Follow these steps to deploy it live.

## ⚡ Step 1: Initialize Git (Run Once)

Open Command Prompt (cmd.exe) in the project directory:

```bash
cd c:\Users\ASUS\Downloads\mlcsjm\fertilizer_prediction_deployment

git init
git config user.email "your-email@example.com"
git config user.name "dahi2003"
git add .
git commit -m "Initial commit: Fertilizer Prediction System"
```

**You should see:**

```
[main (root-commit) abc1234] Initial commit: Fertilizer Prediction System
 10 files changed, 5000+ insertions(+)
 create mode 100644 Procfile
 create mode 100644 runtime.txt
 ...
```

---

## ⚡ Step 2: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name:** `fertilizer-prediction`
   - **Description:** "ML-based Fertilizer Prediction System with Flask API"
   - **Public** (recommended for easy sharing)
   - **Initialize with README?** ❌ No (you already have files)
3. Click **Create repository**

---

## ⚡ Step 3: Push Code to GitHub

Copy-paste these commands into Command Prompt:

```bash
git remote add origin https://github.com/dahi2003/fertilizer-prediction.git
git branch -M main
git push -u origin main
```

**You should see:**

```
Enumerating objects: 15, done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**✅ Your code is now on GitHub at:**

```
https://github.com/dahi2003/fertilizer-prediction
```

---

## ⚡ Step 4: Deploy on Render

1. Go to **https://render.com** and sign up (free account)
2. Click **+ New** → **Web Service**
3. Click **Connect GitHub** (authorize Render to access your repos)
4. Select `dahi2003/fertilizer-prediction`
5. Fill in deployment settings:
   - **Name:** `fertilizer-prediction`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt` (auto-detected)
   - **Start Command:** `gunicorn --config gunicorn_config.py fertilizer_deployment.app:app` (auto-detected from Procfile)
   - **Instance Type:** `Free` (starts free, upgrade later if needed)
6. Click **Create Web Service**

**⏳ Render will now:**

- Download your code from GitHub
- Build the environment (~2-3 minutes)
- Start your app
- Assign you a URL like: `https://fertilizer-prediction-xxxx.onrender.com`

---

## ✅ Step 5: Test Your Live App

Once Render shows **"Live"** status (green):

### Web UI

```
https://fertilizer-prediction-xxxx.onrender.com
```

Enter soil parameters and click **🔍 Predict Fertilizer**

### API Health Check

```bash
curl https://fertilizer-prediction-xxxx.onrender.com/health
```

**Expected response:**

```json
{
  "status": "ok",
  "model": "RandomForestClassifier",
  "fertilizer_classes": [
    "10-26-26",
    "14-35-14",
    "17-17-17",
    "20-20",
    "28-28",
    "DAP",
    "Urea"
  ]
}
```

### Make a Prediction

```bash
curl -X POST https://fertilizer-prediction-xxxx.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Temparature": 30,
    "Humidity": 66,
    "Moisture": 38,
    "Soil Type": "Red",
    "Crop Type": "Millets",
    "Nitrogen": 23,
    "Potassium": 0,
    "Phosphorous": 24
  }'
```

**Response:**

```json
{
  "prediction": "28-28",
  "confidence": 0.72,
  "probabilities": {
    "10-26-26": 0.03,
    "14-35-14": 0.05,
    "28-28": 0.72,
    ...
  }
}
```

---

## 🔗 Share Your App

Once live, you can share:

```
https://fertilizer-prediction-xxxx.onrender.com
```

Anyone can:

- Use the web interface
- Call the API from their app
- View predictions in real-time

---

## ⚙️ Advanced: Custom Domain (Optional)

In Render dashboard:

1. Go to your service settings
2. **Custom Domains** → Add domain
3. Point your domain's DNS to Render
4. HTTPS included automatically!

---

## 📊 Monitor Your App

In Render dashboard:

- **Logs** tab → See real-time logs
- **Metrics** tab → CPU, memory, requests
- **Settings** tab → Environment variables, restart service

---

## 💾 Make Changes

If you want to update the app later:

```bash
# In your local project directory
git add .
git commit -m "Fix bug / Add feature"
git push origin main
```

**Render automatically redeploys** within seconds!

---

## 🆘 Troubleshooting

| Issue                     | Solution                                          |
| ------------------------- | ------------------------------------------------- |
| "Deploy failed"           | Check **Logs** tab in Render → see error message  |
| "503 Service Unavailable" | Cold start (free tier). Wait 30s and refresh.     |
| "Model not found"         | Verify `.pkl` files in `/model` folder via GitHub |
| "Import error"            | Check `requirements.txt` has all dependencies     |

---

## 📋 Deployment Checklist

- ✅ Project prepared with Procfile, runtime.txt, gunicorn_config.py
- ✅ Git initialized locally
- ✅ Code committed locally
- ✅ GitHub repository created
- ✅ Code pushed to GitHub
- ✅ Render connected to GitHub
- ✅ Web Service deployed
- ✅ App live at https://fertilizer-prediction-xxxx.onrender.com

---

## 🎯 You're Done!

Your **Fertilizer Prediction System** is now live on the internet! 🎉

Share the link with friends, use it in your portfolio, or integrate it into other projects.

**Questions?** Check `QUICKSTART.md` or `DEPLOYMENT.md` for more details.
