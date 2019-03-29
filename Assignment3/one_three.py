from random import random, randint
DIM = 2

class Cell:
    def __init__(self, terrain, x, y):
        self.P = -1 #probability of finding in square
        self.negP = -1 #probability of false negative
        self.terrain = terrain #[0:"flat", 1:"hilly", 2:"forested", 3:"mazeOfCaves"]
        if terrain == 0:
            self.negP = 0.1
        elif terrain == 1:
            self.negP = 0.3
        elif terrain == 2:
            self.negP = 0.7
        elif terrain == 3:
            self.negP = 0.9

        self.isTarget = 0
        self.x = x
        self.y = y

def main():
    #generate the DIMxDIM grid 
    grid = [[0 for i in range(DIM)] for i in range(DIM)]

    #calculate total # of cells
    numCells = DIM * DIM

    for i in range(DIM):
        for j in range(DIM):
            x = random()
            terr = -1
            if x < 0.25:
                terr = 0
            elif x < 0.5:
                terr = 1
            elif x < 0.75:
                terr = 2
            else:
                terr = 3
             
            #create and push into data structures
            cell = Cell(terr, i, j)
            grid[i][j] = cell

            #set initial probabilities
            cell.P = (float)(1/numCells) * (1-cell.negP)
            
    #choose a square to put target
    xCoord = randint(0, DIM-1)
    yCoord = randint(0, DIM-1)
    print("target is in: " + str(xCoord) + "," + str(yCoord))
    grid[xCoord][yCoord].isTarget = 1

    #while target is not found, query and update probabilities
    ctr = 0
    while True:
        #search each grid for max probability
        maxProb = -1
        maxCell = None
        for i in range(DIM):
            for j in range(DIM):
                if grid[i][j].P > maxProb:
                    maxProb = grid[i][j].P
                    maxCell = grid[i][j]
                    print("maxProb:" + str(maxProb))
            
        #query the grid with max probability
        print("queried: " + str(maxCell.x) + "," + str(maxCell.y))
        if maxCell.isTarget == 1:
            rand = random()
            if rand < maxCell.negP: #if less than the false negative rate, then continue
                print("false negative")
                updateProb(grid, maxCell.x, maxCell.y)
                pass
            else:
                break
        else:
            updateProb(grid, maxCell.x, maxCell.y)
            ctr += 1

    print("target found!")
    print("took " + str(ctr) + " queries!")
    
def updateProb(grid, x, y): #x & y are coordinates of the queried cell
    Queried = grid[x][y]

    #After using Bayes rule, the algorithm is, for each round of updateProb:
    #divide all probabilities in grid (including Queried.P ) by exactly 1-(Queried.P)
    #Queried.P := (Queried.P) *  (Queried.negP)

    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].P /= 1-(Queried.P)

    Queried.P *= Queried.negP
    printGrid(grid)


def printGrid(grid):
    print("+++++++++++")
    for i in range(len(grid)):
        for j in range(len(grid)):
            cell = grid[i][j]
            print("pos " + str(i) + "," + str(j))
            print("falseNegativeRate: " + str(cell.negP))
            print("newProb: " + str(cell.P))

    
    
    print("+++++++++++")
if __name__ == "__main__":
    main()

