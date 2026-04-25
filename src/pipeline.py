from pathlib import Path
from typing import Optional, Union

from .config import LOCAL_IMAGE_DIR, LOCAL_RESULT_DIR, SPARK_APP_NAME
from .image_features import (
    extract_features,
    extract_label_from_path,
    prepare_feature_extractor,
)
from .spark_session import create_spark_session


def _to_spark_path(path: Union[str, Path]) -> str:
    if isinstance(path, Path):
        return path.as_posix()
    return path


def _create_featurize_udf(broadcast_weights):
    from pyspark.sql.functions import PandasUDFType, pandas_udf

    @pandas_udf("array<float>", PandasUDFType.SCALAR_ITER)
    def featurize_udf(content_series_iter):
        model = prepare_feature_extractor(model_weights=broadcast_weights.value)
        for content_series in content_series_iter:
            yield extract_features(model, content_series)

    return featurize_udf


def run_pipeline(
    input_path: Union[str, Path] = LOCAL_IMAGE_DIR,
    output_path: Union[str, Path] = LOCAL_RESULT_DIR,
    app_name: str = SPARK_APP_NAME,
    repartition_count: Optional[int] = 20,
):
    """Run the local feature extraction pipeline and write results as Parquet."""
    from pyspark.sql.functions import col, udf
    from pyspark.sql.types import StringType

    spark = create_spark_session(app_name)

    images = (
        spark.read.format("binaryFile")
        .option("pathGlobFilter", "*.jpg")
        .option("recursiveFileLookup", "true")
        .load(_to_spark_path(input_path))
    )

    label_udf = udf(extract_label_from_path, StringType())
    images_with_labels = images.withColumn("label", label_udf(col("path")))

    feature_extractor = prepare_feature_extractor()
    broadcast_weights = spark.sparkContext.broadcast(feature_extractor.get_weights())
    featurize_udf = _create_featurize_udf(broadcast_weights)

    if repartition_count:
        images_with_labels = images_with_labels.repartition(repartition_count)

    features_df = images_with_labels.select(
        col("path"),
        col("label"),
        featurize_udf("content").alias("features"),
    )

    features_df.write.mode("overwrite").parquet(_to_spark_path(output_path))
    return features_df


if __name__ == "__main__":
    run_pipeline()
