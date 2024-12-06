import numpy as np


def mirrorAxis(picture, verticalFlip: bool = True, pos=0.5,  flip=False):
    """
    Mirror image along axis in given position.

    :param picture: array, 2d, 3d

    :param verticalFlip: bool
            True - Image will be mirrored up-down
            False - Image will be mirrored left-right

    :param pos: Float or Int
            Float - <0, 1> Axis position = number * dimention.
            Int - <0, MaxDimension> Image position

    :param flip: bool, flip other direction

    :return:

    """

    if len(picture.shape) == 3:
        h, w, c = picture.shape
    else:
        h, w = picture.shape

    if isinstance(pos, int):
        if verticalFlip:
            center = np.clip(pos, 0, h)
        else:
            center = np.clip(pos, 0, w)

    elif isinstance(pos, float):
        if verticalFlip:
            center = np.round(h * pos).astype(int)
        else:
            center = np.round(w * pos).astype(int)
    else:
        raise ValueError("Pos must be int or float")

    if verticalFlip:
        "Vertical mirror"
        if center == h or center == 0:
            "EDGE CASES"
            return np.flipud(picture)
        first = picture[:center, :]
        second = picture[center:, :]

    else:
        "Horizontal Mirror"
        if center == w or center == 0:
            "EDGE CASES"
            return np.fliplr(picture)
        first = picture[:, :center]
        second = picture[:, center:]

    " NORMAL MIRROR "
    if verticalFlip:
        if flip:
            first = np.flipud(second)
        else:
            second = np.flipud(first)

    else:
        if flip:
            first = np.fliplr(second)
        else:
            second = np.fliplr(first)

    axis = 0 if verticalFlip else 1
    combined = np.concatenate([first, second], axis=axis)

    return combined


__all__ = [
    'mirrorAxis',
]


if __name__ == "__main__":
    import cv2 as _cv2
    import os
    img = _cv2.imread(os.path.join(os.path.dirname(__file__), "cat.jpg"))

    count = 0
    imFlip = mirrorAxis(img, False, 0.3, False)

    "Loop checking"
    for pos in [0.2, 0, 400, 0.8]:
        for verticalFlip in [False, True]:
            for flip in [False, True]:
                print()
                imFlip = mirrorAxis(img, verticalFlip, pos, flip)
                # _cv2.imshow(str(count), imFlip)
                count += 1

    # mir1 = mirrorAxis(img, )
    # mir2 = mirrorAxis(img, flip=True)
    # _cv2.imshow("Orig", img)
    # _cv2.imshow("Smol1", mir1)
    # _cv2.imshow("Smol2", mir2)

    # _cv2.waitKey()
