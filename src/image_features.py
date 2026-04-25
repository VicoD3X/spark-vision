import io
import re
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    import pandas as pd

from .config import IMAGE_SIZE


def extract_label_from_path(image_path: str) -> str:
    """Extract the image label from its parent directory."""
    parts = [part for part in re.split(r"[\\/]", image_path.strip("/\\")) if part]
    if len(parts) < 2:
        raise ValueError(f"Cannot extract label from path: {image_path}")
    return parts[-2]


def prepare_feature_extractor(model_weights: Optional[List[Any]] = None):
    """Prepare MobileNetV2 as a feature extractor without the classification layer."""
    from tensorflow.keras import Model
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2

    weights = None if model_weights is not None else "imagenet"
    base_model = MobileNetV2(
        weights=weights,
        include_top=True,
        input_shape=(*IMAGE_SIZE, 3),
    )
    for layer in base_model.layers:
        layer.trainable = False

    feature_extractor = Model(
        inputs=base_model.input,
        outputs=base_model.layers[-2].output,
    )
    if model_weights is not None:
        feature_extractor.set_weights(model_weights)

    return feature_extractor


def preprocess_image(content: bytes):
    """Preprocess raw image bytes for MobileNetV2."""
    from PIL import Image
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    from tensorflow.keras.preprocessing.image import img_to_array

    with Image.open(io.BytesIO(content)) as image:
        image = image.convert("RGB").resize(IMAGE_SIZE)
        array = img_to_array(image)

    return preprocess_input(array)


def extract_features(model: Any, content_series: "pd.Series") -> "pd.Series":
    """Extract flattened MobileNetV2 features from a pandas Series of image bytes."""
    import numpy as np
    import pandas as pd

    batch = np.stack(content_series.map(preprocess_image))
    predictions = model.predict(batch)
    return pd.Series([prediction.flatten() for prediction in predictions])
