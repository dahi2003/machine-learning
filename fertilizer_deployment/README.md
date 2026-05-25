# 🌱 Fertilizer Prediction System — Deployment Guide

**Chhatrapati Shahu Ji Maharaj University, Kanpur**
Project Report on Machine Learning | Semester VI | Session 2025-26

| Team Member | Enrollment |
|---|---|
| Anshuman Tiwari | CSJMA23001390274 |
| Shubham Kumar Gupta | CSJMA23001390308 |
| Omkar Yadav | CSJMA23001390297 |

**Guided by:** Dr. Alok Kumar | Dept. of Computer Science & Engineering

---

## 📁 Project Structure

```
fertilizer_deployment/
├── model/
│   ├── random_forest_model.pkl   ← Trained Random Forest classifier
│   ├── le_soil.pkl               ← LabelEncoder for Soil Type
│   ├── le_crop.pkl               ← LabelEncoder for Crop Type
│   └── le_fertilizer.pkl         ← LabelEncoder for Fertilizer Name
├── train_model.py                ← Retrain model from Excel dataset
├── predict.py                    ← CLI tool (interactive + batch CSV)
├── app.py                        ← Flask REST API + Web UI
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Retrain the model
Only needed if you have a fresh dataset or want to regenerate the .pkl files:
```bash
python train_model.py --data Fertilizer_Prediction_Modified.xlsx
```

### 3. Run the Web API
```bash
python app.py
```
Then open **http://localhost:5000** in your browser to use the web UI.

### 4. Command-line prediction
```bash
# Interactive mode (guided prompts):
python predict.py

# One-shot flag mode:
python predict.py \
  --temp 30 --humidity 66 --moisture 38 \
  --soil Red --crop Millets \
  --nitrogen 23 --potassium 0 --phosphorous 24

# Batch CSV mode (saves results to *_predictions.csv):
python predict.py --csv my_samples.csv
```

---

## 🌐 API Reference

All endpoints accept and return JSON.

### `GET /health`
Returns server status and available fertilizer classes.

### `GET /model_info`
Returns model metadata, feature importances, and accuracy metrics.

### `POST /predict`
Single-sample prediction.

**Request body:**
```json
{
  "Temparature": 30,
  "Humidity": 66,
  "Moisture": 38,
  "Soil Type": "Red",
  "Crop Type": "Millets",
  "Nitrogen": 23,
  "Potassium": 0,
  "Phosphorous": 24
}
```

**Response:**
```json
{
  "prediction": "28-28",
  "confidence": 0.72,
  "probabilities": {
    "10-26-26": 0.03,
    "14-35-14": 0.05,
    "17-17-17": 0.04,
    "20-20": 0.06,
    "28-28": 0.72,
    "DAP": 0.07,
    "Urea": 0.03
  }
}
```

### `POST /predict_batch`
Array of sample objects — returns a list of prediction results.

---

## 📊 Model Summary

| Rank | Model | Test Acc | CV Acc | Avg F1 |
|---|---|---|---|---|
| ✅ 1 | **Random Forest** | **75.5%** | **77.0%** | **75.4%** |
| 2 | SVM (RBF kernel) | 73.0% | 74.2% | 72.2% |
| 3 | Logistic Regression | 69.5% | 71.6% | 68.3% |
| 4 | K-Nearest Neighbors | 69.0% | 71.5% | 68.7% |
| 5 | Decision Tree | 62.0% | 61.1% | 62.6% |

**Why Random Forest?**
The dataset includes 15% label noise and 30% feature noise (Gaussian) on NPK values to simulate real-world IoT sensor inaccuracies. Random Forest's ensemble bagging strategy makes it inherently robust to this variance.

---

## 🔢 Input Features

| Feature | Type | Range / Values |
|---|---|---|
| Temparature | Numeric | 25–38 °C |
| Humidity | Numeric | 50–72 % |
| Moisture | Numeric | 25–65 % |
| Soil Type | Categorical | Black, Clayey, Loamy, Red, Sandy |
| Crop Type | Categorical | Barley, Cotton, Ground Nuts, Maize, Millets, Oil seeds, Paddy, Pulses, Sugarcane, Tobacco, Wheat |
| Nitrogen (N) | Numeric | 4–42 kg/ha |
| Potassium (K) | Numeric | 0–19 kg/ha |
| Phosphorous (P) | Numeric | 0–42 kg/ha |

## 🌿 Target Classes (7 Fertilizers)

`10-26-26` · `14-35-14` · `17-17-17` · `20-20` · `28-28` · `DAP` · `Urea`

---

## 🔑 Feature Importance (from Random Forest)

| Rank | Feature | Importance |
|---|---|---|
| 1 | Phosphorous | 24.75% |
| 2 | Nitrogen | 23.85% |
| 3 | Potassium | 15.43% |
| 4 | Moisture | 8.74% |
| 5 | Crop Type | 7.76% |
| 6 | Humidity | 7.63% |
| 7 | Temperature | 7.44% |
| 8 | Soil Type | 4.39% |

NPK values collectively drive ~64% of the prediction — consistent with agronomic theory.

---

## 🚀 Future Improvements (from Report)

1. **XGBoost / LightGBM** — expected 2–4% further accuracy gain
2. **Feature Scaling** — critical if deploying SVM or KNN models
3. **Hyperparameter tuning** — `GridSearchCV` on `n_estimators`, `max_depth`
4. **Better IoT sensors** — reduce NPK noise below 30% std dev
5. **Stricter data-validation** — eliminate label noise at source

---

## 🛠 Environment

- Python 3.9+
- scikit-learn ≥ 1.3
- Flask ≥ 3.0
- Tested on Ubuntu 22.04 / Windows 11

---

*End of Deployment Guide*
