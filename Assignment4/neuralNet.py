from util import printM
from PIL import Image
import numpy as np
import math 

TEST_SIZE = 200 #test NN on smaller pic before we commit to a 1000 pixel monstrosity
SET_SIZE = 5 #training batch size, i guess
LAMBDA = 0 #minimize loss? 0 =danger of overfitting
class Layer:
    def __init__(self, MRow, MCol):

        #matrix is size matRow, matCol
        #initialize all weights to 1 for now. TODO: random weights?
        self.weights = [[0.5 for i in range(MCol)] for j in range(MRow)]
        self.activation = [0 for i in range(MRow)] #i think this is total output of node
        self.error = [0 for i in range(MRow)]
        self.deriv = [[1 for i in range(MCol)] for j in range(MRow)]
        self.gradientMatrix = [[0 for i in range(MCol)] for j in range(MRow)]

    def forwardPropagate(self, Input):
        #calculate effect of weights on input
        weights_on_input= np.dot(self.weights, Input)
        func = sigmoid #choose the function
        return list(map(func, weights_on_input)) #apply the function


class Net:
    def __init__(self, hWidth, hDepth):
        self.layers = []
        self.buildNet(hWidth, hDepth)


    def buildNet(self,hiddenWidth, hiddenDepth):
        #input is the 8 pixels surrounding the pixel that we're trying to predict + that pixel = 9
        #so the input layer will have 9 nodes
        #each subsequent layer will have <hiddenWidth> nodes 
        #we represent this by coding a 20 x 9 matrix into our first "Layer" object.
        firstLayer = Layer(hiddenWidth, 9)
        self.layers.append(firstLayer)

        for i in range(hiddenDepth-1):
            layer = Layer(hiddenWidth, hiddenWidth)
            self.layers.append(layer)


        #we need 3 output nodes for R,G,B 
        lastLayer = Layer(3,hiddenWidth)
        self.layers.append(lastLayer)

    def feedForwardAllLayers(self, vec): #in the beginning, vec is the input vector
        for i in range(len(self.layers)):
            layer = self.layers[i]
            vec = layer.forwardPropagate(vec) 
            layer.activation = vec
            """ 
            print("feedForwardAllLayers: layer: " + str(i))
            print("activation is:")
            print(layer.activation)
            input()
            """
        return vec

    def backPropagate(self, actualVals, inputVec): #actualVals is the desired output vector
        self.clearGradientMatrices()
        numLayers = len(self.layers) #number of trainable layers
        self.calculateLastLayerLoss( numLayers -1, actualVals)
        for i in range(numLayers -1):  #numlayers = 3 (for i in range(2)) -> [0,1]
            self.calculateHiddenLayerLoss(numLayers-2-i) #3-2-0 = 1 3-2-1 = 0 OK

        #now the loss (err) for all layers has been calculated. 
        #calculate the gradients.
        self.calculateDeltas(inputVec)

    def calculateLastLayerLoss(self, layerNum, actualVals):
        print("Output layer loss Calculating -> check value later")
        layer = self.layers[layerNum]
        layer.error = np.subtract(layer.activation, actualVals)
      
        """
        #TODO: is this right? should i do mean-square err?
        print("layer number " + str(layerNum))
        print(layer.error)
        input()
        """

    def calculateHiddenLayerLoss(self, layerNum): #sets layer.error
        print("Hidden layer loss Calculating -> check value")
        layer = self.layers[layerNum]
        nextLayer = self.layers[layerNum+1]
        X = np.dot(np.transpose(nextLayer.weights), nextLayer.error)
        onesVec = [1 for i in range(len(layer.activation))]
        NLD = np.multiply(layer.activation, np.subtract(onesVec,layer.activation))
        """
        print("NLD")
        printM(NLD)
        print("layer activation")
        printM(layer.activation)
        """
        layer.error = np.multiply(X, NLD)
        """
        print("layer number " + str(layerNum))
        print(layer.error)
        input()
        """

    def calculateDeltas(self, inputVec):
        print("Gradient Calculating")
        prevLayerActivation = inputVec

        #do some weird off-by-one thing, sorry
        for k in range(len(self.layers)):
            
            layer = self.layers[k]
            """
            #I have reason to believe that the video is wrong about this equation
            #print(prevLayerActivation)
            print("layer error: ")
            print(layer.error)
            """

            #PROD = np.dot(layer.error, np.transpose(prevLayerActivation)) 
            PROD = np.dot(np.transpose([layer.error]), [prevLayerActivation])
            #TODO: yea so in the middle layer, both of these vectors have the
            #same numbers in all positions, so the layer isn't training properly
            layer.gradientMatrix = np.add(layer.gradientMatrix, PROD)
            prevLayerActivation = layer.activation

            """
            print("calculateDeltas: at layer " + str(k))
            print("PROD is:")
            printM(PROD)
            print("layer.gradientMatrix is: " )
            printM(layer.gradientMatrix)
        
            print("activation: ")
            print(layer.activation)
            print("??")
            input()
            """

    def clearGradientMatrices(self):
        for layer in self.layers:
            uwu = layer.gradientMatrix
            for i in range(len(uwu)):
                for j in range(len(uwu[0])):
                    layer.gradientMatrix[i][j] = 0

    def gradientDescent(self):
        print("Gradient Descending")
        for layer in self.layers:
            layer.gradientMatrix = np.multiply(layer.gradientMatrix, (float)(1/SET_SIZE))
            layer.weights = np.subtract(layer.weights, layer.gradientMatrix)
            
            """ 
            print("gradientMatrix: ")
            printM(layer.gradientMatrix)
            input()
            """

    def runNetOneSet(self,Set):
        for data in Set:
            print("Forward Propagating")
            result = self.feedForwardAllLayers(data[1])
            print("Back Propagating")
            self.backPropagate(data[0], data[1])
            print("Set Complete!")
        
        self.gradientDescent()
        print("In runNetOneSet: Total Error: ")
        print((self.layers[len(self.layers)-1]).error)
        input()


def sigmoid(x):
    return 1/(1+ math.exp(-1 *x))

#returns a matrix of values
def getTrainingDataFromImage(imgName):

    #TESTING ONLY
    return [([1,2,3],[1,2,3,4,5,6,7,8,9]) for i in range(300)]


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

def train():
    #create neural net
    print("Created neural net")
    net = Net(6,2)

    #get a matrix of training data
    trainingData = getTrainingDataFromImage('simpson.png')
    sets = divideTrainingDataIntoSets(trainingData)

    print("aa")

    print("Commence training")
    for Set in sets:
        net.runNetOneSet(Set)

#returns an array
def divideTrainingDataIntoSets(trainingData):
    #divide the training data into sets of 50

    print("Dividing training data into sets")

    sets = []
    trainLen = len(trainingData)
    i = 0
    while i < TEST_SIZE: #TODO: this will break if the number of data points is less than TEST_SIZE
        j = 0
        newSet = []
        while j < SET_SIZE:
            if i >= trainLen:
                break

            newSet.append(trainingData[i])
            j+=1
            i+=1
        sets.append(newSet)

    return sets

       


if __name__ == "__main__":
    train()


            
