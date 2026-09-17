
import os
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


# ============================================================
# PATH CONFIGURATION
# ============================================================

# Works both locally and on Streamlit Cloud
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "waste_classifier.keras"
CLASS_PATH = BASE_DIR / "models" / "class_names.json"

IMG_SIZE = (224, 224)


# ============================================================
# DISPLAY NAMES
# ============================================================

DISPLAY_NAMES = {
    "organic": "Organic / Biodegradable",
    "plastic": "Plastic",
    "paper": "Paper / Cardboard",
    "metal": "Metal",
    "glass": "Glass",
    "e_waste": "E-Waste",
    "textile": "Textile",
    "general": "General Waste",
    "cardboard": "Cardboard",
}


# ============================================================
# MODEL LOADER
# ============================================================

_model = None
_class_names = None


def load_model():
    global _model
    global _class_names

    # --------------------------------------------------------
    # Already loaded
    # --------------------------------------------------------
    if _model is not None and _class_names is not None:
        return _model, _class_names

    # --------------------------------------------------------
    # Check model file
    # --------------------------------------------------------
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "\n\nTrained model not found.\n\n"
            f"Expected location:\n{MODEL_PATH}\n\n"
            "Make sure models/waste_classifier.keras exists "
            "in the project repository."
        )

    # --------------------------------------------------------
    # Check class mapping
    # --------------------------------------------------------
    if not CLASS_PATH.exists():
        raise FileNotFoundError(
            "\n\nClass mapping not found.\n\n"
            f"Expected location:\n{CLASS_PATH}\n\n"
            "Make sure models/class_names.json exists "
            "in the project repository."
        )

    # --------------------------------------------------------
    # Load trained model
    # --------------------------------------------------------
    _model = tf.keras.models.load_model(
        MODEL_PATH
    )

    # --------------------------------------------------------
    # Load class names
    # --------------------------------------------------------
    with open(
        CLASS_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        _class_names = json.load(file)

    return _model, _class_names


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize to MobileNetV2 input size
    image = image.resize(IMG_SIZE)

    # Convert image to NumPy array
    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    # MobileNetV2 preprocessing
    image_array = (
        tf.keras.applications.mobilenet_v2.preprocess_input(
            image_array
        )
    )

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


# ============================================================
# PREDICTION
# ============================================================

def process_and_predict(image):

    model, class_names = load_model()

    processed_image = preprocess_image(image)

    # --------------------------------------------------------
    # Model prediction
    # --------------------------------------------------------
    probabilities = model.predict(
        processed_image,
        verbose=0
    )[0]

    # --------------------------------------------------------
    # Top predictions
    # --------------------------------------------------------
    sorted_indices = np.argsort(
        probabilities
    )[::-1]

    top_predictions = []

    for index in sorted_indices[:3]:

        raw_category = class_names[index]

        confidence = (
            float(probabilities[index]) * 100
        )

        display_category = DISPLAY_NAMES.get(
            raw_category,
            raw_category.replace("_", " ").title()
        )

        top_predictions.append({
            "category": display_category,
            "raw_category": raw_category,
            "confidence": round(
                confidence,
                2
            )
        })

    # --------------------------------------------------------
    # Best prediction
    # --------------------------------------------------------
    best = top_predictions[0]

    # --------------------------------------------------------
    # Uncertainty protection
    # --------------------------------------------------------
    if best["confidence"] < 45:

        category = "Uncertain / Needs Review"

    else:

        category = best["category"]

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------
    return {
        "category": category,
        "raw_category": best["raw_category"],
        "confidence": best["confidence"],
        "top_predictions": top_predictions,
    }
