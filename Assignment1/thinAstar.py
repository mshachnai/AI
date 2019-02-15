# Solving mazes with thinning A* heuristic

from maze_gen import *
from search import DFS, BFS, AStarE, AStarM
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
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
    qprob = .5
    # to keep track of all the nodes expanded in thinned maze
    nodes_exp = 0

    # 1)run maze_gen
    maze = maze_gen(dim, prob)
    res = BFS(maze)
    # maze_visual(dim, maze)

    # make sure there is path from start to goal
    if res is not None:
        # 2)thin original version of maze
        maze1 = thin_maze_gen(qprob, maze)
        # maze_visual(dim, maze1)

        # 3) solve thinned maze and return solution path
        res = AStarE(maze1)
        nodes_exp = nodes_exp + res[1][2]

        iter = 1

        # 4) check if solution works on original, if not
        # repeat process from (2) if path invalid
        while not valid_path(maze, res[0]):
            maze1 = thin_maze_gen(qprob, maze)
            res = AStarE(maze1)
            nodes_exp = nodes_exp + res[1][2]
            iter = iter + 1

        print("total nodes expanded: ", nodes_exp)
        print("number of iterations: ", iter)

    if res is not None:
        maze_visual(dim, maze, res[0])

    # 5) compare nodes expanded with original maze solution
    # add comparison here#

    print("A* Euclidean")
    res = AStarE(maze)
    print(tm.timeit(lambda: AStarE(maze), number=RUNS))
    if DEBUG == 1 or DEBUG == 3:
        if res is None:
            print("No path")
        else:
            maze_visual(dim, maze, res[0])

        # print(res[1])

    print("A* Manhattan")
    res = AStarM(maze)
    print(tm.timeit(lambda: AStarM(maze), number=RUNS))
    if DEBUG == 1 or DEBUG == 3:
        if res is None:
            print("No path")
        else:
            maze_visual(dim, maze, res[0])
            # print(res[1])

    print("BFS")
    res = BFS(maze)
    print(tm.timeit(lambda: BFS(maze), number=RUNS))
    if DEBUG == 1 or DEBUG == 3:
        if res is None:
            print("No path")
        else:
            maze_visual(dim, maze, res[0])
            # print(res[1])

    print("DFS")
    res = DFS(maze)
    print(tm.timeit(lambda: DFS(maze), number=RUNS))
    if DEBUG == 1 or DEBUG == 3:
        if res is None:
            print("No path")
        else:
            maze_visual(dim, maze, res[0])
            # print(res[1])

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
