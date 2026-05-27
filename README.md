fertilizer prediction model 

MODEL PERFORMANCE
───────────────────────────────────────────────────────────────────

Algorithm: Random Forest Classifier (100 trees)
Test Accuracy: 75.5%
Cross-Validation Accuracy: 77.0%
Average F1 Score: 75.4%

Input Features (8):

- Temperature (25-38°C)
- Humidity (50-72%)
- Moisture (25-65%)
- Soil Type (Black, Clayey, Loamy, Red, Sandy)
- Crop Type (11 types: Barley, Cotton, Maize, etc.)
- Nitrogen (4-42 kg/ha)
- Potassium (0-19 kg/ha)
- Phosphorous (0-42 kg/ha)

Output Classes (7 Fertilizers):
10-26-26, 14-35-14, 17-17-17, 20-20, 28-28, DAP, Urea

Top Features by Importance:

1. Phosphorous (24.75%)
2. Nitrogen (23.85%)
3. Potassium (15.43%)
4. Moisture (8.74%)
5. Crop Type (7.76%)

───────────────────────────────────────────────────────────────────
📁 FILE STRUCTURE
───────────────────────────────────────────────────────────────────

fertilizer_prediction_deployment/
│
├── 📄 START_HERE.md ..................... ⭐ READ THIS FIRST
├── 📄 GITHUB_RENDER_DEPLOY.md ........... Step-by-step guide
├── 📄 QUICKSTART.md ..................... Quick reference
├── 📄 DEPLOYMENT.md ..................... Detailed setup
├── 📄 DEPLOYMENT_READY.txt .............. Overview
│
├── 🔧 deploy.bat ........................ Auto git setup (Windows)
├── 📋 Procfile .......................... Cloud deployment config
├── 📋 runtime.txt ....................... Python 3.11.6
├── 📋 gunicorn_config.py ................ WSGI server config
├── 📋 .gitignore ........................ Git ignore rules
├── ✅ validate_deployment.py ........... Verify setup
│
└── 📂 fertilizer_deployment/
├── 🐍 app.py ........................ Flask REST API + Web UI
├── 🐍 predict.py ................... CLI prediction tool
├── 🐍 train_model.py ............... Model retraining
├── 📋 requirements.txt ............. Dependencies
│
└── 📂 model/
├── 🤖 random_forest_model.pkl
├── 🔀 le_soil.pkl
├── 🔀 le_crop.pkl
└── 🔀 le_fertilizer.pkl

───────────────────────────────────────────────────────────────────
🔗 AVAILABLE API ENDPOINTS
───────────────────────────────────────────────────────────────────

GET /
→ Web interface with prediction form

GET /health
→ Server status & model info

GET /model_info
→ Model metadata, feature importance, accuracy

POST /predict
→ Single sample prediction
Request: JSON object with 8 fields
Response: prediction, confidence, probabilities

POST /predict_batch
→ Batch predictions (array of samples)
Request: JSON array of 8-field objects
Response: Array of predictions
