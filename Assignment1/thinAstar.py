# Solving mazes with thinning A* heuristic

from maze_gen import *
from search import DFS, BFS, AStarE, AStarM
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
import math
import copy

DEBUG = 1

# function to generate a thinned/easier version of the original maze
def thin_maze_gen(prob, maze1):
    random.seed()
    # make copy of original maze to retain its values
    maze = copy.deepcopy(maze1)

    for i in range(0, len(maze)):
        for j in range(0, len(maze)):
            rand = random.random()  # used for generating a value between 0-1
            # remove blocked cell with given probability
            if rand <= prob and maze[i][j].val == 1:
                maze[i][j].val = 0

    return maze

def BFS_A2B(maze1, start, end):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Edit: I'll have to change this to incorporate class Cell later
    Returns: a list of tuples if a valid path exists. Returns None otherwise """

    size = len(maze1)

    #make a deep copy of maze to use it without changing original values
    maze = copy.deepcopy(maze1)
    if maze[0][0].val == 1:
        return None

    root = Node(start, [], None)
    queue = []
    queue.append(root)

    ret = []

    #initialize counters for max fringe size, max nodes expanded
    maxFringe = 0
    maxNodes = 0

    while len(queue) != 0:

        #max fringe counter
        maxFringe = max(maxFringe, len(queue))

        node = queue.pop(0)

        #check if node is the goal state 
        if node.data == end:
            while(node):
                ret.append(node.data)
                node = node.parent
            return (ret, [len(ret), maxFringe, maxNodes])

        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        
        #check right
        if col < size-1:
            if(maze[row][col+1].val == 0):
                #create a new node
                rightNode = Node((row,col+1), [], node)
                #enqueue
                queue.append(rightNode)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col+1].val = 2
                #increment nodes expanded
                maxNodes+=1

        #check down
        if row < size -1:
            if(maze[row+1][col].val == 0):
                downNode = Node((row+1, col), [], node)
                queue.append(downNode)
                node.children.append(downNode)
                maze[row+1][col].val = 2
                maxNodes+=1

        #check up
        if row > 0:
            if(maze[row-1][col].val == 0):
                upNode = Node((row-1, col), [], node)
                queue.append(upNode)
                node.children.append(upNode)
                maze[row-1][col].val = 2
                maxNodes+=1

        #check left
        if col > 0: 
            if(maze[row][col-1].val == 0):
                leftNode = Node((row, col-1), [], node)
                queue.append(leftNode)
                node.children.append(leftNode)
                maze[row][col-1].val = 2
                maxNodes+=1


def valid_path(maze1, sol=[]):
    if sol == None:
        return False
    for (r, c) in sol:
        if (maze1[r][c].val == 1):
            return False
    return True


def main():
    # take in user input of maze dimension and blocked cell probability
    dim = int(input("Enter maze dimension: "))
    prob = float(input("Enter probability: "))
    # probability of unblocking cells
    qprob = .02
    # to keep track of all the nodes expanded in thinned maze
    nodes_exp = 0
    nodes_exp1 = 0

    #keep count of blocked cells in path of original maze for computing prob
    count = 0

    # 1)run maze_gen
    maze = maze_gen(dim, prob)
    res = AStarE(maze)
    # maze_visual(dim, maze)

    # make sure there is path from start to goal
    if res is not None:
        # 2)generate a thin\easier version of original maze
        maze1 = thin_maze_gen(qprob, maze)
        # maze_visual(dim, maze1)

        # 3) solve thinned maze and return solution path
        res = AStarE(maze1)
        print(tm.timeit(lambda: AStarE(maze1), number=RUNS))
        nodes_exp = nodes_exp + res[1][2]

        iter = 1

        # 4) check if solution works on original, if not
        # repeat process from (2) 
        #while not valid_path(maze, res[0]):
        #    maze1 = thin_maze_gen(qprob, maze)
        #    res = BFS(maze1)
        #    nodes_exp = nodes_exp + res[1][2]
        #    iter = iter + 1
       
        for i in range(len(maze)):
            for j in range(len(maze)):
                if maze[i][j].coord in res[0] and maze[i][j].val == 1 :
                    count = count+1

        print ("probability of having matching solutions: ", math.pow(qprob,
            count))
        print("total nodes expanded for thinned maze: ", nodes_exp)
        print("number of iterations: ", iter)

    if res is not None:
        maze_visual(dim, maze1, res[0])
        maze_visual(dim, maze, res[0])

   # 5) compare nodes expanded with original maze solution
        res = AStarE(maze)
        print(tm.timeit(lambda: AStarE(maze), number=RUNS))
        maze_visual(dim, maze, res[0])
        nodes_exp1 = nodes_exp1 + res[1][2]
        print("total nodes expanded for original: ", nodes_exp1)
    
   
   #####Alternative option - didn't get to this yet
    
    

    ################# for potential use
    # 4)plot algorithm stats with graphs (add data here - to be completed)
    # density vs. solvability
    array = [1, 2, 3, 4]
    plt.plot(array, [1, 2, 3, 4], 'ro')
    plt.ylabel('density')
    plt.xlabel('solvability')
    if DEBUG == 2 or DEBUG == 3:
        plt.show()

    # density vs. shortest expected path
    plt.plot([1, 2, 3, 4], [1, 2, 7, 8], 'ro')
    plt.ylabel('density')
    plt.xlabel('shortest expected path')
    if DEBUG == 2 or DEBUG == 3:
        plt.show()

    return


if __name__ == "__main__":
    main()
