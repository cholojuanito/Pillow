"""Test DdsImagePlugin"""
from io import BytesIO

import pytest

from PIL import DdsImagePlugin, Image

from .helper import assert_image_equal, assert_image_equal_tofile

TEST_FILE_DXT1 = "Tests/images/dxt1-rgb-4bbp-noalpha_MipMaps-1.dds"
TEST_FILE_DXT3 = "Tests/images/dxt3-argb-8bbp-explicitalpha_MipMaps-1.dds"
TEST_FILE_DXT5 = "Tests/images/dxt5-argb-8bbp-interpolatedalpha_MipMaps-1.dds"
TEST_FILE_DX10_BC7 = "Tests/images/bc7-argb-8bpp_MipMaps-1.dds"
TEST_FILE_DX10_BC7_UNORM_SRGB = "Tests/images/DXGI_FORMAT_BC7_UNORM_SRGB.dds"
TEST_FILE_DX10_R8G8B8A8 = "Tests/images/argb-32bpp_MipMaps-1.dds"
TEST_FILE_DX10_R8G8B8A8_UNORM_SRGB = "Tests/images/DXGI_FORMAT_R8G8B8A8_UNORM_SRGB.dds"
TEST_FILE_UNCOMPRESSED_RGB = "Tests/images/hopper.dds"
TEST_FILE_UNCOMPRESSED_RGB_WITH_ALPHA = "Tests/images/uncompressed_rgb.dds"


def test_sanity_dxt1():
    """Check DXT1 images can be opened"""
    with Image.open(TEST_FILE_DXT1.replace(".dds", ".png")) as target:
        target = target.convert("RGBA")
    with Image.open(TEST_FILE_DXT1) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (256, 256)

        assert_image_equal(im, target)


def test_sanity_dxt5():
    """Check DXT5 images can be opened"""

    with Image.open(TEST_FILE_DXT5) as im:
        im.load()

    assert im.format == "DDS"
    assert im.mode == "RGBA"
    assert im.size == (256, 256)

    assert_image_equal_tofile(im, TEST_FILE_DXT5.replace(".dds", ".png"))


def test_sanity_dxt3():
    """Check DXT3 images can be opened"""

    with Image.open(TEST_FILE_DXT3) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (256, 256)

        assert_image_equal_tofile(im, TEST_FILE_DXT3.replace(".dds", ".png"))


def test_dx10_bc7():
    """Check DX10 images can be opened"""

    with Image.open(TEST_FILE_DX10_BC7) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (256, 256)

        assert_image_equal_tofile(im, TEST_FILE_DX10_BC7.replace(".dds", ".png"))


def test_dx10_bc7_unorm_srgb():
    """Check DX10 unsigned normalized integer images can be opened"""

    with Image.open(TEST_FILE_DX10_BC7_UNORM_SRGB) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (16, 16)
        assert im.info["gamma"] == 1 / 2.2

        assert_image_equal_tofile(
            im, TEST_FILE_DX10_BC7_UNORM_SRGB.replace(".dds", ".png")
        )


def test_dx10_r8g8b8a8():
    """Check DX10 images can be opened"""

    with Image.open(TEST_FILE_DX10_R8G8B8A8) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (256, 256)

        assert_image_equal_tofile(im, TEST_FILE_DX10_R8G8B8A8.replace(".dds", ".png"))


def test_dx10_r8g8b8a8_unorm_srgb():
    """Check DX10 unsigned normalized integer images can be opened"""

    with Image.open(TEST_FILE_DX10_R8G8B8A8_UNORM_SRGB) as im:
        im.load()

        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (16, 16)
        assert im.info["gamma"] == 1 / 2.2

        assert_image_equal_tofile(
            im, TEST_FILE_DX10_R8G8B8A8_UNORM_SRGB.replace(".dds", ".png")
        )


def test_unimplemented_dxgi_format():
    with pytest.raises(NotImplementedError):
        with Image.open("Tests/images/unimplemented_dxgi_format.dds"):
            pass


def test_uncompressed_rgb():
    """Check uncompressed RGB images can be opened"""

    # convert -format dds -define dds:compression=none hopper.jpg hopper.dds
    with Image.open(TEST_FILE_UNCOMPRESSED_RGB) as im:
        assert im.format == "DDS"
        assert im.mode == "RGB"
        assert im.size == (128, 128)

        assert_image_equal_tofile(im, "Tests/images/hopper.png")

    # Test image with alpha
    with Image.open(TEST_FILE_UNCOMPRESSED_RGB_WITH_ALPHA) as im:
        assert im.format == "DDS"
        assert im.mode == "RGBA"
        assert im.size == (800, 600)

        assert_image_equal_tofile(
            im, TEST_FILE_UNCOMPRESSED_RGB_WITH_ALPHA.replace(".dds", ".png")
        )


def test__accept_true():
    """Check valid prefix"""
    # Arrange
    prefix = b"DDS etc"

    # Act
    output = DdsImagePlugin._accept(prefix)

    # Assert
    assert output


def test__accept_false():
    """Check invalid prefix"""
    # Arrange
    prefix = b"something invalid"

    # Act
    output = DdsImagePlugin._accept(prefix)

    # Assert
    assert not output


def test_short_header():
    """ Check a short header"""
    with open(TEST_FILE_DXT5, "rb") as f:
        img_file = f.read()

    def short_header():
        with Image.open(BytesIO(img_file[:119])):
            pass  # pragma: no cover

    with pytest.raises(OSError):
        short_header()


def test_short_file():
    """ Check that the appropriate error is thrown for a short file"""

    with open(TEST_FILE_DXT5, "rb") as f:
        img_file = f.read()

    def short_file():
        with Image.open(BytesIO(img_file[:-100])) as im:
            im.load()

    with pytest.raises(OSError):
        short_file()


def test_unimplemented_pixel_format():
    with pytest.raises(NotImplementedError):
        with Image.open("Tests/images/unimplemented_pixel_format.dds"):
            pass
