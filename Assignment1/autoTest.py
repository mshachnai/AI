from hardMaze import generateHardMaze
from maze_gen import maze_gen, maze_visual
import matplotlib.pyplot as plt
from search import BFS, DFS, AStarE, AStarM

P = 0.3
DIM = 30

def two_point_four():
    """
    #density vs. shortest expected path
    plt.plot([1,2,3,4], [1, 2, 7, 8], 'ro')
    plt.ylabel('density')
    plt.xlabel('shortest expected path')
    if DEBUG == 2 or DEBUG == 3:
        plt.show()
    """
    xy = []
    #run dfs a bunch for each p up to p0
    for i in range(0,int(P * 100) + 1, int(0.02 * 100)):
        prob = i * 0.01 
        print(prob)
        Sum = 0
        ctr = 0
        while ctr < 30:
            maze = maze_gen(DIM, prob)
            #maze_visual(30, maze)
            ret = AStarM(maze)
            if ret:
                shortestPath = ret[1][0]
                Sum += shortestPath
                ctr +=1
        print(Sum/float(ctr))
        xy.append((prob, Sum/float(ctr) ))

    xVal = []
    yVal = []
    for pair in xy:
        xVal.append(pair[0])
        yVal.append(pair[1])



    plt.plot(xVal, yVal, 'ro')
    plt.xlabel('density')
    plt.ylabel('shortest path')
    plt.title('A* Manhattan shortest path over p from [0,p0]')
    plt.show()

def two_point_six():
    #for DIM = 30, generate a maze for each p from p up to p0


    xValScatter = []
    yValScatter = []

    xValNeg = []
    yValNeg = []

    xyBFS = []
    xyDFS = []
    #run dfs a bunch for each p up to p0
    for i in range(0,int(P * 100) + 1, int(0.02 * 100)):
        prob = i * 0.01 
        print(prob)
        SumBFS = 0
        SumDFS = 0
        ctr = 0
        while ctr < 30:
            maze = maze_gen(DIM, prob)
            #maze_visual(30, maze)
            retBFS = BFS(maze)
            retDFS = DFS(maze)

            if retBFS:

                #calculate BFS stuff
                shortestPathBFS = retBFS[1][0]
                SumBFS += shortestPathBFS


                #calculate DFS stuff
                shortestPathDFS = retDFS[1][0]
                SumDFS += shortestPathDFS
                
                diff = shortestPathDFS -shortestPathBFS 
                if diff < 0:
                    xValNeg.append(prob)
                    yValNeg.append(diff)
                else:
                    xValScatter.append(prob)
                    yValScatter.append(shortestPathDFS -shortestPathBFS)

                ctr +=1

        xyBFS.append((prob, SumBFS/float(ctr) ))
        xyDFS.append((prob, SumDFS/float(ctr) ))

    xValBFS = []
    yValBFS = []
    for pair in xyBFS:
        xValBFS.append(pair[0])
        yValBFS.append(pair[1])

    xValDFS = []
    yValDFS = []
    for pair in xyDFS:
        xValDFS.append(pair[0])
        yValDFS.append(pair[1])

    """
    plt.plot(xValBFS, yValBFS, 'ro')
    plt.plot(xValDFS, yValDFS, 'bo')
    plt.xlabel('density')
    plt.ylabel('solution length')
    plt.title('A comparison of solution lengths for BFS (red), and DFS(blue)')
    plt.show()
    """

    plt.scatter(xValScatter, yValScatter, s=0.1,c='r')
    plt.scatter(xValNeg, yValNeg, s=1, c='b')
    plt.xlabel('density')
    plt.ylabel('solution length differernce')
    plt.title('difference in solution lengths (DFS-BFS)')
    plt.show()



if __name__ == "__main__":
    two_point_six()

