def create_spark_session(app_name: str):
    """Create the Spark session used by the image feature extraction pipeline."""
    from pyspark.sql import SparkSession

    return SparkSession.builder.appName(app_name).getOrCreate()
