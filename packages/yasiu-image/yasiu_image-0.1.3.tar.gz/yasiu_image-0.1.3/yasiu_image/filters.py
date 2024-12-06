import numpy as np


def mirrorAxis(picture, horizontalMirror: bool = True, pos=0.5,  flip=False):
    """
    Mirror image along axis in given position.

    :param picture: array, 2d, 3d
    :param pos: Float or Int
            Float - <0, 1> Axis position = number * dimention.
            Int - <0, MaxDimension> Image position

    :param axis: 0=horizontal mirror, 1=vertical mirror
    :param flip: bool, flag for flipping other side

    :return:

    """
    if len(picture.shape) == 3:
        h, w, c = picture.shape
    else:
        h, w = picture.shape

    if isinstance(pos, int):
        if horizontalMirror:
            center = np.clip(pos, 0, h)
        else:
            center = np.clip(pos, 0, w)

    elif isinstance(pos, float):
        if horizontalMirror:
            center = np.round(h * pos).astype(int)
        else:
            center = np.round(w * pos).astype(int)
    else:
        raise ValueError("Pos must be int or float")

    if horizontalMirror == 0:
        "Horizontal Mirror"
        if center == h or center == 0:
            return np.flipud(picture)
        first = picture[:center]
        second = picture[center:]

        size1 = first.shape[0]
        size2 = second.shape[0]

    else:
        "Vertical mirror"
        if center == w or center == 0:
            return np.fliplr(picture)
        first = picture[:, :center]
        second = picture[:, center:]

        size1 = first.shape[1]
        size2 = second.shape[1]

    if size1 > size2:
        if horizontalMirror:
            mirrored = np.flipud(first)
            second = mirrored[:size2]
        else:
            mirrored = np.fliplr(first)
            second = mirrored[:, :size2]

    elif size2 > size1:
        if horizontalMirror:
            mirrored = np.flipud(second)
            first = mirrored[-size1:]
        else:
            mirrored = np.fliplr(second)
            first = mirrored[:, -size1:]

    elif flip:
        if horizontalMirror:
            first = np.fliplr(second)
        else:
            first = np.flipud(second)
    else:
        if horizontalMirror:
            second = np.fliplr(first)
        else:
            second = np.flipud(first)

    axis = 1 if horizontalMirror else 0
    combined = np.concatenate([first, second], axis=axis)

    return combined


__all__ = [
    'mirrorAxis',
]


if __name__ == "__main__":
    import cv2 as _cv2
    import os
    img = _cv2.imread(os.path.join(os.path.dirname(__file__), "cat.jpg"))

    mir1 = mirrorAxis(img, )
    mir2 = mirrorAxis(img, flip=True)
    _cv2.imshow("Orig", img)
    _cv2.imshow("Smol1", mir1)
    _cv2.imshow("Smol2", mir2)

    _cv2.waitKey()
