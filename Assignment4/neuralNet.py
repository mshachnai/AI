from util import printM
from PIL import Image
import numpy as np
import math 

SET_SIZE = 1 #training batch size, i guess
LAMBDA = 0 #minimize loss? 0 =danger of overfitting
ALPHA = 0.01 #learning rate?

FILE = open("weights", "w+")

class Layer:
    def __init__(self, MRow, MCol):

        #matrix is size matRow, matCol
        #initialize all weights to 1 for now. TODO: random weights?
        self.weights = [[(np.random.randint(low=-100, high=100)/100.0) for i in range(MCol)] for j in range(MRow)]
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

    def train(self, imgName): #TODO:make this a training set

        #get a matrix of training data
        trainingData = getTrainingDataFromImage(imgName)
        sets = divideTrainingDataIntoSets(trainingData)
        print("Commence training")
        for Set in sets:
            self.runNetOneSet(Set)


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
        for aaa in range(len(self.layers)):
            layer = self.layers[aaa]
            layer.gradientMatrix = np.multiply(layer.gradientMatrix, (float)(1/SET_SIZE))
            layer.weights = np.subtract(layer.weights, np.multiply(layer.gradientMatrix, ALPHA))
            
            print("weights:")
            #printM(layer.weights)
            if aaa == len(self.layers) -1:
                for X in layer.weights:
                    for Y in X:
                        FILE.write((str(Y))[0:10] + "\t")
                    FILE.write("\n")

                FILE.write("------------------------------------------\n")
                FILE.write("------------------------------------------\n")

            print("gradientMatrix: ")
            #printM(layer.gradientMatrix)
            #input()
            

    def runNetOneSet(self,Set):
        #print(Set)
        for data in Set:
            #print(data)
            print("Forward Propagating")
            result = self.feedForwardAllLayers(data[1])
            print("Back Propagating")
            self.backPropagate(data[0], data[1])
            print("Set Complete!")
        
        self.gradientDescent()
        
        print("In runNetOneSet: Total Error: ")
        print((self.layers[len(self.layers)-1]).error)
        print(sum(self.layers[len(self.layers)-1].error))
        #input()


    def predict(self, imgName):
        img = Image.open(imgName)
        imgGrey = img.convert('L')

        greyMatrix = np.array(imgGrey)

        (row,col) = greyMatrix.shape

        #convert greyMatrix into a list of training data
        testData = [[0 for i in range(col-1)] for j in range(row-1)]
        for i in range(1,row-1):
            for j in range(1,col-1):
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
                testData[i][j] = greyVals

        redMatrix = [[0 for i in range(col-1)] for j in range(row-1)]
        greenMatrix = [[0 for i in range(col-1)] for j in range(row-1)]
        blueMatrix = [[0 for i in range(col-1)] for j in range(row-1)]

        for i in range(1, row-1):
            for j in range(1, col-1):
                #normalize testData
                norm = list(map(divide256,testData[i][j]))
                output = list(map(multiply256, self.feedForwardAllLayers(norm)))
                redMatrix[i][j] = output[0]
                greenMatrix[i][j] = output[1]
                blueMatrix[i][j] = output[2]
        
        colorData = [redMatrix, greenMatrix, blueMatrix]

        color = Image.fromarray(np.array(colorData), mode="RGB")
        color.save('output.png')
        color.show()

        """



to = Image.open('2.jpg')
    grayVersion = photo.convert('L')
    grayMatrix = np.array(grayVersion)

    width = photo.size[0] #define W and H
    height = photo.size[1]

    finalSolution = [[[0,0,0] for x in range(width)] for y in range(height)]


    for i in range(1, height-1): #each pixel's coordinates
        row = ""
        for j in range(1, width-1):

            inputMatrix = np.array([[grayMatrix[i-1][j-1],grayMatrix[i-1][j],grayMatrix[i-1][j+1]],
                                    [grayMatrix[i][j-1],grayMatrix[i][j],grayMatrix[i][j+1]],
                                    [grayMatrix[i+1][j-1],grayMatrix[i+1][j],grayMatrix[i+1][j+1]]])
            nn.feedforward()
            finalSolution[i][j] = nn.output

    print(finalSolution)
    grey = Image.fromarray(finalSolution)
    grey.save('output.png')
    grey.show()



def sigmoid(x):
    return 1/(1+ math.exp(-1 *x))

#returns a matrix of values
def getTrainingDataFromImage(imgName):

    #TESTING ONLY
    #return [([1,2,3],[1,2,3,4,5,6,7,8,9]) for i in range(300)]


    #open iaaa11mage 
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
    trainingData = [[0 for i in range(col-2)] for j in range(row-2)]
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
            trainingData[i-1][j-1] = [colorVal, greyVals]

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


#returns an array
def divideTrainingDataIntoSets(trainingData):
    #divide the training data into sets of 50

    print("Dividing training data into sets")

    flatListTrain = [item for sublist in trainingData for item in sublist]

    sets = []
    trainLen = len(flatListTrain)
    i = 0
    while i < trainLen: 
        j = 0
        newSet = []
        while j < SET_SIZE:
            if i >= trainLen:
                break

            #do the normalization here
            flatListTrain[i][0] = list(map(divide256,flatListTrain[i][0]))
            flatListTrain[i][1] = list(map(divide256,flatListTrain[i][1]))

            newSet.append(flatListTrain[i])
            j+=1
            i+=1
        sets.append(newSet)

    return sets

       
def divide256(x):
    return x/256.0

def multiply256(x):
    return x * 256.0

if __name__ == "__main__":
    net = Net(9,3)
    net.train('mini_pink.PNG')
    #net.train('pink.PNG')
    #input()
    net.predict('mini_pink.PNG')



