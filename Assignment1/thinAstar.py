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
import numpy as np

DEBUG = 0

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
    qprob = .0
    # to keep track of all the nodes expanded in thinned maze
    nodes_exp = 0
    nodes_exp1 = 0

    #keep count of blocked cells in path of original maze for computing prob
    count = 0
    stats = []
    stats1 = []
    values = []

    while qprob <= 1 :
        count = 0
        nodes_exp = 0
        nodes_exp1 = 0

        # 1)run maze_gen
        maze = maze_gen(dim, prob)
        res = BFS(maze)
        # maze_visual(dim, maze)

        # make sure there is path from start to goal
        if res is None:
            #print ("no path")
            continue

        # 2)generate a thin\easier version of original maze
        maze1 = thin_maze_gen(qprob, maze)
        # maze_visual(dim, maze1)

        # 3) solve thinned maze and return solution path
        res = AStarE(maze1)
        nodes_exp = nodes_exp + res[1][2]
        stats.append(nodes_exp)# + count*1)
        #print(tm.timeit(lambda: AStarE(maze1), number=50))
        #print("total nodes expanded for thinned maze: ", nodes_exp)#+count*4)
        #print("length of thinned maze path solution: ", res[1][0])

        #collect data of original maze
        res = AStarE(maze)
        nodes_exp1 = nodes_exp1 + res[1][2]
        stats1.append(nodes_exp1)
        #print(tm.timeit(lambda: AStarE(maze), number=50))
        #print("total nodes expanded for original: ", nodes_exp1)
        #print("length of original maze path solution: ", res[1][0])

        #find all blocked cells in path of thinned maze solution
        for i in range(len(maze)):
            for j in range(len(maze)):
                if maze[i][j].coord in res[0] and maze[i][j].val == 1 :
                    count = count+1
        
        values.append(qprob)
        qprob += .05

    #get stats for original maze
    avg_node_exp = sum(stats)/len(stats)
    avg_node_exp1 = sum(stats1)/len(stats1)
    #print("probability of having matching solutions: ", math.pow(qprob, count))
    #print("cost for computing thinned maze: ", nodes_exp)
    #print("total nodes expanded for thinned maze: ", nodes_exp)#+count*4)
    #print("length of thinned maze path solution: ", res[1][0])
    #print("length of thinned maze path solution on original maze: ", res[1][0]+count*4)
    #print("number of iterations: ", iter)
    
    #visual of thinned maze with solution
    #maze_visual(dim, maze1, res[0])
    #visual of original maze with thinned maze solution
    #maze_visual(dim, maze, res[0])

   # 5) compare nodes expanded with original maze solution
    #res = AStarE(maze)
    #maze_visual(dim, maze, res[0])
    #nodes_exp1 = nodes_exp1 + res[1][2]
    #print("total nodes expanded for original: ", nodes_exp1)
    #print("length of original maze path solution: ", res[1][0])
    print(stats, stats1)    
   
    ################# for potential use
    # 4)plot algorithm stats with graphs (add data here - to be completed)
    # density vs. solvability
    array = [1, 2, 3, 4]
    plt.plot(array, [1, 2, 3, 4], 'ro')
    plt.ylabel('density')
    plt.xlabel('solvability')
    if DEBUG == 2 or DEBUG == 3:
        plt.show()

    avg = [avg_node_exp, avg_node_exp1]
    #sampled time at 200ms intervals
    #t = np.arange(3)
    #red dashes, blue squares and green triangles
    #plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
    #plt.show()

    names = ['Thin A*', 'Reg A*']
    #values = [0., .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.]
	
    plt.figure(1, figsize=(9, 3))
	
    plt.subplot(131)
    plt.ylabel('Difficulty of solving maze (tot. nodes expanded)')
    plt.xlabel('Prob. of simplifying maze')
    plt.scatter(values, stats)
    plt.scatter(values, stats1)
    plt.legend(('Thin A*', 'A*'))
    plt.subplot(132)
    plt.ylabel('Avg. tot. node expansion')
    plt.bar(names, [avg_node_exp, avg_node_exp1], width = 0.6, edgecolor =
            'red', color = ['C0','orange'])
    plt.subplot(133)
    plt.ylabel('Difficulty of solving maze (tot. nodes expanded)')
    plt.xlabel('Prob. of simplifying maze')
    plt.plot(values, stats)
    plt.plot(values, stats1)
    plt.suptitle('Thinning A* Heuristic Stats')
    plt.show()
    
    return

if __name__ == "__main__":
    main()
