#Probabilistic search and destroy -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from statistics import mean
import timeit as tm
import random
import copy
import seeker as sv
import Q2_seeker as sv2
import seeker_restricted as sv3
import Q2_seeker_restricted as sv4

######for later use
#DEBUG is used for turning visuals on/off: (not complete yet)
#0: will not show any visuals
#1: will show grid visuals
#2: will show plotting graphs
#3: will show all visuals
#DEBUG = 3 
RUNS = 50 #number of times each algorithm is run

#S&D will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, ltype = "flat", coord = (0,0), target = 0): 
        self.ltype = ltype     #value to denote land type 
        self.target = target     #value to denote if target(1)/clear(0)
        self.coord = coord #this is touple to indicate cell coordinates
        self.visited = 0 #value to indicate if cell has been visited
        self.prob = -1.00 #value to indicate probability of being a
        #target

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
    #sv.seeker(grid, dim, button, root)
    
    root.mainloop()
    print("\nNumber of cells searched ", score[0])
    return

#function to change target location
def update_target_loc(grid, dim, x, y):
    for i in range(40):
        #if neighboring cell is out of bound
        row = random.randint(-1,1)
        col = random.randint(-1,1)
        if x+row < 0 or x+row >= dim or y+col < 0 or y+col >=dim or (x+row == x and
                y+col == y):
            continue
        else:
            grid[x][y].target = 0
            grid[x+row][y+col].target = 1
            return x+row, y+col


#function to find target location
def find_target(grid, dim):
    for i in range(0,dim):
        for j in range(0,dim):
            if grid[i][j].target == 1:
                return i, j

def main():

    #take in user input of grid dimension and blocked cell probability
    dim = int(input("Enter grid dimension: "))
    grid = []
    if dim < 0:
        print("dimension less than 0...terminating")
        return
    score = [0]
    #target coordinates

    grid = map_gen(dim)
    x1, y1 = find_target(grid, dim)
    search_list = []
    search_list2 = []
    #grid_visual(dim, grid, score)

    #1)run mine_gen -- #2) run solver to compare between number of searches for each
    #rule(collect, update KB, take action) 
    for i in range(RUNS):
        search_list.append(sv4.seeker(grid, dim, rule = 1))
        search_list2.append(sv4.seeker(grid, dim, rule = 2))
    print("rule 1 searches same map X 50 times: ", mean(search_list))
    print("rule 2 searches same map X 50 times: ", mean(search_list2))

    search_list.clear()
    search_list2.clear()
    for i in range(RUNS):
        search_list.append(sv4.seeker(grid, dim, rule = 1))
        search_list2.append(sv4.seeker(grid, dim, rule = 2))
        #new target location for next round
        x1, y1 = update_target_loc(grid, dim, x1, y1)
    print("rule 1 searches same map X 50 times(initial target position moved): ", mean(search_list))
    print("rule 2 searches same map X 50 times(initial target position moved): ", mean(search_list2))
    
    search_list.clear()
    search_list2.clear()
    for i in range(RUNS):
        grid = map_gen(dim)
        search_list.append(sv4.seeker(grid, dim, rule = 1))
        search_list2.append(sv4.seeker(grid, dim, rule = 2))
    print("rule 1 searches X 50 times (different map): ", mean(search_list))
    print("rule 2 searches X 50 times (different map): ", mean(search_list2))
    
    return

if __name__ == "__main__":
    main()
