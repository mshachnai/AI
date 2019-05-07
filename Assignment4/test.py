import numpy as np
from PIL import Image

img = Image.open('mini_pink.PNG')
arr = np.array(img)

print(arr)
