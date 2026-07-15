# 🌱 Fertilizer Prediction System

A Machine Learning-based Fertilizer Recommendation System that predicts the most suitable fertilizer based on soil properties, crop type, environmental conditions, and nutrient levels. The project is deployed as a Flask web application with REST APIs for both single and batch predictions.

---

## 📌 Features

- 🌾 Predicts the most suitable fertilizer for a given crop and soil condition
- 🤖 Built using Random Forest Classifier
- 🌐 Interactive Flask web interface
- 🔗 REST API for easy integration
- 📦 Batch prediction support
- ❤️ Health check endpoint
- 📊 Model information endpoint
- ☁️ Ready for deployment on Render

---

## 🎯 Problem Statement

Selecting the correct fertilizer is essential for improving crop yield while minimizing excessive fertilizer usage. This project uses Machine Learning to recommend the most appropriate fertilizer based on environmental conditions, crop type, soil type, and nutrient composition.

---

# 📊 Model Performance

| Metric | Value |
|---------|------:|
| Algorithm | Random Forest Classifier |
| Number of Trees | 100 |
| Test Accuracy | **75.5%** |
| Cross Validation Accuracy | **77.0%** |
| Average F1 Score | **75.4%** |

---

# 📥 Input Features

The model uses the following eight features:

| Feature | Description |
|----------|-------------|
| Temperature | 25–38°C |
| Humidity | 50–72% |
| Moisture | 25–65% |
| Soil Type | Black, Clayey, Loamy, Red, Sandy |
| Crop Type | Barley, Cotton, Ground Nuts, Maize, Millets, Oil Seeds, Paddy, Pulses, Sugarcane, Tobacco, Wheat |
| Nitrogen | 4–42 kg/ha |
| Potassium | 0–19 kg/ha |
| Phosphorous | 0–42 kg/ha |

---

# 📤 Output Classes

The model predicts one of the following fertilizers:

- 10-26-26
- 14-35-14
- 17-17-17
- 20-20
- 28-28
- DAP
- Urea

---

# 📈 Feature Importance

| Feature | Importance |
|----------|-----------:|
| Phosphorous | 24.75% |
| Nitrogen | 23.85% |
| Potassium | 15.43% |
| Moisture | 8.74% |
| Crop Type | 7.76% |

The nutrient values (NPK) contribute the most to fertilizer recommendation.

---

# 🛠 Tech Stack

- Python 3.11
- Scikit-learn
- Pandas
- NumPy
- Flask
- Gunicorn
- Pickle
- HTML/CSS

---

# 📁 Project Structure

```text
fertilizer_prediction_deployment/
│
├── START_HERE.md
├── QUICKSTART.md
├── DEPLOYMENT.md
├── GITHUB_RENDER_DEPLOY.md
├── DEPLOYMENT_READY.txt
│
├── deploy.bat
├── Procfile
├── runtime.txt
├── gunicorn_config.py
├── validate_deployment.py
│
└── fertilizer_deployment/
    ├── app.py
    ├── predict.py
    ├── train_model.py
    ├── requirements.txt
    │
    └── model/
        ├── random_forest_model.pkl
        ├── le_soil.pkl
        ├── le_crop.pkl
        └── le_fertilizer.pkl
```

---

# 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/your-username/fertilizer-prediction.git
cd fertilizer_prediction_deployment
```

### Install dependencies

```bash
pip install -r fertilizer_deployment/requirements.txt
```

### Run the application

```bash
python fertilizer_deployment/app.py
```

The application will start at:

```
http://localhost:5000
```

---

# 🌐 API Endpoints

## Home

```
GET /
```

Displays the web interface.

---

## Health Check

```
GET /health
```

Returns application status and model availability.

---

## Model Information

```
GET /model_info
```

Returns model metadata including accuracy, feature importance, and supported fertilizer classes.

---

## Single Prediction

```
POST /predict
```

### Request

```json
{
    "Temperature": 30,
    "Humidity": 60,
    "Moisture": 40,
    "Soil Type": "Loamy",
    "Crop Type": "Maize",
    "Nitrogen": 20,
    "Potassium": 10,
    "Phosphorous": 18
}
```

### Response

```json
{
    "prediction": "DAP",
    "confidence": 0.91
}
```

---

## Batch Prediction

```
POST /predict_batch
```

Accepts an array of samples and returns predictions for each record.

---

# ☁️ Deployment

This project is configured for deployment using:

- Flask
- Gunicorn
- Procfile
- runtime.txt
- Render

Deployment documentation:

- START_HERE.md
- QUICKSTART.md
- DEPLOYMENT.md
- GITHUB_RENDER_DEPLOY.md

---

# 📊 Future Improvements

- Improve model accuracy using hyperparameter tuning
- Compare with XGBoost, CatBoost, and LightGBM
- Add fertilizer dosage recommendation
- Integrate IoT soil sensor data
- Develop a mobile application
- Add multilingual support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 👨‍💻 Author

**Omkar Yadav**

Machine Learning | Python | Flask | Scikit-learn

GitHub: https://github.com/dahi2003

⭐ If you found this project useful, consider giving it a star!
