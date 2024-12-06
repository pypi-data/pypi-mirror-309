import pytest
from yasiu_image.filters import mirrorAxis

import numpy as np


@pytest.fixture()
def blank_image_flat():
    img = np.zeros((300, 300), dtype=np.uint8)
    return img


@pytest.fixture()
def blank_image_gray():
    img = np.zeros((300, 300, 1), dtype=np.uint8)
    return img


@pytest.fixture()
def blank_image():
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    return img


tests_params = [
        (val, ax, flag)
        for val in [*np.linspace(0, 1, 15), *range(290, 310), *range(-15, 20)]
        for ax in [0, 1]
        for flag in [False, True]
]


# @pytest.fixture()
# def all_img_types():
#     image_params = [blank_image(), blank_image_gray(), blank_image_flat()]
#     return image_params


@pytest.mark.parametrize('val,ax,flag', tests_params)
@pytest.mark.parametrize('image', ['blank_image', 'blank_image_flat', 'blank_image_gray'])
def test_1(image, val, ax, flag, request):
    image = request.getfixturevalue(image)
    # print(image)
    # print(image.shape)
    # raise ValueError
    ret = mirrorAxis(image, pos=val, verticalAxis=ax, flip=flag)
    assert ret.shape == image.shape, "Shape must be true"
    # assert (image == ret).all(), "Returned diff image"
