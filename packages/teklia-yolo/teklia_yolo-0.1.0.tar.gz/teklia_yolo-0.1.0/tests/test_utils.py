import pytest

from teklia_yolo.extract.utils import download_image, get_bbox
from tests import FIXTURES


@pytest.mark.parametrize("thumbnail", [None, 320])
def test_download_image_thumbnail(thumbnail, tmp_path, responses):
    source = FIXTURES / "427x640.jpg"
    expected_path = (
        FIXTURES / f"{source.stem}-{'not-' if not thumbnail else ''}thumbnail.jpg"
    )
    output_path = tmp_path / expected_path.name

    iiif_url = "https://iiif.url/cat.jpg/full/full/0/default.jpg"
    responses.add(responses.GET, iiif_url, body=source.read_bytes())

    download_image(
        iiif_url,
        output_path,
        resize=[thumbnail, thumbnail] if thumbnail else None,
    )

    assert output_path.read_bytes() == expected_path.read_bytes()


@pytest.mark.parametrize(
    ("thumbnail", "source"),
    [(320, FIXTURES / "427x640.jpg"), (640, FIXTURES / "214x320.jpg")],
)
def test_download_image_padding(thumbnail, source, tmp_path, responses):
    expected_path = FIXTURES / f"{source.stem}-padding.jpg"
    output_path = tmp_path / expected_path.name

    iiif_url = "https://iiif.url/cat.jpg/full/full/0/default.jpg"
    responses.add(responses.GET, iiif_url, body=source.read_bytes())

    download_image(
        iiif_url,
        output_path,
        resize=[thumbnail, thumbnail],
        padding=True,
    )

    assert output_path.read_bytes() == expected_path.read_bytes()


@pytest.mark.parametrize(
    ("ark_poly", "iiif_bbox"),
    [
        # Rectangle
        ("[[0, 0], [0, 3453], [2218, 3453], [2218, 0], [0, 0]]", "0,0,2218,3453"),
        # Polygon
        ("[[0, 0], [0, 4000], [2000, 3000], [2000, 0], [0, 0]]", "0,0,2000,4000"),
    ],
)
def test_get_bbox(ark_poly, iiif_bbox):
    assert get_bbox(ark_poly) == iiif_bbox
