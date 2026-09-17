import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
)

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = r"E:\Greensight"

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "waste_classifier.keras"
)

CLASS_PATH = os.path.join(
    MODEL_DIR,
    "class_names.json"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
SEED = 42

# Reasonable training time for today's build
INITIAL_EPOCHS = 12
FINE_TUNE_EPOCHS = 8

EXPECTED_CLASSES = [
    "cardboard",
    "e_waste",
    "general",
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic",
    "textile",
]

# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

# ============================================================
# DEVICE CHECK
# ============================================================

print("\n" + "=" * 60)
print("VERDESIGHT AI — MODEL TRAINING")
print("=" * 60)

print("\nDEVICE CHECK")
print("-" * 60)

gpus = tf.config.list_physical_devices("GPU")

if gpus:
    print("GPU detected:")
    for gpu in gpus:
        print(" ", gpu)
else:
    print("GPU not detected.")
    print("Training will use CPU.")

# ============================================================
# CHECK DATASET
# ============================================================

print("\nDATASET CHECK")
print("-" * 60)

if not os.path.exists(DATASET_DIR):
    raise FileNotFoundError(
        f"\nDataset folder not found:\n{DATASET_DIR}"
    )

dataset_folders = sorted(
    [
        folder
        for folder in os.listdir(DATASET_DIR)
        if os.path.isdir(
            os.path.join(DATASET_DIR, folder)
        )
    ]
)

print("Detected folders:")

for folder in dataset_folders:
    print(" ", folder)

missing_classes = [
    cls
    for cls in EXPECTED_CLASSES
    if cls not in dataset_folders
]

if missing_classes:
    raise ValueError(
        "\nMissing expected classes:\n"
        + "\n".join(
            f" - {cls}"
            for cls in missing_classes
        )
    )

# ============================================================
# IMAGE COUNT
# ============================================================

print("\nIMAGE COUNTS")
print("-" * 60)

valid_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
)

image_counts = {}

for class_name in EXPECTED_CLASSES:

    class_path = os.path.join(
        DATASET_DIR,
        class_name
    )

    count = 0

    for root, _, files in os.walk(class_path):

        for file in files:

            if file.lower().endswith(
                valid_extensions
            ):
                count += 1

    image_counts[class_name] = count

    print(
        f"{class_name:<12} : {count:>5} images"
    )

total_images = sum(
    image_counts.values()
)

print("-" * 60)
print(
    f"TOTAL        : {total_images:>5} images"
)

if total_images < 1000:
    raise ValueError(
        "Dataset is too small for reliable training."
    )

# ============================================================
# LOAD TRAINING DATA
# ============================================================

print("\n" + "=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.20,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
)

# ============================================================
# LOAD VALIDATION DATA
# ============================================================

print("\nLoading validation data...")

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.20,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
)

# ============================================================
# CLASS NAMES
# ============================================================

class_names = train_ds.class_names

print("\n" + "=" * 60)
print("MODEL CLASSES")
print("=" * 60)

for index, name in enumerate(class_names):
    print(f"{index}: {name}")

NUM_CLASSES = len(class_names)

if NUM_CLASSES != 9:
    raise ValueError(
        f"Expected 9 classes, but found {NUM_CLASSES}."
    )

# ============================================================
# SAVE CLASS MAPPING
# ============================================================

with open(
    CLASS_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        class_names,
        file,
        indent=4
    )

print(
    f"\nClass mapping saved to:\n{CLASS_PATH}"
)

# ============================================================
# PERFORMANCE PIPELINE
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(
    AUTOTUNE
)

val_ds = val_ds.prefetch(
    AUTOTUNE
)

# ============================================================
# CLASS WEIGHTS
# ============================================================

print("\n" + "=" * 60)
print("CLASS WEIGHTS")
print("=" * 60)

# Weight = total images / (number of classes * class images)
class_weights = {}

for index, class_name in enumerate(class_names):

    count = image_counts[class_name]

    weight = (
        total_images
        / (NUM_CLASSES * count)
    )

    class_weights[index] = weight

    print(
        f"{class_name:<12} : {weight:.3f}"
    )

# ============================================================
# DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip(
            "horizontal"
        ),

        layers.RandomRotation(
            0.12
        ),

        layers.RandomZoom(
            0.12
        ),

        layers.RandomTranslation(
            0.08,
            0.08
        ),

        layers.RandomContrast(
            0.12
        ),
    ],
    name="data_augmentation"
)

# ============================================================
# BASE MODEL
# ============================================================

print("\n" + "=" * 60)
print("LOADING MOBILENETV2")
print("=" * 60)

base_model = MobileNetV2(
    input_shape=(
        224,
        224,
        3
    ),
    include_top=False,
    weights="imagenet",
)

# Freeze initially
base_model.trainable = False

# ============================================================
# MODEL ARCHITECTURE
# ============================================================

inputs = layers.Input(
    shape=(
        224,
        224,
        3
    ),
    name="image_input"
)

x = data_augmentation(
    inputs
)

x = tf.keras.applications.mobilenet_v2.preprocess_input(
    x
)

x = base_model(
    x,
    training=False
)

x = layers.GlobalAveragePooling2D()(x)

x = layers.BatchNormalization()(x)

x = layers.Dense(
    256,
    activation="relu"
)(x)

x = layers.Dropout(
    0.40
)(x)

x = layers.Dense(
    128,
    activation="relu"
)(x)

x = layers.Dropout(
    0.30
)(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax",
    name="waste_class"
)(x)

model = models.Model(
    inputs,
    outputs
)

# ============================================================
# MODEL SUMMARY
# ============================================================

print("\nMODEL SUMMARY")
print("-" * 60)

model.summary()

# ============================================================
# COMPILE — STAGE 1
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-4
    ),

    loss="sparse_categorical_crossentropy",

    metrics=[
        "accuracy"
    ],
)

# ============================================================
# CALLBACKS
# ============================================================

callbacks = [

    ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1,
    ),

    EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
        verbose=1,
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=2,
        min_lr=1e-7,
        verbose=1,
    ),
]

# ============================================================
# STAGE 1 — TRANSFER LEARNING
# ============================================================

print("\n" + "=" * 60)
print("STAGE 1 — TRANSFER LEARNING")
print("=" * 60)

history1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=INITIAL_EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks,
)

# ============================================================
# STAGE 2 — FINE TUNING
# ============================================================

print("\n" + "=" * 60)
print("STAGE 2 — FINE TUNING")
print("=" * 60)

base_model.trainable = True

# Freeze early layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Keep BatchNorm layers frozen
for layer in base_model.layers:

    if isinstance(
        layer,
        layers.BatchNormalization
    ):
        layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),

    loss="sparse_categorical_crossentropy",

    metrics=[
        "accuracy"
    ],
)

history2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks,
)

# ============================================================
# LOAD BEST CHECKPOINT
# ============================================================

print("\n" + "=" * 60)
print("LOADING BEST MODEL")
print("=" * 60)

if os.path.exists(MODEL_PATH):

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        "Best validation model loaded."
    )

else:

    model.save(
        MODEL_PATH
    )

    print(
        "Model saved."
    )

# ============================================================
# FINAL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL EVALUATION")
print("=" * 60)

loss, accuracy = model.evaluate(
    val_ds,
    verbose=1
)

print(
    f"\nValidation Accuracy : "
    f"{accuracy * 100:.2f}%"
)

print(
    f"Validation Loss     : "
    f"{loss:.4f}"
)

# ============================================================
# FINAL FILE CHECK
# ============================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"\nModel saved at:"
    f"\n{MODEL_PATH}"
)

print(
    f"\nClass mapping saved at:"
    f"\n{CLASS_PATH}"
)

print("\nClasses:")

for index, name in enumerate(class_names):

    print(
        f"  {index} → {name}"
    )

print(
    "\nVerdeSight AI model is ready for inference."
)

