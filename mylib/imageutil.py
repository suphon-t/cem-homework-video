import numpy as np
from PIL import Image


def load_svd():
    u = np.load("data/svd_u.npy")
    s = np.load("data/svd_s.npy")
    s = np.diag(s)
    vt = np.load("data/svd_vt.npy")
    return [u, s, vt]


def construct_image(k):
    [u, s, vt] = load_svd()

    u_sigma = np.matmul(u[:, 0:k], s[0:k, 0:k])
    result = np.matmul(u_sigma, vt[0:k, :])
    return Image.fromarray(result, mode=None)


def original_image():
    return Image.open("data/IMG_5058.jpeg").convert(mode='RGB')


def scale_image(image):
    scale = 0.2
    image = image.copy()
    size = image.size
    new_size = (int(size[0] * scale), int(size[1] * scale))
    image.thumbnail(new_size)
    return image


def to_image(arr):
    return Image.fromarray(arr, mode=None)
