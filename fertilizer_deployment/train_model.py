"""
train_model.py
==============
Fertilizer Prediction System — Model Training Script
Chhatrapati Shahu Ji Maharaj University | Sem VI | Session 2025-26
Authors: Anshuman Tiwari, Shubham Kumar Gupta, Omkar Yadav
Guided by: Dr. Alok Kumar

Run this script to retrain the Random Forest model and regenerate
all saved artifacts (model + label encoders).

Usage:
    python train_model.py --data Fertilizer_Prediction_Modified.xlsx
"""

import argparse
import datetime
import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────
# Configuration (mirrors the project report)
# ──────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.20
N_ESTIMATORS = 100
CV_FOLDS = 5
MODEL_DIR = "model"

FEATURE_COLS = [
    "Temparature",
    "Humidity",
    "Moisture",
    "Soil Type Enc",
    "Crop Type Enc",
    "Nitrogen",
    "Potassium",
    "Phosphorous",
]
TARGET_COL = "Fertilizer Name"


def fix_date_parsing(val):
    """Excel parses '10-26-26' as a datetime. Convert it back."""
    if isinstance(val, datetime.datetime):
        return "10-26-26"
    return str(val)


def load_and_preprocess(data_path: str):
    print(f"[1/4] Loading dataset: {data_path}")
    df = pd.read_excel(data_path)
    print(f"      Rows: {len(df)}  |  Columns: {list(df.columns)}")

    # Fix Excel date-parsing artefact on fertilizer '10-26-26'
    df[TARGET_COL] = df[TARGET_COL].apply(fix_date_parsing)

    print("\n[2/4] Label-encoding categorical columns …")
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()
    le_fert = LabelEncoder()

    df["Soil Type Enc"] = le_soil.fit_transform(df["Soil Type"])
    df["Crop Type Enc"] = le_crop.fit_transform(df["Crop Type"])
    df["Fertilizer Enc"] = le_fert.fit_transform(df[TARGET_COL])

    print(f"      Soil types  : {dict(zip(le_soil.classes_, le_soil.transform(le_soil.classes_)))}")
    print(f"      Crop types  : {dict(zip(le_crop.classes_, le_crop.transform(le_crop.classes_)))}")
    print(f"      Fertilizers : {dict(zip(le_fert.classes_, le_fert.transform(le_fert.classes_)))}")

    X = df[FEATURE_COLS]
    y = df["Fertilizer Enc"]
    return X, y, le_soil, le_crop, le_fert


def train_and_evaluate(X, y, le_fert):
    print("\n[3/4] Splitting data (80% train / 20% test, stratified) …")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"      Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    print(f"\n      Training Random Forest (n_estimators={N_ESTIMATORS}) …")
    rf = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)

    cv_scores = cross_val_score(rf, X, y, cv=CV_FOLDS, scoring="accuracy")
    cv_mean = cv_scores.mean()

    print(f"\n      ✔  Test Accuracy        : {test_acc*100:.1f}%")
    print(f"      ✔  CV Accuracy (5-fold) : {cv_mean*100:.1f}%  (±{cv_scores.std()*100:.1f}%)")
    print("\n" + classification_report(y_test, y_pred, target_names=le_fert.classes_))

    return rf, X_train, X_test, y_test, y_pred


def save_artifacts(rf, le_soil, le_crop, le_fert):
    print(f"[4/4] Saving model artifacts to ./{MODEL_DIR}/ …")
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf,      os.path.join(MODEL_DIR, "random_forest_model.pkl"))
    joblib.dump(le_soil, os.path.join(MODEL_DIR, "le_soil.pkl"))
    joblib.dump(le_crop, os.path.join(MODEL_DIR, "le_crop.pkl"))
    joblib.dump(le_fert, os.path.join(MODEL_DIR, "le_fertilizer.pkl"))
    print("      Saved: random_forest_model.pkl, le_soil.pkl, le_crop.pkl, le_fertilizer.pkl")


def main():
    parser = argparse.ArgumentParser(description="Train Fertilizer Prediction Model")
    parser.add_argument(
        "--data",
        default="Fertilizer_Prediction_Modified.xlsx",
        help="Path to the Excel dataset",
    )
    args = parser.parse_args()

    X, y, le_soil, le_crop, le_fert = load_and_preprocess(args.data)
    rf, X_train, X_test, y_test, y_pred = train_and_evaluate(X, y, le_fert)
    save_artifacts(rf, le_soil, le_crop, le_fert)
    print("\n✅  Training complete. Run `python app.py` to start the API server.")


if __name__ == "__main__":
    main()
