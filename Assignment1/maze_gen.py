#Maze Generator -- INTRO TO AI 198:520 -- Rutgers University


from tkinter import *
from tkinter import ttk
import random

#maze generator will be formed using a 2d array of struct named cell
class Cell:
    #instance variables unique to each instance (with default arguments)
    def __init__(self, val = 0, heuri = 0): 
        self.val = val      
        self.heuri = heuri

#function to generate maze
def maze_gen(dim, prob, maze):
    random.seed()

    #construct 2d array from cells and assign white/black cells based on
    #given probability
    maze = []
    for i in range(0,dim):
        maze.append([])

    for i in range(0,dim):
        for j in range(0,dim):
            rand = random.random()  #used for generating a value between 0-1
            if rand <= prob :
                maze[i].append(Cell(val = 1))
            else : 
                maze[i].append(Cell(val = 0))

    #initialize visual window
    root = Tk()

    for r in range(dim): #width of maze
        for c in range(dim): #height of maze


            if r == 0 and c == 0 :  
                button1 = Button(root, text = "S", relief = SOLID, borderwidth = 1, bg = "light blue", height = 1, width = 1 ).grid(row=r,column=c)

            elif r == dim-1 and c == dim-1 :  
                button2 = Button(root, text = "G", relief = SOLID, borderwidth = 1, bg = "light blue", width = 1 ).grid(row=r,column=c)

            elif maze[r][c].val == 1:
                button3 = Button(root, relief = SOLID, borderwidth = 1, bg = "black", width = 1).grid(row=r,column=c)
                        
            else:
                button4 = Button(root, relief = SOLID, borderwidth = 1, bg = "white", width = 1).grid(row=r,column=c)

    root.mainloop()
    return;


dim = int(input("Enter dimension: "))
prob = float(input("Enter probability: "))

maze = []
#for i in range(0,dim):
#    maze.append([])
#    
#for i in range(0,dim):
#    for j in range(0,dim):
#        maze[i].append(Cell())

#for i in range(dim) : print(maze[i][dim-1].val)
#print(for i in range(dim) : maze[i][n].val)
#c1 = Cell(2,1)
#print(c1.val, c1.heuri)

maze_gen(dim, prob, maze)
