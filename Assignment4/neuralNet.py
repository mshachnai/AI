import os
from PIL import Image
import numpy as np

class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(3,3) 
        self.weights2   = np.random.rand(3,3)                 
        self.y          = y
        self.output     = np.zeros(3)

    def feedforward(self):
        self.hiddenLayer = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.hiddenLayer, self.weights2))

    def backprop(self):

        self.weights2 += np.dot(self.hiddenLayer.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        self.weights1 += np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.hiddenLayer)))

def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

def sigmoid_derivative(x):
    return x * (1.0 - x)

if __name__ == "__main__":

    nn = NeuralNetwork( np.array([[0,0,0],
                        [0,0,0],
                        [0,0,0]]),
                       
                        np.array( [0,0,0] )   )

    for l in range(20):
        for k in range(20):
            photo = Image.open('%d.jpg' % k)
            photo = photo.convert('RGB')
            grayVersion = photo.convert('L')
            grayMatrix = np.array(grayVersion)

            width = photo.size[0] #define W and H
            height = photo.size[1]

            #training our NN with all the pixel sets of a certain image
            for j in range(1, height-1): #each pixel's coordinates

                for i in range(1, width-1):

                    RGB = photo.getpixel((i,j))
                    R,G,B = RGB  #current pixel's RGB value

                    inputMatrix = np.array([[grayMatrix[j-1][i-1],grayMatrix[j-1][i],grayMatrix[j-1][i+1]],
                                            [grayMatrix[j][i-1],grayMatrix[j][i],grayMatrix[j][i+1]],
                                            [grayMatrix[j+1][i-1],grayMatrix[j+1][i],grayMatrix[j+1][i+1]]])
                    actualRGB = np.array([R,G,B])

                    nn.input = inputMatrix
                    nn.y = actualRGB

                    nn.feedforward()
                    nn.backprop()

    #running our NN on a given input
    photo = Image.open('2.jpg')
    grayVersion = photo.convert('L')
    grayMatrix = np.array(grayVersion)

    width = photo.size[0]
    height = photo.size[1]

    finalSolution = np.random.rand(height,width,3)
    
    for j in range(1, height-1): #each pixel's coordinates

        for i in range(1, width-1):

            inputMatrix = np.array([[grayMatrix[j-1][i-1],grayMatrix[j-1][i],grayMatrix[j-1][i+1]],
                                        [grayMatrix[j][i-1],grayMatrix[j][i],grayMatrix[j][i+1]],
                                        [grayMatrix[j+1][i-1],grayMatrix[j+1][i],grayMatrix[j+1][i+1]]])
            nn.feedforward()

            finalSolution[j][i][0] = nn.output[0][0] #(r)
            finalSolution[j][i][1] = nn.output[1][0] #(b)
            finalSolution[j][i][2] = nn.output[2][0] #(g)
            
    grey = Image.fromarray(finalSolution, mode="RGB")
    grey.save('output.png')
    grey.show()
