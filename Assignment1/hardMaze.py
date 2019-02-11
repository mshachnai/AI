from maze_gen import maze_gen, maze_visual, Cell, calculateProb
from search import BFS, DFS, AStarM, AStarE
from random import random
from math import ceil, floor
from copy import deepcopy

START_PROB = 0.3
EDIT_PROB = 0.1
DIM = 15
MAX_LOOP_LEN = 800  #switch editMaze to "both"
MAX_LOOP_LEN2 = 1600 #lower maze quality standards for acceptance
TREE_DEPTH = 20
SEARCH = "bfs"
METRIC = 0
PFUNC=True

def generateHardMaze():
    #create a random maze 
    #do random starting probabilities until we find a good one
    
                    #int(input("Enter maze dimensions: "))
                    #float(input("Enter starting probability: "))
    beamSize = 8    #int(input("Enter beam size: "))

    worstLen = ceil(0.25 * beamSize)
    bestLen = floor(0.75 * beamSize) 

    #this is a list of mazes. we add <beamSize> mazes to start off the algorithm
    mazeList = []

    while len(mazeList) < beamSize:
        maze = maze_gen(DIM, START_PROB)
        maze_eval = mazeEval(maze, SEARCH, METRIC) 
        if maze_eval:
            mazeList.append((maze, maze_eval))
    print("initial mazes appended")


    #each iteration of this loop is like another layer of the tree
    for i in range(TREE_DEPTH):
        print("aaaa")
        #generate 4 * beamSize mazes
        #push the worst 1/4 * beamSize mazes, and push the best 3/4 * beamsize (for "genetic diversity")
        
        newMazes = []
        
        #this loop generates a lot of possible mazes, which we will cull when the loop breaks
    
        for mazeTuple in mazeList:

            #test to see which editMaze algorithm would work the best
            print("test1")
            sum1 = runTest(mazeTuple, editMaze1)

            #test2: the one where we only 1->0
            print("test2")
            sum2 = runTest(mazeTuple, editMaze2)

            #test3: the one where we only 0->1
            print("test3")
            sum3 = runTest(mazeTuple, editMaze3)

            maxSum = max(sum1, sum2, sum3)

            #find the maximum sum out of them 
            #print("generating actual mazes")
            editMaze = editMaze1
            if maxSum == sum1:
                print("both")
                editMaze = editMaze1
            elif maxSum == sum2:
                print("remove")
                editMaze = editMaze2
            elif maxSum == sum3:
                print("add")
                editMaze = editMaze3

            #generate mazes to put into the list of new mazes 
            
            loopCounter = 0
            numMazes = 0 #want to generate 4 "child" mazes for every maze
            standard = mazeTuple[1] #mazes must exceed this number before being put into queue
            while numMazes < 4:
                newMaze = editMaze(mazeTuple[0])
                newMazeEval = mazeEval(newMaze, SEARCH, METRIC)
                if newMazeEval and newMazeEval > standard:
                    newMazes.append((newMaze, newMazeEval))
                    numMazes+=1
                loopCounter+=1

                if loopCounter == MAX_LOOP_LEN:
                    print("exceeded MAX_LOOP_LEN. using remove/add func")
                    #this is necessary b/c "add" editMaze will eventually stall program,
                    #unless we prevent it
                    editMaze = editMaze1
                if loopCounter > MAX_LOOP_LEN2:
                    standard -=1 #gradually lower the standard for accepting maze

            newMazes.append(mazeTuple) #append the old maze, just to be safe
                    

        #at this point, we should have 5 * beamSize mazes. 
        #sort newMazes by the performance metric in ascending order (worst -> best)
        sortedMazes = sorted(newMazes, key = lambda x : x[1])

        #print stats of hardest maze, currently
        print("curr hardest stats: ",sortedMazes[-1][1])
        for m in sortedMazes:
            print(m[1], end=" ")

        #cull the poorly performing mazes
        mazeList = sortedMazes[0:worstLen] + sortedMazes[(-1 * bestLen):]
        print("loop has run " + str(i) + " times!")

    #mazes are sorted from (worst -> best)
    finalMazes = sorted(mazeList, key = lambda x: x[1])
    print("return 1")
    return finalMazes[-1][0]


def runTest(mazeTuple, editMaze):
    Sum= 0
    counter = 0
    while counter < 4:
        newMaze = editMaze(mazeTuple[0])
        val = mazeEval(newMaze, SEARCH, METRIC)
        if val:
            Sum+=val
            counter+=1
            #print("invalid maze")
            #maze_visual(len(newMaze), newMaze)
    return Sum


   
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
        #print("no path")

        #maze_visual(len(maze), maze ) #delete later
        return None


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
    prob = EDIT_PROB

    #make the probability a function of the row and column.
    #this is to prevent the start/goal corners from getting blocked off
    #f(r,c) = (prob/dim) * (dim - abs(r + c -dim))

    for r in range(dim):
        for c in range(dim):
            rand = random()
            curr = maze[r][c] #current cell
            if curr.val == 1:
                if rand < prob:
                    maze[r][c] = Cell(0, curr.heuri, curr.coord)
            elif curr.val == 0:
                if PFUNC:
                    if rand < calculateProb(r,c,prob, dim):
                        maze[r][c] = Cell(1, curr.heuri, curr.coord)
                else:
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
    prob = EDIT_PROB

    for r in range(dim):
        for c in range(dim):
            rand = random()
            curr = maze[r][c]
            if curr.val == 1:
                if rand < prob:
                    maze[r][c] = Cell(0, curr.heuri, curr.coord)

    return maze


def editMaze3(mazeOrig):
    """
    returns a slightly modified maze (only flips 0's to 1)
    """

    #create a deep copy of maze

    #make a deep copy of maze to use it without changing original values
    maze = deepcopy(mazeOrig)
    
    dim = len(maze)

    prob = EDIT_PROB

    for r in range(dim):
        for c in range(dim):
            rand = random()
            curr = maze[r][c]
            if curr.val == 0:
                if PFUNC:
                    if rand < calculateProb(r,c,prob, dim):
                        maze[r][c] = Cell(1, curr.heuri, curr.coord)
                else:
                    if rand < prob:
                        maze[r][c] = Cell(1, curr.heuri, curr.coord)

    return maze



if __name__ == "__main__":
    maze = generateHardMaze()
    if SEARCH == "bfs":
        res = BFS(maze)
    elif SEARCH == "dfs":
        res = DFS(maze) #make this main into an actual function that takes input for search type & metric
    
    print("solution length: " + str(res[1][0]))
    print("max fringe: " + str(res[1][1]))
    print("max nodes: " + str(res[1][2]))

    maze_visual(len(maze),maze, res[0]) #change this function to not take in "dim" as parameter









