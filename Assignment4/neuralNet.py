from PIL import Image
import numpy as np
import math 



def sigmoid(x):
    return 1/(1+ math.exp(-1 *x))

class Layer:
    def __init__(self, MRow, MCol):

        #matrix is size matRow, matCol
        #initialize all weights to 1 for now
        self.weights = [[1 for i in range(MCol)] for j in range(MRow)]
        self.derivs = [[1 for i in range(MCol)] for j in range(MRow)]
        self.pre_sigmoid_output = []
        self.post_sigmoid_output = []

        self.col = MCol
        self.row = MRow

    def forwardPropagate(Input):
        #calculate effect of weights on input
        weights_on_input= np.matmul(self.weights, Input)
        self.pre_sigmoid_output = weights_on_input
        
        func = sigmoid #choose the function
        sigmoid_applied =  map(func, weights_on_input) #apply the function
        self.post_sigmoid_output = sigmoid_applied
        return sigmoid_applied

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

    def feedForwardAllLayers(vec):
        for layer in self.layers:
            vec = layer.forwardPropagate(vec) 
        return vec

    def backPropagate(res, actual):
        #res is the output vector from feed-forward stage

        firstLayer = None #set this later obviously

        for i in range(self.row):
            for j in range(self.col):
                layers[len(layers) -1].derivs[i][j] = derivFirstlayer(i,j, res, actual)

    def derivFirstLayer(i,j, res, actual): #i sort of refers to output node, j to input.
        lastLayerNum = len(self.layers)
        
        dL_dO = dLoss_dOut(res, actual)
        dO_dI = dSigmaFn(layers[lastLayerNum -1].pre_sigmoid_output[i])
        dI_dW = layers[lastLayerNum-2].post_sigmoid_output[j]
        
        return dL_dO * dO_dI * dI_dW

    def dLoss_dOut(res, actual):
        ret = []

        size = len(res)
        for i in range(len(res)):
            ret.append((float)(1/size) * (res[i] - actual[i]))
        return ret

    def dSigmaFn(I): #"I" is the output before sigmoid is applied to it 
        ret = []
        for i in range(len(I)):
            ret.append(sigmoid(I[i]) * (1 - sigmoid(I[i])))

        return ret

    

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



            
