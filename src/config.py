import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
MODELS_DIR = os.path.join(ROOT_DIR, "models")

model_name = "yolo11s.pt"

YOLO_MODEL = os.path.join(MODELS_DIR, model_name)
YOLO_CLASSES = [0, 32]  # 0=Person, 32=Sports ball

# Analizės svoriai
WEIGHT_VISUAL = 0.6
WEIGHT_AUDIO = 0.4

# Video generavimas
TARGET_DURATION = 120
SCAN_INTERVAL = 10
BUFFER_SECONDS = 2

# Katalogai
DATA_DIR = "data"
RESULTS_DIR = "results"