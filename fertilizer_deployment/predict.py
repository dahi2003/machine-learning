"""
predict.py
==========
Fertilizer Prediction System — Command-Line Inference Tool
Chhatrapati Shahu Ji Maharaj University | Sem VI | Session 2025-26

Usage examples
--------------
# Interactive mode (prompts for each value):
    python predict.py

# Pass all values as flags:
    python predict.py --temp 30 --humidity 66 --moisture 38 \
        --soil Red --crop Millets --nitrogen 23 --potassium 0 --phosphorous 24

# Predict from a CSV file (no header required beyond column names):
    python predict.py --csv samples.csv

CSV format expected (with header row):
    Temparature,Humidity,Moisture,Soil Type,Crop Type,Nitrogen,Potassium,Phosphorous
"""

import argparse
import os
import sys

import joblib
import numpy as np
import pandas as pd

# ── Load model artifacts ──────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

try:
    model   = joblib.load(os.path.join(MODEL_DIR, "random_forest_model.pkl"))
    le_soil = joblib.load(os.path.join(MODEL_DIR, "le_soil.pkl"))
    le_crop = joblib.load(os.path.join(MODEL_DIR, "le_crop.pkl"))
    le_fert = joblib.load(os.path.join(MODEL_DIR, "le_fertilizer.pkl"))
except FileNotFoundError as e:
    sys.exit(f"[ERROR] Model artifacts not found: {e}\nRun `python train_model.py` first.")

SOIL_TYPES  = list(le_soil.classes_)
CROP_TYPES  = list(le_crop.classes_)
FERTILIZERS = list(le_fert.classes_)


# ── Core prediction function ──────────────────────────────────────────────────
def predict_single(temp, humidity, moisture, soil, crop, nitrogen, potassium, phosphorous):
    """Return (fertilizer_name, confidence_pct, probabilities_dict)."""
    if soil not in SOIL_TYPES:
        raise ValueError(f"Soil Type '{soil}' not recognised. Choose from: {SOIL_TYPES}")
    if crop not in CROP_TYPES:
        raise ValueError(f"Crop Type '{crop}' not recognised. Choose from: {CROP_TYPES}")

    soil_enc = le_soil.transform([soil])[0]
    crop_enc = le_crop.transform([crop])[0]

    X = pd.DataFrame([[float(temp), float(humidity), float(moisture),
                       soil_enc, crop_enc,
                       float(nitrogen), float(potassium), float(phosphorous)]],
                      columns=["Temparature","Humidity","Moisture",
                               "Soil Type Enc","Crop Type Enc",
                               "Nitrogen","Potassium","Phosphorous"])

    pred_enc  = model.predict(X)[0]
    pred_name = le_fert.inverse_transform([pred_enc])[0]
    proba     = model.predict_proba(X)[0]
    proba_dict = {le_fert.classes_[i]: round(float(p) * 100, 2)
                  for i, p in enumerate(proba)}
    confidence = max(proba_dict.values())

    return pred_name, confidence, proba_dict


def print_result(pred, conf, proba, idx=None):
    label = f"  Sample {idx}" if idx is not None else "  Result"
    print("\n" + "─" * 52)
    print(f"{label}")
    print(f"  ✅  Recommended Fertilizer : {pred}")
    print(f"  📊  Confidence             : {conf:.1f}%")
    print("  📈  Class Probabilities:")
    for name, pct in sorted(proba.items(), key=lambda x: -x[1]):
        bar = "█" * int(pct / 5)
        print(f"       {name:<12} {bar:<20} {pct:.1f}%")
    print("─" * 52)


# ── Interactive mode ──────────────────────────────────────────────────────────
def interactive():
    print("\n🌱  Fertilizer Prediction System — Interactive Mode")
    print("    (Ctrl+C to quit)\n")

    def ask_float(prompt, lo, hi):
        while True:
            try:
                v = float(input(f"  {prompt} [{lo}–{hi}]: "))
                if lo <= v <= hi:
                    return v
                print(f"    ⚠  Please enter a value between {lo} and {hi}.")
            except ValueError:
                print("    ⚠  Numeric value required.")

    def ask_choice(prompt, choices):
        for i, c in enumerate(choices, 1):
            print(f"    {i:2}. {c}")
        while True:
            try:
                idx = int(input(f"  {prompt} (enter number): ")) - 1
                if 0 <= idx < len(choices):
                    return choices[idx]
                print(f"    ⚠  Enter a number between 1 and {len(choices)}.")
            except ValueError:
                print("    ⚠  Numeric selection required.")

    while True:
        try:
            temp       = ask_float("Temperature (°C)",   25, 38)
            humidity   = ask_float("Humidity (%)",        50, 72)
            moisture   = ask_float("Moisture (%)",        25, 65)

            print("\n  Soil Type:")
            soil       = ask_choice("Select Soil Type", SOIL_TYPES)

            print("\n  Crop Type:")
            crop       = ask_choice("Select Crop Type", CROP_TYPES)

            nitrogen   = ask_float("Nitrogen   N (kg/ha)", 0, 60)
            potassium  = ask_float("Potassium  K (kg/ha)", 0, 30)
            phosphorous= ask_float("Phosphorous P (kg/ha)",0, 60)

            pred, conf, proba = predict_single(
                temp, humidity, moisture, soil, crop,
                nitrogen, potassium, phosphorous
            )
            print_result(pred, conf, proba)

            again = input("\n  Predict another sample? [y/N]: ").strip().lower()
            if again != "y":
                break

        except (KeyboardInterrupt, EOFError):
            print("\n\nBye! 👋")
            break


# ── CSV batch mode ────────────────────────────────────────────────────────────
def predict_csv(csv_path: str):
    print(f"\n📂  Reading: {csv_path}")
    df = pd.read_csv(csv_path)

    required = ["Temparature", "Humidity", "Moisture",
                "Soil Type", "Crop Type",
                "Nitrogen", "Potassium", "Phosphorous"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        sys.exit(f"[ERROR] Missing columns in CSV: {missing}")

    preds, confs = [], []
    for i, row in df.iterrows():
        try:
            pred, conf, proba = predict_single(
                row["Temparature"], row["Humidity"], row["Moisture"],
                row["Soil Type"],   row["Crop Type"],
                row["Nitrogen"],    row["Potassium"], row["Phosphorous"]
            )
            preds.append(pred)
            confs.append(conf)
            print_result(pred, conf, proba, idx=i + 1)
        except ValueError as e:
            preds.append("ERROR")
            confs.append(0.0)
            print(f"\n  ⚠  Row {i+1} skipped: {e}")

    out_path = csv_path.replace(".csv", "_predictions.csv")
    df["Predicted Fertilizer"] = preds
    df["Confidence (%)"]       = confs
    df.to_csv(out_path, index=False)
    print(f"\n✅  Results saved to: {out_path}")


# ── CLI entrypoint ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Fertilizer Prediction CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--temp",        type=float, help="Temperature (°C)")
    parser.add_argument("--humidity",    type=float, help="Humidity (%%)")
    parser.add_argument("--moisture",    type=float, help="Moisture (%%)")
    parser.add_argument("--soil",        type=str,   help=f"Soil Type: {SOIL_TYPES}")
    parser.add_argument("--crop",        type=str,   help=f"Crop Type: {CROP_TYPES}")
    parser.add_argument("--nitrogen",    type=float, help="Nitrogen N (kg/ha)")
    parser.add_argument("--potassium",   type=float, help="Potassium K (kg/ha)")
    parser.add_argument("--phosphorous", type=float, help="Phosphorous P (kg/ha)")
    parser.add_argument("--csv",         type=str,   help="Path to CSV file for batch prediction")
    args = parser.parse_args()

    if args.csv:
        predict_csv(args.csv)
    elif all(v is not None for v in [
            args.temp, args.humidity, args.moisture, args.soil,
            args.crop, args.nitrogen, args.potassium, args.phosphorous]):
        try:
            pred, conf, proba = predict_single(
                args.temp, args.humidity, args.moisture,
                args.soil, args.crop,
                args.nitrogen, args.potassium, args.phosphorous
            )
            print_result(pred, conf, proba)
        except ValueError as e:
            sys.exit(f"[ERROR] {e}")
    else:
        interactive()


if __name__ == "__main__":
    main()
