#Probabilistic search and destroy -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
import copy
#import prob_solver_minesweeper as sv

######for later use
#DEBUG is used for turning visuals on/off: (not complete yet)
#0: will not show any visuals
#1: will show grid visuals
#2: will show plotting graphs
#3: will show all visuals
#DEBUG = 3 
#RUNS = 1 #number of times each algorithm is run for timing

#S&D will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, ltype = "flat", coord = (0,0), target = 0): 
        self.ltype = ltype     #value to denote land type 
        self.target = target     #value to denote if target(1)/clear(0)
        self.coord = coord #this is touple to indicate cell coordinates
        self.visited = 0 #value to indicate if cell has been visited
        self.prob = -1 #value to indicate probability of being a bomb

#function to generate S&D map - takes in dimension of map
def map_gen(dim):
    grid = []
    random.seed()

    #create 2d grid and assign land types to each (.2 flat, .3 hill, .3 forest, .2 #cave)
    for i in range(0,dim):
        grid.append([])
        for j in range(0,dim):
            grid[i].append(Cell(coord = (i,j)))
            rand = random.randint(1, 10)
            if rand <= 2:
                grid[i][j].ltype = "flat"
            elif rand > 2 and rand <= 5:
                grid[i][j].ltype = "hill"
            elif rand > 5 and rand <= 8:
                grid[i][j].ltype = "forest"
            elif rand > 8 and rand <= 10:
                grid[i][j].ltype = "cave"

    #assign target randomly to one of the cells
    x = random.randint(0,dim-1)  #random X coordinate
    y = random.randint(0,dim-1)  #random Y coordinate
    grid[x][y].target = 1 
        
    return grid



#function to generate a visual of the grid and its solver if given
def grid_visual(dim, grid, score):

    #initialize visual window and create grid layout using buttons
    root = tk.Tk()
    root.title('Search & Destroy')
    
    #clickable function for minesweeper
    def mouse_press(row, col):
        rand = random.random()
        
        if grid[row][col].ltype == "flat":
            #if cell is target (and with correct probability is found) - show it
            if grid[row][col].target == 1 and rand <= 0.9 :  
                button[row][col].config(disabledforeground = "red", font = '40', command = 0, relief = SUNKEN, text = "X", state = DISABLED)
                #keep track of number of cells explored
                score[0] += 1
            #else search failed - show it
            else:
                button[row][col].config(text = "F")
                button[row][col].after(300, lambda: button[row][col].config(text = ""))
                #keep track of number of cells explored
                score[0] += 1
        elif grid[row][col].ltype == "hill":
            #if cell is target (and with correct probability is found) - show it
            if grid[row][col].target == 1 and rand <= 0.7 : 
                button[row][col].config(disabledforeground = "red", font = '40', command = 0, relief = SUNKEN, text = "X", state = DISABLED)
                #keep track of number of cells explored
                score[0] += 1
            #else search failed - show it
            else:
                button[row][col].config(text = "F")
                button[row][col].after(300, lambda: button[row][col].config(text = ""))
                #keep track of number of cells explored
                score[0] += 1
        elif grid[row][col].ltype == "forest":
            #if cell is target (and with correct probability is found) - show it
            if grid[row][col].target == 1 and rand <= 0.3 : 
                button[row][col].config(disabledforeground = "red", font = '40', command = 0, relief = SUNKEN, text = "X", state = DISABLED)
                #keep track of number of cells explored
                score[0] += 1
            #else search failed - show it
            else:
                button[row][col].config(text = "F")
                button[row][col].after(300, lambda: button[row][col].config(text = ""))
                #keep track of number of cells explored
                score[0] += 1
        elif grid[row][col].ltype == "cave":
            #if cell is target (and with correct probability is found) - show it
            if grid[row][col].target == 1 and rand <= 0.1 : 
                button[row][col].config(disabledforeground ="red", font = '40', command = 0, relief = SUNKEN, text = "X", state = DISABLED)
                #keep track of number of cells explored
                score[0] += 1
            #else search failed - show it
            else:
                button[row][col].config(text = "F")
                button[row][col].after(300, lambda: button[row][col].config(text = ""))
                #keep track of number of cells explored
                score[0] += 1

                
    #create a grid of buttons with functionality
    button = []
    for r in range(dim): #width of grid
        button.append([])
        for c in range(dim): #height of grid
            if grid[r][c].ltype == "flat":
                color = "snow"
            elif grid[r][c].ltype == "hill":
                color = "light grey"
            elif grid[r][c].ltype == "forest":
                color = "lime green"
            elif grid[r][c].ltype == "cave":
                color = "grey22"
            #create blank clickable cells (functionality is in each cell)
            button[r].append(tk.Button(root, relief = SOLID, text = "", command =
                lambda row = r, col = c: mouse_press(row, col), borderwidth = 1, bg =
                color, width = 2, height = 2))
            button[r][-1].grid(row=r,column=c)

    #solver for S&D
    #sv.solver(grid, dim, button, root)
    
    root.mainloop()
    return


def main():

    #take in user input of grid dimension and blocked cell probability
    dim = int(input("Enter grid dimension: "))
    grid = []
    if dim < 0:
        print("dimension less than 0...terminating")
        return
    score = [0]

    ########this is for testing purposes only ########
    #dim = 4
    #num_mines = 3
    #for i in range(0,dim):
    #    grid.append([])
    #    for j in range(0,dim):
    #        grid[i].append(Cell(coord = (i,j)))
    #grid[0][0].val = 0    
    #grid[0][1].val = 0    
    #grid[0][2].val = 0    
    #grid[1][0].val = 1    
    #grid[1][1].val = 2    
    #grid[1][2].val = 2    
    #grid[2][0].val = 1    
    #grid[2][1].bomb = 1    
    #grid[2][2].bomb = 1    

    #1)run mine_gen -- #2) run solver in visual to solve the maze (collect, update KB, take action) 
    grid = map_gen(dim)
    grid_visual(dim, grid, score)
    print("\nNumber of cells searched ", score[0])
    
    #2)run agent to solve the maze (collect, update KB, take action) 


    #3)plot agent stats with graphs
    #density vs. solvability
    #array = [1,2,3,4]
    #plt.plot(array, [1, 2, 3, 4], 'ro')
    #plt.ylabel('density')
    #plt.xlabel('solvability')
    #if DEBUG == 2 or DEBUG == 3 :
    #    plt.show()
    #
    ##density vs. shortest expected path
    #plt.plot([1,2,3,4], [1, 2, 7, 8], 'ro')
    #plt.ylabel('density')
    #plt.xlabel('shortest expected path')
    #if DEBUG == 2 or DEBUG == 3:
    #    plt.show()"""

    return

if __name__ == "__main__":
    main()
