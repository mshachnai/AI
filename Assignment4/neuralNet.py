from PIL import Image
import numpy as np
import math 
class Layer:
    def __init__(self, MRow, MCol):

        #matrix is size matRow, matCol
        #initialize all weights to 1 for now
        self.weights = [[1 for i in range(MCol)] for j in range(MRow)]
        
        def forwardPropagate(Input):
            #calculate effect of weights on input
            weights_on_input= np.matmul(self.weights, Input)
            
            func = self.sigmoid #choose the function
            return map(func, weights_on_input) #apply the function

        def sigmoid(x):
            return 1/(1+ math.exp(-1 *x))

class Net:
    def __init__(self, hWidth, hDepth):
        self.layers = []
        self.buildNet(hWidth, hDepth)


    def buildNet(hiddenWidth, hiddenDepth):
        #input is the 8 pixels surrounding the pixel that we're trying to predict + that pixel = 9
        #so the input layer will have 9 nodes
        #each subsequent layer will have <hiddenWidth> nodes 
        #we represent this by coding a 20 x 9 matrix into our first "Layer" object.
        firstLayer = Layer(hiddenWidth, 0)
        self.layers.append(firstLayer)

        for i in range(hiddenDepth-1):
            layer = Layer(hiddenWidth, hiddenWidth)
            self.layers.append(layer)

        #we need 3 output nodes for R,G,B 
        lastLayer = Layer(3,20)
        self.layers.append(lastLayer)

    def feedForwardAllLayers(vec):
        for layer in self.layers:
            vec = layer.forwardPropagate(vec) 
        return vec

    def backPropagate():
        pass


    def runNetOneRound(vec):
        result = self.feedForwardAllLayers(vec)
        self.backPropagate()    

#returns a matrix of values
def getTrainingDataFromImage(imgName):
    #open image 
    img = Image.open(imgName)
    #turn image to grayscale
    grey = img.convert('L')

    #convert image to matrix (numpy array)
    greyMatrix = np.array(grey)
    (row,col) = greyMatrix.shape


    #turn image into RGB
    img_rgb = img.convert('RGB')
    
    colorMatrix = [[0 for i in range(col)] for j in range(row)]

    for i in range(row):
        for j in range(col):
            r, g, b = img_rgb.getpixel((j, i)) #TODO: double check that this works 
            colorMatrix[i][j] = (r,g,b)

    #print(colorRes)
    #print(greyMatrix)

    #ok, so we have rgb/grey values in an array!
    #every "window" where P is the pixel we're trying to predict will contain data formatted as follows:
    """
    C is the color value in the center. 
    the grey matrix window centered at 9 looks like:
    1 | 2 | 3
    _   _   _
    8 | 9 | 4   => (C,[1,2,3,4,5,6,7,8,9])
    _   _   _
    7 | 6 | 5

    TODO: since this probably won't predict very well, maybe increase window size
    """
    trainingData = [[0 for i in range(col-1)] for j in range(row-1)]
    for i in range(1,row-1):
        for j in range(1,col-1):
            colorVal = colorMatrix[i][j]
            greyVals = [greyMatrix[i-1][j-1],
                            greyMatrix[i-1][j],
                            greyMatrix[i-1][j+1],
                            greyMatrix[i][j+1],
                            greyMatrix[i+1][j+1],
                            greyMatrix[i+1][j],
                            greyMatrix[i+1][j-1],
                            greyMatrix[i][j-1],
                            greyMatrix[i][j]]
            greyVals = np.transpose(greyVals) 
            trainingData[i][j] = (colorVal, greyVals)

    """
    #test if the previous logic works
    X = [[1,2,3],
        [8,100,4],
        [7,6,5]]

    i = 1
    j = 1
    test = (X[i-1][j-1],
                    X[i-1][j],
                    X[i-1][j+1],
                    X[i][j+1],
                    X[i+1][j+1],
                    X[i+1][j],
                    X[i+1][j-1],
                    X[i][j-1])
    print(test)
    """
    return trainingData

if __name__ == "__main__":
    trainingData = getTrainingDataFromImage('simpson.png')



            
