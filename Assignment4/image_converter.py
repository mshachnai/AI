#Image converter from color to greyscale

from PIL import Image
import numpy as np

img_matrix = []

#open image 
img = Image.open('simpson.png')
#turn image to grayscale
grey = img.convert('L')
#convert image to matrix (numpy array)
img_matrix = np.array(grey)
#print info about matrix (size and type)
print(img_matrix.shape)
print(img_matrix.dtype)

#convert numpy array back to image
grey = Image.fromarray(img_matrix)
grey.save('output.png')
grey.show()



#img_matrix1 = np.array(img)
#print(img_matrix1.shape)
#print(img_matrix1.dtype)
#img.show()

