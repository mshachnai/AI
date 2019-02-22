#Minesweeper -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
import copy

#DEBUG is used for turning visuals on/off: (not complete yet)
#0: will not show any visuals
#1: will show grid visuals
#2: will show plotting graphs
#3: will show all visuals
DEBUG = 3 
RUNS = 1 #number of times each algorithm is run for timing

#minesweeper will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, val = 0, coord = (0,0), bomb = 0): 
        self.val = val     #value to denote nearby bombs
        self.bomb = bomb     #value to denote if bomb/clear
        self.coord = coord #this is touple to indicate cell coordinates
    
#function to add values to each cell according num of adjacent mines
def cell_val(dim, grid = [], X = 0, Y = 0, depth = 0):
    #base cases
    #check if depth search reached (this can vary if needed)
    if depth == 2:
        #print("depth = 2")
        return 0
    #check if X/Y coordinates are out of range 
    elif X < 0 or X >= dim or Y < 0 or Y >= dim: 
        #print("out of range")
        return 0
    #check if coordinate is a bomb and increment accordingly
    elif grid[X][Y].bomb == 1:
        #print("this is bomb coordinate", X, Y)
        return 1
        
    depth += 1
    return 0 + cell_val(dim, grid, X-1, Y-1, depth) + cell_val(dim, grid, X-1,Y,
            depth) + cell_val(dim, grid, X-1, Y+1, depth) + cell_val(dim, grid, X, Y-1, depth) + cell_val(dim, grid, X, Y+1, depth ) + cell_val(dim, grid, X+1, Y-1, depth ) + cell_val(dim, grid, X+1, Y, depth ) + cell_val(dim, grid, X+1, Y+1, depth )


#function to generate minesweeper - takes in dimension of grid, probability of blocked cell, and 2d array
def mine_gen(dim, num_mines):
    grid = []
    count = 0 #number of mines
    random.seed()

    #create 2d grid
    for i in range(0,dim):
        grid.append([])
        for j in range(0,dim):
            grid[i].append(Cell(coord = (i,j))) 

    #add bombs to random coordinates according to num of mines inputted
    while count != num_mines : 
        X = random.randint(0,dim-1)  #random X coordinate
        Y = random.randint(0,dim-1)  #random Y coordinate
        
        #assign bombs randomly until number of bombs required is reached
        if grid[X][Y].bomb == 1 :  
            continue
        else :
            grid[X][Y].bomb = 1 
        
        #count number of mines placed
        count += 1
    
    #add cell value based on adjacent bombs
    for i in range(dim):
        for j in range(dim):
            grid[i][j].val = cell_val(dim, grid, X = i, Y = j)
    
    return grid



#function to generate a visual of the grid and its solution if given
def grid_visual(dim, grid, sol = []):

    #initialize visual window and create grid layout using buttons
    root = Tk()
    root.title('Minesweeper')
  
    #clickable function for minesweeper
    def mouse_press(n, row, col):
        #print("hello")
        if grid[row][col].bomb == 1:
            button[n].config(bg = "red", command = 0, relief = SUNKEN, text =
                    "X", state = DISABLED)    
        else: 
            button[n].config(relief = SUNKEN, command = 0, text =
                    grid[row][col].val, state = DISABLED, disabledforeground =
                    "blue")    
    button = []
    count = 0

    for r in range(dim): #width of grid
        for c in range(dim): #height of grid

            #create blank clickable cells
            #else:
            button.append(Button(root, relief = SOLID, text = "",
                    command = lambda n = count, row = r, col = c :
                    mouse_press(n, row, col), borderwidth = 1, bg = "light grey", width = 1))
            button[-1].grid(row=r,column=c)
    
            count += 1
    root.mainloop()
    return


def main():

    #take in user input of grid dimension and blocked cell probability
    dim = int(input("Enter grid dimension: "))
    num_mines = int(input("Enter number of mines: "))

    #1)run mine_gen
    grid = mine_gen(dim, num_mines)
    grid_visual(dim, grid)

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
