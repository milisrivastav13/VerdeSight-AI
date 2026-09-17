import os
import json

import numpy as np
import tensorflow as tf

from PIL import Image


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = r"E:\Greensight"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "waste_classifier.keras"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)

IMG_SIZE = (224, 224)


# ============================================================
# DISPLAY NAMES
# ============================================================

DISPLAY_NAMES = {

    "organic":
        "Organic / Biodegradable",

    "plastic":
        "Plastic",

    "paper":
        "Paper / Cardboard",

    "metal":
        "Metal",

    "glass":
        "Glass",

    "e_waste":
        "E-Waste",

    "textile":
        "Textile",

    "general":
        "General Waste",
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

    if (
        _model is not None
        and _class_names is not None
    ):

        return _model, _class_names

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "\n\nTrained model not found.\n\n"
            f"Expected location:\n"
            f"{MODEL_PATH}\n\n"
            "First run:\n"
            "python train_model.py"
        )

    if not os.path.exists(CLASS_PATH):

        raise FileNotFoundError(
            "\n\nClass mapping not found.\n\n"
            f"Expected location:\n"
            f"{CLASS_PATH}\n\n"
            "First run:\n"
            "python train_model.py"
        )

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    _model = tf.keras.models.load_model(
        MODEL_PATH
    )

    with open(
        CLASS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        _class_names = json.load(file)

    return (
        _model,
        _class_names
    )


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):

    if not isinstance(
        image,
        Image.Image
    ):

        image = Image.open(
            image
        )

    image = image.convert(
        "RGB"
    )

    image = image.resize(
        IMG_SIZE
    )

    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    # MobileNetV2 preprocessing
    image_array = (
        tf.keras.applications
        .mobilenet_v2
        .preprocess_input(
            image_array
        )
    )

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

    processed_image = (
        preprocess_image(
            image
        )
    )

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

        raw_category = (
            class_names[index]
        )

        confidence = (
            float(
                probabilities[index]
            ) * 100
        )

        display_category = (
            DISPLAY_NAMES.get(
                raw_category,
                raw_category
                .replace("_", " ")
                .title()
            )
        )

        top_predictions.append({

            "category":
                display_category,

            "raw_category":
                raw_category,

            "confidence":
                round(
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

        category = (
            "Uncertain / Needs Review"
        )

    else:

        category = best["category"]

    return {

        "category":
            category,

        "raw_category":
            best["raw_category"],

        "confidence":
            best["confidence"],

        "top_predictions":
            top_predictions,
    }