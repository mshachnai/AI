#Minesweeper -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
import copy

######for later use
#DEBUG is used for turning visuals on/off: (not complete yet)
#0: will not show any visuals
#1: will show grid visuals
#2: will show plotting graphs
#3: will show all visuals
#DEBUG = 3 
#RUNS = 1 #number of times each algorithm is run for timing

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
        x = random.randint(0,dim-1)  #random X coordinate
        y = random.randint(0,dim-1)  #random Y coordinate
        
        #assign bombs randomly until number of bombs required is reached
        if grid[x][y].bomb == 1 :  
            continue
        else :
            grid[x][y].bomb = 1 
        
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
    root = tk.Tk()
    root.title('Minesweeper')
    
    #function to find all bordering zeroes and uncovering them
    def zero_bfs(cell,q):
        for i in range(-1,2):
            for j in range(-1,2):
                #print(cell.coord[0]+i,cell.coord[1]+j)
                if cell.coord[0]+i < 0 or cell.coord[0]+i >= dim or cell.coord[1]+j < 0 or cell.coord[1]+j >=dim:
                    #print("skip")
                    continue
                else:
                    q.append(grid[cell.coord[0]+i][cell.coord[1]+j])


    #clickable function for minesweeper
    def mouse_press(row, col):
        #if bomb - show it
        if grid[row][col].bomb == 1: 
            button[row][col].config(bg = "red", disabledforeground = "black", command = 0, relief = SUNKEN, text = "X", state = DISABLED)
        #if cell value != 0 - show it
        elif grid[row][col].val > 0: 
            button[row][col].config(relief = SUNKEN, text = grid[row][col].val, state = DISABLED, disabledforeground = "blue")
        #if cell value = 0 - show it and uncover all bordering 0s
        else:
            q = []
            q.append(grid[row][col])
 
            while len(q) != 0:
                cell = q.pop()
                #print(button[cell.coord[0]][cell.coord[1]])
                #print(cell.coord[0],cell.coord[1])
                if button[cell.coord[0]][cell.coord[1]]['relief'] == "sunken":
                    #print(button[cell.coord[0]][cell.coord[1]]['relief'] == 'sunken')
                    pass
                elif cell.val == 0:
                    button[cell.coord[0]][cell.coord[1]].config(relief = SUNKEN, text = cell.val, state = DISABLED, disabledforeground = "blue")
                    #run function to uncover all bordering 0s
                    zero_bfs(cell,q)
                else:
                    button[cell.coord[0]][cell.coord[1]].config(relief = SUNKEN, text = cell.val, state = DISABLED, disabledforeground = "blue")
        
    button = []
    count = 0

    for r in range(dim): #width of grid
        button.append([])
        for c in range(dim): #height of grid

            #create blank clickable cells (functionality is in each cell)
            button[r].append(tk.Button(root, relief = SOLID, text = "", command = lambda row = r, col = c : mouse_press(row, col), borderwidth = 1, bg = "light grey", width = 1))
            button[r][-1].grid(row=r,column=c)
    
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
