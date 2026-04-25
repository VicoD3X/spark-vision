from src import config


def test_local_paths_target_expected_project_directories():
    assert config.LOCAL_IMAGE_DIR.as_posix().endswith(
        "data/fruits-360_dataset/fruits-360/Test"
    )
    assert config.LOCAL_RESULT_DIR.as_posix().endswith("data/Results")


def test_mobilenet_image_size_and_spark_app_name_are_defined():
    assert config.IMAGE_SIZE == (224, 224)
    assert config.SPARK_APP_NAME == "Spark Vision Feature Extraction"
