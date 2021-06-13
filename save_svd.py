import numpy as np
from PIL import Image


image = Image.open("data/IMG_5058.jpeg").convert(mode='L')

mat = np.array(image)
u, s, vt = np.linalg.svd(mat)
np.save("data/svd_u", u)
np.save("data/svd_s", s)
np.save("data/svd_vt", vt)
