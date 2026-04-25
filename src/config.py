from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOCAL_IMAGE_DIR = PROJECT_ROOT / "data" / "fruits-360_dataset" / "fruits-360" / "Test"
LOCAL_RESULT_DIR = PROJECT_ROOT / "data" / "Results"

IMAGE_SIZE = (224, 224)
SPARK_APP_NAME = "Spark Vision Feature Extraction"
