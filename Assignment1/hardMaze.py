from maze_gen import maze_gen, maze_visual, Cell
from search import BFS, DFS, AStarM, AStarE
from random import random
from math import ceil, floor
from copy import deepcopy

MAX_LOOP_LEN = 30
OUTER_LOOP_LEN = 20
def generateHardMaze(size):
    #create a random maze 
    #do random starting probabilities until we find a good one
    
    SEARCH = "bfs"
    METRIC = 1

    dim = 20        #int(input("Enter maze dimensions: "))
    prob = 0.4      #float(input("Enter starting probability: "))
    beamSize = 8    #int(input("Enter beam size: "))

    worstLen = ceil(0.25 * beamSize)
    bestLen = floor(0.75 * beamSize) 

    #this is a list of mazes. we add <beamSize> mazes to start off the algorithm
    mazeList = []
    while len(mazeList) < beamSize:
        maze = maze_gen(dim, prob)
        maze_eval = mazeEval(maze, SEARCH, METRIC) 
        if maze_eval:
            mazeList.append((maze, maze_eval))
    print("initial mazes appended")

    for i in range(OUTER_LOOP_LEN):
        #generate 4 * beamSize mazes
        #push the worst 1/4 * beamSize mazes, and push the best 3/4 * beamsize (for "genetic diversity")
        
        newMazes = []
        #loop while we haven't exceeded the beam length
        #this would occur if the mazes that we generate don't have a solution
        #it might be useful if we keep track of the number of times this loop executes
        #   -the default editMaze function adds more obstacles than it deletes. 
        #   -make another editMaze that deletes more obstacles than it adds 
        
        
        loopCounter = 0
        editMaze = editMaze1 #set the editMaze function
        while len(newMazes) < beamSize:
            
            
            #keep track of the number of times this loop executes
            #if it runs for too long, change the editMaze function
            if loopCounter == 10:
                print("switching editMaze func")
                editMaze = editMaze2

            if loopCounter == MAX_LOOP_LEN:
                break

            for mazeTuple in mazeList:
                for x in range(4):
                    newMaze = editMaze(mazeTuple[0])
                    oldMazeEval = mazeTuple[1]
                    newMazeEval = mazeEval(newMaze, SEARCH, METRIC)
                    if newMazeEval and newMazeEval > oldMazeEval:
                        newMazes.append((newMaze, newMazeEval))

            loopCounter+=1
            print(loopCounter)

        if loopCounter == MAX_LOOP_LEN:
            print("exceeded MAX_LOOP_LEN. killing program")
            if len(newMazes) == 0:
                finalMazes = sorted(mazeList, key= lambda x : x[1])
            else:
                finalMazes = sorted(newMazes, key= lambda x : x[1])

            return finalMazes[-1][0]

        #sort newMazes by the performance metric in ascending order (worst -> best)
        sortedMazes = sorted(newMazes, key = lambda x : x[1])

        #cull the poorly performing mazes
        mazeList = sortedMazes[0:worstLen] + sortedMazes[(-1 * bestLen):]
        print("loop has run " + str(i) + " times!")

    #mazes are sorted from (worst -> best)
    finalMazes = sorted(mazeList, key = lambda x: x[1])
    return finalMazes[-1][0]



   
def mazeEval(maze, search, metric):
    """ mazeEval evaluates a maze based on characteristics such as 
            the length of the shortest path 
            number of nodes expended while solving 
            maximum size of fringe 
        note that all of these are measured in relation to their dimension

        search is a string that is either ["bfs", "dfs", "astare", "astarm"]
        metric is an int that corresponds to a metric. The mapping can be described as follows:
                {0: "maximal shortest path", 1: "maximal fringe size", 2: maximal nodes expanded}
    """

    if search not in ["bfs", "dfs", "astare", "astarm"]:
        print("invalid search type")
        return None

    if metric not in [0,1,2]:
        print("invalid metric")
        return None

    if search == "bfs":
        #print("did a bfs")
        res = BFS(maze)
    elif search == "dfs": 
        res = DFS(maze)
    elif search == "astare":
        res = AStarE(maze)
    elif search == "astarm":
        res = AStarM(maze)

    if res:
        return res[1][metric]
    else:
        return


def editMaze1(mazeOrig):
    """
    returns a slightly modified maze ("randomly" flips 0's and 1's)
    the probability of 0 -> 1 is 2x the probability of 1 -> 0
    """

    #create a deep copy of maze

    #make a deep copy of maze to use it without changing original values
    maze = deepcopy(mazeOrig)
    
    dim = len(maze)

    # 0 < prob < 0.49
    #there will probably be a value for "prob" that works the best.
    #if prob is too small, then the new mazes will be similar to parent
    #   -will have to run more iterations to get desired result
    #if prob is too large, the new mazes will not be similar to parent at all
    #   -problem becomes very similar to random walk
    #testing idea: test in increments of 0.05 until we're satisfied
    prob = 0.10

    for r in range(dim):
        for c in range(dim):
            rand = random()
            curr = maze[r][c] #current cell
            if curr.val == 1:
                if rand < prob:
                    maze[r][c] = Cell(0, curr.heuri, curr.coord)
            elif curr.val == 0:
                if rand < prob:
                    maze[r][c] = Cell(1, curr.heuri, curr.coord)

    return maze


def editMaze2(mazeOrig):
    """
    returns a slightly modified maze (only flips 1's to 0)
    """

    #create a deep copy of maze

    #make a deep copy of maze to use it without changing original values
    maze = deepcopy(mazeOrig)
    
    dim = len(maze)

    # 0 < prob < 1.0
    #there will probably be a value for "prob" that works the best.
    #if prob is too large, it's counterproductive to finding difficult mazes
    #if prob is too small, the program might run for a long time
    #testing idea: start at 0.10 and work our way smaller until the program runs too slowly
    prob = 0.10

    for r in range(dim):
        for c in range(dim):
            rand = random()
            curr = maze[r][c]
            if curr.val == 1:
                if rand < prob:
                    maze[r][c] = Cell(0, curr.heuri, curr.coord)

    return maze


if __name__ == "__main__":
    maze = generateHardMaze(20)
    res = BFS(maze) #make this main into an actual function that takes input for search type & metric
    
    print("solution length: " + str(res[1][0]))
    print("max fringe: " + str(res[1][1]))
    print("max nodes: " + str(res[1][2]))

    maze_visual(20,maze, res[0]) #change this function to not take in "dim" as parameter









