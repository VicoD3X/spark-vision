import pytest

from src.image_features import extract_label_from_path


@pytest.mark.parametrize(
    ("image_path", "expected_label"),
    [
        (
            "data/fruits-360_dataset/fruits-360/Test/Apple Braeburn/321_100.jpg",
            "Apple Braeburn",
        ),
        (
            r"D:\CloneGit\spark-vision\data\fruits-360_dataset"
            r"\fruits-360\Test\Kiwi\1_100.jpg",
            "Kiwi",
        ),
        ("s3://spark-vision-bucket/Test/Banana/45_100.jpg", "Banana"),
    ],
)
def test_extract_label_from_path(image_path, expected_label):
    assert extract_label_from_path(image_path) == expected_label


def test_extract_label_from_path_rejects_invalid_path():
    with pytest.raises(ValueError):
        extract_label_from_path("image.jpg")
