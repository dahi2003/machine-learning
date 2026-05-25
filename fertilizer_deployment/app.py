

import os
import logging
from flask import Flask, request, jsonify, render_template_string

import joblib
import numpy as np
import pandas as pd

# ── ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__)
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

# ── Load artifacts at startup ─────────────────────────────────────────────────
try:
    model   = joblib.load(os.path.join(MODEL_DIR, "random_forest_model.pkl"))
    le_soil = joblib.load(os.path.join(MODEL_DIR, "le_soil.pkl"))
    le_crop = joblib.load(os.path.join(MODEL_DIR, "le_crop.pkl"))
    le_fert = joblib.load(os.path.join(MODEL_DIR, "le_fertilizer.pkl"))
    logger.info("✅ Model and encoders loaded successfully.")
except FileNotFoundError as e:
    raise RuntimeError(
        f"Model artifacts not found: {e}\n"
        "Run `python train_model.py` first to generate them."
    )

SOIL_TYPES  = list(le_soil.classes_)
CROP_TYPES  = list(le_crop.classes_)
FERTILIZERS = list(le_fert.classes_)
FEATURE_NAMES = [
    "Temparature", "Humidity", "Moisture",
    "Soil Type", "Crop Type",
    "Nitrogen", "Potassium", "Phosphorous",
]


# ── Helper ────────────────────────────────────────────────────────────────────
def encode_and_predict(data: dict):
    """
    Accepts a dict with keys matching FEATURE_NAMES.
    Returns (predicted_fertilizer: str, probabilities: dict).
    Raises ValueError with a descriptive message on bad input.
    """
    # Validate presence
    for field in FEATURE_NAMES:
        if field not in data:
            raise ValueError(f"Missing field: '{field}'")

    # Encode categoricals
    soil = str(data["Soil Type"]).strip()
    crop = str(data["Crop Type"]).strip()
    if soil not in SOIL_TYPES:
        raise ValueError(f"Unknown Soil Type '{soil}'. Valid: {SOIL_TYPES}")
    if crop not in CROP_TYPES:
        raise ValueError(f"Unknown Crop Type '{crop}'. Valid: {CROP_TYPES}")

    soil_enc = le_soil.transform([soil])[0]
    crop_enc = le_crop.transform([crop])[0]

    # Numeric features
    try:
        temp      = float(data["Temparature"])
        humidity  = float(data["Humidity"])
        moisture  = float(data["Moisture"])
        nitrogen  = float(data["Nitrogen"])
        potassium = float(data["Potassium"])
        phosph    = float(data["Phosphorous"])
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Numeric conversion error: {exc}")

    X = pd.DataFrame([[temp, humidity, moisture, soil_enc, crop_enc,
                       nitrogen, potassium, phosph]],
                      columns=["Temparature","Humidity","Moisture",
                               "Soil Type Enc","Crop Type Enc",
                               "Nitrogen","Potassium","Phosphorous"])

    pred_enc  = model.predict(X)[0]
    pred_name = le_fert.inverse_transform([pred_enc])[0]
    proba     = model.predict_proba(X)[0]
    proba_dict = {le_fert.classes_[i]: round(float(p), 4) for i, p in enumerate(proba)}

    return pred_name, proba_dict


# ── HTML template (embedded, no extra file needed) ────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Fertilizer Prediction System</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; color: #333; }
  header {
    background: linear-gradient(135deg, #1a6b3c 0%, #2e9e5a 100%);
    color: white; padding: 24px 32px;
  }
  header h1 { font-size: 1.6rem; }
  header p  { opacity: .85; font-size:.9rem; margin-top:4px; }
  .container { max-width: 820px; margin: 32px auto; padding: 0 16px; }
  .card {
    background: white; border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,.1); padding: 28px; margin-bottom: 24px;
  }
  h2 { color: #1a6b3c; margin-bottom: 18px; font-size: 1.15rem; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  label { display: block; font-size: .85rem; font-weight: 600;
          color: #555; margin-bottom: 4px; }
  input, select {
    width: 100%; padding: 9px 12px; border: 1px solid #d1d5db;
    border-radius: 7px; font-size: .95rem; transition: border .2s;
  }
  input:focus, select:focus { border-color: #2e9e5a; outline: none; }
  .hint { font-size: .75rem; color: #888; margin-top: 3px; }
  button {
    display: block; width: 100%; padding: 13px;
    background: linear-gradient(135deg, #1a6b3c, #2e9e5a);
    color: white; border: none; border-radius: 8px;
    font-size: 1rem; font-weight: 600; cursor: pointer; margin-top: 8px;
    transition: opacity .2s;
  }
  button:hover { opacity: .88; }
  #result { display:none; }
  .result-box {
    background: #f0fdf4; border: 2px solid #2e9e5a;
    border-radius: 10px; padding: 20px; text-align: center;
  }
  .result-name { font-size: 2rem; font-weight: 700; color: #1a6b3c; }
  .result-conf { font-size: .95rem; color: #555; margin-top: 6px; }
  .prob-bars { margin-top: 16px; text-align: left; }
  .prob-row  { display:flex; align-items:center; margin-bottom: 6px; font-size:.85rem; }
  .prob-label{ width: 100px; font-weight: 600; }
  .prob-track{ flex:1; background:#e5e7eb; border-radius:4px; height:12px; margin: 0 8px; }
  .prob-fill { background: #2e9e5a; border-radius:4px; height:100%; transition: width .5s; }
  .prob-pct  { width: 45px; text-align:right; }
  .error-box { background:#fef2f2; border:2px solid #ef4444;
               border-radius:10px; padding:16px; color:#dc2626; }
  .badge {
    display:inline-block; background:#dcfce7; color:#166534;
    border-radius:20px; padding: 3px 12px; font-size:.8rem; font-weight:600;
    margin: 6px 4px;
  }
  footer { text-align:center; font-size:.8rem; color:#888; padding: 20px 0 40px; }
</style>
</head>
<body>
<header>
  <h1>🌱 Fertilizer Prediction System</h1>
  <p>Soil Health–Based ML Recommendation | CSJMU Sem VI Project · Dr. Alok Kumar</p>
</header>

<div class="container">

  <div class="card">
    <h2>📋 Enter Soil & Crop Parameters</h2>
    <div class="grid">

      <div>
        <label>Temperature (°C)</label>
        <input type="number" id="temp" placeholder="25–38" min="0" max="60" step="0.1"/>
        <div class="hint">Ambient temperature in Celsius</div>
      </div>

      <div>
        <label>Humidity (%)</label>
        <input type="number" id="humidity" placeholder="50–72" min="0" max="100" step="0.1"/>
        <div class="hint">Relative humidity percentage</div>
      </div>

      <div>
        <label>Moisture (%)</label>
        <input type="number" id="moisture" placeholder="25–65" min="0" max="100" step="0.1"/>
        <div class="hint">Soil moisture percentage</div>
      </div>

      <div>
        <label>Soil Type</label>
        <select id="soil">
          <option value="">— Select —</option>
          {% for s in soil_types %}
          <option value="{{ s }}">{{ s }}</option>
          {% endfor %}
        </select>
      </div>

      <div>
        <label>Crop Type</label>
        <select id="crop">
          <option value="">— Select —</option>
          {% for c in crop_types %}
          <option value="{{ c }}">{{ c }}</option>
          {% endfor %}
        </select>
      </div>

      <div>
        <label>Nitrogen — N (kg/ha)</label>
        <input type="number" id="nitrogen" placeholder="4–42" min="0" max="100" step="0.1"/>
      </div>

      <div>
        <label>Potassium — K (kg/ha)</label>
        <input type="number" id="potassium" placeholder="0–19" min="0" max="100" step="0.1"/>
      </div>

      <div>
        <label>Phosphorous — P (kg/ha)</label>
        <input type="number" id="phosphorous" placeholder="0–42" min="0" max="100" step="0.1"/>
      </div>

    </div>

    <br/>
    <button onclick="predict()">🔍 Predict Fertilizer</button>
  </div>

  <div class="card" id="result">
    <h2>🎯 Prediction Result</h2>
    <div id="result-content"></div>
  </div>

  <div class="card">
    <h2>ℹ️ Supported Fertilizer Classes</h2>
    {% for f in fertilizers %}
    <span class="badge">{{ f }}</span>
    {% endfor %}
    <p style="margin-top:12px;font-size:.85rem;color:#666;">
      Model: <strong>Random Forest</strong> (100 trees) &nbsp;|&nbsp;
      Test Accuracy: <strong>75.5%</strong> &nbsp;|&nbsp;
      CV Accuracy: <strong>77.0%</strong>
    </p>
  </div>

</div>

<footer>
  Anshuman Tiwari · Shubham Kumar Gupta · Omkar Yadav &nbsp;|&nbsp;
  Dept. of CSE, CSJMU, Kanpur &nbsp;|&nbsp; Session 2025-26
</footer>

<script>
async function predict() {
  const payload = {
    Temparature:  document.getElementById('temp').value,
    Humidity:     document.getElementById('humidity').value,
    Moisture:     document.getElementById('moisture').value,
    "Soil Type":  document.getElementById('soil').value,
    "Crop Type":  document.getElementById('crop').value,
    Nitrogen:     document.getElementById('nitrogen').value,
    Potassium:    document.getElementById('potassium').value,
    Phosphorous:  document.getElementById('phosphorous').value,
  };

  const resultCard = document.getElementById('result');
  const resultContent = document.getElementById('result-content');
  resultCard.style.display = 'block';
  resultContent.innerHTML = '<p style="color:#888">⏳ Predicting…</p>';

  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    const data = await resp.json();

    if (!resp.ok) {
      resultContent.innerHTML = `<div class="error-box">❌ ${data.error}</div>`;
      return;
    }

    const probs = data.probabilities;
    const sorted = Object.entries(probs).sort((a,b) => b[1]-a[1]);
    const confidence = (data.confidence * 100).toFixed(1);

    let barsHtml = sorted.map(([name, p]) => {
      const pct = (p * 100).toFixed(1);
      return `<div class="prob-row">
        <span class="prob-label">${name}</span>
        <div class="prob-track"><div class="prob-fill" style="width:${pct}%"></div></div>
        <span class="prob-pct">${pct}%</span>
      </div>`;
    }).join('');

    resultContent.innerHTML = `
      <div class="result-box">
        <div class="result-name">🌿 ${data.prediction}</div>
        <div class="result-conf">Confidence: <strong>${confidence}%</strong></div>
      </div>
      <div class="prob-bars" style="margin-top:20px">
        <p style="font-weight:600;margin-bottom:10px;font-size:.9rem">Class Probabilities</p>
        ${barsHtml}
      </div>`;
  } catch (err) {
    resultContent.innerHTML = `<div class="error-box">❌ Network error: ${err}</div>`;
  }
}
</script>
</body>
</html>
"""


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        HTML_TEMPLATE,
        soil_types=SOIL_TYPES,
        crop_types=CROP_TYPES,
        fertilizers=FERTILIZERS,
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "RandomForestClassifier",
                    "fertilizer_classes": FERTILIZERS})


@app.route("/model_info", methods=["GET"])
def model_info():
    feature_cols = ["Temparature", "Humidity", "Moisture",
                    "Soil Type Enc", "Crop Type Enc",
                    "Nitrogen", "Potassium", "Phosphorous"]
    importances  = dict(zip(feature_cols, model.feature_importances_.tolist()))
    return jsonify({
        "model_type":       "RandomForestClassifier",
        "n_estimators":     model.n_estimators,
        "n_classes":        model.n_classes_,
        "fertilizer_classes": FERTILIZERS,
        "soil_types":       SOIL_TYPES,
        "crop_types":       CROP_TYPES,
        "feature_importances": importances,
        "test_accuracy":    0.755,
        "cv_accuracy":      0.770,
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        prediction, probabilities = encode_and_predict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422

    confidence = max(probabilities.values())
    logger.info("Prediction: %s (conf=%.2f)", prediction, confidence)

    return jsonify({
        "prediction":    prediction,
        "confidence":    confidence,
        "probabilities": probabilities,
    })


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    """
    Accepts a JSON array of samples.
    Returns a list of prediction objects.
    Example body: [{"Temparature": 30, "Humidity": 60, ...}, {...}]
    """
    data = request.get_json(silent=True)
    if not isinstance(data, list):
        return jsonify({"error": "Body must be a JSON array of sample objects"}), 400

    results = []
    for i, sample in enumerate(data):
        try:
            pred, proba = encode_and_predict(sample)
            results.append({
                "index":       i,
                "prediction":  pred,
                "confidence":  max(proba.values()),
                "probabilities": proba,
            })
        except ValueError as e:
            results.append({"index": i, "error": str(e)})

    return jsonify(results)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info("Starting Fertilizer Prediction API on port %d …", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
