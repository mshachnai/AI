from PIL import Image
import numpy as np
import math 

SET_SIZE = 50 #training batch size, i guess
LAMBDA = 0 #minimize loss? 0 =danger of overfitting
class Layer:
    def __init__(self, MRow, MCol):

        #matrix is size matRow, matCol
        #initialize all weights to 1 for now
        self.weights = [[1 for i in range(MCol)] for j in range(MRow)]
        self.activation = [0 for i in range(MRow)] #i think this is total output of node
        self.error = [0 for i in range(MRow)]
        self.deriv = [[1 for i in range(MCol)] for j in range(MRow)]
        self.gradientMatrix = [[0 for i in range(MCol)] for j in range(MRow)]

    def forwardPropagate(Input):
        #calculate effect of weights on input
        weights_on_input= np.matmul(self.weights, Input)
        
        func = self.sigmoid #choose the function
        return map(func, weights_on_input) #apply the function

    def sigmoid(x):
        return 1/(1+ math.exp(-1 *x))
`
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

    def feedForwardAllLayers(vec): #in the beginning, vec is the input vector
        for layer in self.layers:
            vec = layer.forwardPropagate(vec) 
        return vec

    def backPropagate(actualVals, inputVec): #actualVals is the desired output vector
        numLayers = len(self.layers) #number of trainable layers
        calculateLastLayerLoss( numLayers -1, actualVals)
        for i in range(numLayers -1):  #numlayers = 3 (for i in range(2)) -> [0,1]
            calculateHiddenLayerLoss(numLayers-2-i) #3-2-0 = 1 3-2-1 = 0 OK

        #now the loss (err) for all layers has been calculated. 
        #calculate the gradients.
        calculateDeltas(inputVec)

    def calculateLastLayerLoss(layerNum, actualVals):
        layer = self.layers[layerNum]
        layer.error = np.subtract(layer.activation, actualVals)

    def calculateHiddenLayerLoss(layerNum): #sets layer.error
        layer = self.layers[layerNum]
        nextLayer = self.layers[layerNum+1]
        X = np.matmul(np.transpose(nextLayer.weights), nextLayer.error)
        NLD = np.multiply(layer.activation, (1 - layer.activation))
        layer.error = np.multiply(X, NLD)

    def calculateDeltas(inputVec):
        prevLayerActivation = inputVec

        #do some weird off-by-one thing, sorry
        for k in range(len(self.layers)):
            layer = self.layers[k]
            PROD = np.matmul(layer.error, np.transpose(prevLayerActivation))
            layer.gradientMatrix = np.add(layer.gradientMatrix, PROD)
            prevLayerActivation = layer.activation
    

    def gradientDescent():
        for layer in self.layers:
            layer.gradientMatrix = np.multiply(layer.gradientMatrix, (float)(1/SET_SIZE))
            layer.weightMatrix = np.subtract(layer.weightMatrix, layer.gradientMatrix)


    def runNetOneSet(Set):
        for data in Set:
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



            
