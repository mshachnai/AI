#Maze Generator -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
from search import DFS, BFS, AStarE, AStarM
from tkinter import *
from tkinter import ttk
import random
import copy

#maze generator will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, val = 0, heuri = 0, coord = 0): 
        self.val = val     #value to denote open/blocked cell
        self.heuri = heuri #heuristic value 
        self.coord = coord #this is touple to indicate cell coordinates
    
    
#function to generate maze - takes in dimension of maze, probability of blocked cell, and 2d array
def maze_gen(dim, prob):
    maze = []

    random.seed()
    for i in range(0,dim):
        maze.append([])
    
    for i in range(0,dim):
        for j in range(0,dim):
            rand = random.random()  #used for generating a value between 0-1
            #if rand <= prob and (i != 0 or j != 0) and (i != dim-1 or j !=
            if rand <= calculateProb(i, j, prob, dim) and (i != 0 or j != 0) and (i != dim-1 or j !=
                    dim-1) :
                maze[i].append(Cell(val = 1, coord = (i,j))) #blocked cell
                #print(maze[i][j].coord)     #coordinates of blocked cells
            else : 
                maze[i].append(Cell(val = 0, coord = (i,j))) #open cell
                #print(maze[i][j].coord)     #coordinates of open cells cells
    return maze

#function to generate a visual of the maze and its solution if given
######need to work on showing actual path taken
def maze_visual(dim, maze, sol = []):

    #initialize visual window and create maze layout using buttons
    root = Tk()
    root.title('Maze Runner')

    for r in range(dim): #width of maze
        for c in range(dim): #height of maze
            #print(r,c, sol[c-1])

            #top left cell of maze will be named 'S' - start
            if r == 0 and c == 0 :  
                button1 = Button(root, text = "S", relief = SOLID, borderwidth = 1, bg = "light blue", height = 1, width = 1 ).grid(row=r,column=c)

            #bottom right cell of maze will be named 'G' - goal
            elif r == dim-1 and c == dim-1 :  
                button2 = Button(root, text = "G", command = root.destroy, relief = SOLID, borderwidth = 1, bg = "light blue", width = 1 ).grid(row=r,column=c)

            #if cell value == 1, this is a blocked cell
            elif maze[r][c].val == 1:
                button3 = Button(root, relief = SOLID, state = DISABLED, borderwidth = 1, bg = "black", width = 1).grid(row=r,column=c)
                        
            #mark path on the maze visual by checking the cell coordinate is
            #listed in the solution array, if it is - mark the specific cell
            elif (r,c) in sol:
                button4 = Button(root, relief = SOLID, state = DISABLED, borderwidth = 1, bg = "yellow", width = 1).grid(row=r,column=c)
                        
            #for all other cases, create white cells
            else:
                button5 = Button(root, relief = SOLID, state = DISABLED, borderwidth = 1, bg = "white", width = 1).grid(row=r,column=c)

    root.mainloop()
    return

def updatePosition(): 
    return

def calculateProb(r, c, prob, dim):
    return (prob/dim) * (dim - abs(r + c -dim)) 


def main():

    #take in user input of maze dimension and blocked cell probability
    dim = int(input("Enter maze dimension: "))
    prob = float(input("Enter probability: "))

    #1)run maze_gen
    maze = maze_gen(dim, prob)

    #3)run search algorithm and generate maze visual
    #if there is a path - show it with maze_visual
    #otherwise print("No path")
    print("A* Euclidean")
    res = AStarE(maze)
    if res is None : 
        print("No path")
    else : 
        maze_visual(dim, maze, res[0])
        print(res[1])

    print("A* Manhattan")
    res = AStarM(maze)
    if res is None : 
        print("No path")
    else : 
        maze_visual(dim, maze, res[0])
        print(res[1])
    print("BFS")
    res = BFS(maze)
    if res is None : 
        print("No path")
    else : 
        maze_visual(dim, maze, res[0])
        print(res[1])
    print("DFS")
    res = DFS(maze)
    if res is None : 
        print("No path")
    else : 
        maze_visual(dim, maze, res[0])
        print(res[1])
    #4)print algorithm stats with graph

    return


if __name__ == " __main__":
    main()
