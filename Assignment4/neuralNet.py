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


#builds a neural net 
def buildNet():
    
    #we will put all layers into here
    layers = []

    #input is the 8 pixels surrounding the pixel thatwe're trying to predict
    #so the input layer will have 8 nodes
    #each subsequent layer will have 20 nodes (this is an arbitrary number lmao)
    #we represent this by coding a 20 x 8 matrix into our first "Layer" object.
    firstLayer = Layer(20, 8)
    layers.append(firstLayer)

    #make 5 hidden layers. 5 is also an arbitrary value
    #each layer is a has 20 nodes.
    for i in range(5):
        layer = Layer(20, 20)
        layers.append(layer)

    #we need 3 output nodes for R,G,B 
    lastLayer = Layer(3,20)
    layers.append(lastLayer)

    return layers


if __name__ == "__main__":
    buildNet()

            
