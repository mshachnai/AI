from maze_gen import maze_gen, maze_visual, Cell, calculateProb
from search import BFS, DFS, AStarM, AStarE
from random import random, sample
from math import ceil, floor
from copy import deepcopy
import os

def generateHardMaze(START_PROB, EDIT_PROB, DIM, MAX_LOOP_LEN, MAX_LOOP_LEN2, TREE_DEPTH, SEARCH, METRIC, PFUNC, FILE):
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
            sum1 = runTest(mazeTuple, editMaze1, SEARCH, METRIC, EDIT_PROB, PFUNC)

            
            #test2: the one where we only 1->0
            print("test2")
            sum2 = runTest(mazeTuple, editMaze2, SEARCH, METRIC, EDIT_PROB, PFUNC)

            #test3: the one where we only 0->1
            print("test3")
            sum3 = runTest(mazeTuple, editMaze3, SEARCH, METRIC, EDIT_PROB, PFUNC)
        

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
            while numMazes < 2:
                newMaze = editMaze(mazeTuple[0], EDIT_PROB, PFUNC)
                newMazeEval = mazeEval(newMaze, SEARCH, METRIC)
                if newMazeEval and newMazeEval >= standard:
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
                    editMaze = editMaze2

            newMazes.append(mazeTuple) #append the old maze, just to be safe
                    

        #at this point, we should have 5 * beamSize mazes. 
        #sort newMazes by the performance metric in ascending order (worst -> best)
        sortedMazes = sorted(newMazes, key = lambda x : x[1])

        #print stats of hardest maze, currently
        print("curr hardest stats: ",sortedMazes[-1][1])
        #maze_visual(len(sortedMazes[0]), sortedMazes[0])
        FILE.write(str(i) + " " + str(sortedMazes[-1][1]) + "\n")

        for m in sortedMazes[-1][0]:
            for n in m:
                FILE.write("%s" % n.val)
            FILE.write("\n")

        for m in sortedMazes:
            print(m[1], end=" ")

        #cull the poorly performing mazes
        #mazeList = sortedMazes[0:worstLen] + sortedMazes[(-1 * bestLen):]
        worstsList = sortedMazes[0: len(sortedMazes) - bestLen]
        worstSelect = sample(worstsList, worstLen)
        
        mazeList = sortedMazes[(-1 * bestLen):] + worstSelect
        print("loop has run " + str(i) + " times!")

    #mazes are sorted from (worst -> best)
    finalMazes = sorted(mazeList, key = lambda x: x[1])
    print("return 1")
    return finalMazes[-1][0]


def runTest(mazeTuple, editMaze, SEARCH, METRIC, EDIT_PROB, PFUNC):
    Sum= 0
    counter = 0
    while counter < 2:
        newMaze = editMaze(mazeTuple[0], EDIT_PROB, PFUNC)
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


def editMaze1(mazeOrig, EDIT_PROB, PFUNC):
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

def editMaze2(mazeOrig, EDIT_PROB, PFUNC):
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


def editMaze3(mazeOrig, EDIT_PROB, PFUNC):
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

def testLoopz():
    #what is this function doing?
    #for each dim output (loop#, difficultyMeasure) into a file -> graphs/limit<dim>
    #our goal is to eventually plot al of these. 
    
    if not os.path.exists("graphs"):
        os.makedirs("graphs")


    for i in range(8, 11):
        #generate filename
        fname = "graphs/limit" + str(i) + ".3"
        File = open(fname, "w")

        maze = generateHardMaze(0.25, 0.25, i, 800, 1600, 30, "bfs", 0, False, File)
        res = BFS(maze)
        maze_visual(len(maze), maze, res[0])


if __name__ == "__main__":
#    testLoopz()


    fname = "foo"
    File = open(fname, "w")

    SEARCH = "astarm"

    maze = generateHardMaze(0.25, 0.10, 20, 800, 1600, 30, SEARCH, 1, False, File)
    if SEARCH == "bfs":
        res = BFS(maze)
    elif SEARCH == "dfs":
        res = DFS(maze) #make this main into an actual function that takes input for search type & metric
    elif SEARCH == "astarm":
        res = AStarM(maze)
    print("solution length: " + str(res[1][0]))
    print("max fringe: " + str(res[1][1]))
    print("max nodes: " + str(res[1][2]))

    maze_visual(len(maze),maze, res[0]) #change this function to not take in "dim" as parameter

    








