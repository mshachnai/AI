#Minesweeper -- INTRO TO AI 198:520 -- Rutgers University -- M.Shachnai
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import timeit as tm
import random
import copy

#DEBUG is used for turning visuals on/off:
#0: will not show any visuals
#1: will show grid visuals
#2: will show plotting graphs
#3: will show all visuals
DEBUG = 3 
RUNS = 1 #number of times each algorithm is run for timing

#minesweeper will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, val = 0, heuri = 0, coord = (0,0), bomb = 0): 
        self.val = val     #value to denote nearby bombs
        self.bomb = bomb     #value to denote if bomb/clear
        self.heuri = heuri #heuristic value 
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
        #depth += 1
        #print("out of range")
        return 0
    elif grid[X][Y].bomb == 1:
        #print("this is bomb coordinat", X, Y)
        #depth += 1
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

    for i in range(dim):
        for j in range(dim):
            grid[i][j].val = cell_val(dim, grid, X = i, Y = j)
    
    return grid

#function to generate a visual of the grid and its solution if given
def grid_visual(dim, grid, sol = []):

    #initialize visual window and create grid layout using buttons
    root = Tk()
    root.title('Maze Runner')

    for r in range(dim): #width of grid
        for c in range(dim): #height of grid

            #If cell contains bomb, display it
            if grid[r][c].bomb == 1:
                button1 = Button(root, text = "X", relief = SOLID, borderwidth =
                        1, bg = "red", height = 1, width = 1 ).grid(row=r,column=c)

                """
            #bottom right cell of grid will be named 'G' - goal
            elif r == dim-1 and c == dim-1 :  
                button2 = Button(root, text = "G", command = root.destroy, relief = SOLID, borderwidth = 1, bg = "light blue", width = 1 ).grid(row=r,column=c)

            #if cell value == 1, this is a blocked cell
            elif grid[r][c].val == 1:
                button3 = Button(root, relief = SOLID, state = DISABLED, borderwidth = 1, bg = "black", width = 1).grid(row=r,column=c)
                        
            #mark path on the grid visual by checking the cell coordinate is
            #listed in the solution array, if it is - mark the specific cell
            elif (r,c) in sol:
                button4 = Button(root, relief = SOLID, state = DISABLED,
                borderwidth = 1, bg = "yellow", width =
                1).grid(row=r,column=c)"""
                        
            #for all other cases, create blank cells
            else:
                button5 = Button(root, relief = SOLID, text = grid[r][c].val,
                        borderwidth = 1, bg = "light blue", width = 1).grid(row=r,column=c)

    root.mainloop()
    return


def main():

    #take in user input of grid dimension and blocked cell probability
    dim = int(input("Enter grid dimension: "))
    num_mines = int(input("Enter number of mines: "))

    #1)run mine_gen
    grid = mine_gen(dim, num_mines)
    grid_visual(dim, grid)

    #2)run search algorithm and generate grid visual
    #if there is a path - show it with grid_visual
    #otherwise print("No path")
    """print("A* Euclidean")
    res = AStarE(grid)
    print(tm.timeit(lambda: AStarE(grid), number = RUNS))
    if DEBUG == 1 or DEBUG == 3 :
        if res is None : 
            print("No path")
        else : 
            grid_visual(dim, grid, res[0])

    print("A* Manhattan")
    res = AStarM(grid)
    print(tm.timeit(lambda: AStarM(grid), number = RUNS))
    if DEBUG == 1 or DEBUG == 3 :
        if res is None : 
            print("No path")
        else : 
            grid_visual(dim, grid, res[0])

    print("BFS")
    res = BFS(grid)
    print(tm.timeit(lambda: BFS(grid), number = RUNS))
    if DEBUG == 1 or DEBUG == 3 :
        if res is None : 
            print("No path")
        else : 
            grid_visual(dim, grid, res[0])

    print("DFS")
    res = DFS(grid)
    print(tm.timeit(lambda: DFS(grid), number = RUNS))
    if DEBUG == 1 or DEBUG == 3 :
        if res is None : 
            print("No path")
        else : 
            grid_visual(dim, grid, res[0])

    #4)plot algorithm stats with graphs
    #density vs. solvability
    array = [1,2,3,4]
    plt.plot(array, [1, 2, 3, 4], 'ro')
    plt.ylabel('density')
    plt.xlabel('solvability')
    if DEBUG == 2 or DEBUG == 3 :
        plt.show()
    
    #density vs. shortest expected path
    plt.plot([1,2,3,4], [1, 2, 7, 8], 'ro')
    plt.ylabel('density')
    plt.xlabel('shortest expected path')
    if DEBUG == 2 or DEBUG == 3:
        plt.show()"""

    return

if __name__ == "__main__":
    main()
