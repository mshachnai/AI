#Probabilistic based solver to minesweeper
import random
import minesweeper as ms

#function to count how many valid neighbors a cell has
def count_neigh(kb, dim, x, y):
        count = 9
        for i in range(-1,2):
            for j in range(-1,2):
                #if neighboring cells are out of bound subtract one neighbor
                if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                    count -= 1
                #else if neighboring cells have been visited or have 0 or 1 bomb prob
                #subtract one neighbor
                elif (x+i==x and y+j==y) or kb[x+i][y+j].visited==1 or kb[x+i][y+j].prob == 0 or kb[x+i][y+j].prob == 1:
                    count -= 1
        return count

def is_normalized(kb, dim, x, y):
    return 


#solver takes in original grid, dimension, button grid, and visual object root
def solver(grid, dim, button, root):
    #1)create 2d grid that will represent agent knowledge base(KB)
    kb = []
    for i in range(0,dim):
        kb.append([])
        for j in range(0,dim):
            kb[i].append(ms.Cell(0, (i,j), 0))

    #def invoke(x, y):
        #button[x][y].invoke()
    #function for pressing a button
    query = lambda x, y: button[x][y].invoke()
    unknown = lambda x, y: button[x][y].config(text = kb[x][y].prob)

    #2)query cell in given minesweeper grid (at random in the first query) and update KB accordingly:
    #track cell value and given probability of bomb in each neighboring cell
    random.seed()
    x = random.randint(0,dim-1)  #random x coordinate
    y = random.randint(0,dim-1)  #random y coordinate
   
    #visually query cell
    delay = 500
    root.after(delay, query, x, y)
    
    #update KB based on acquired knowledge
    if grid[x][y].bomb == 1:
        kb[x][y].bomb = 1
        kb[x][y].prob = 1
        kb[x][y].visited = 1

    elif grid[x][y].val == 0:
        kb[x][y].val = 0
        kb[x][y].bomb = 0
        kb[x][y].prob = 0
        kb[x][y].visited = 1
        #add probabilities to neighboring cells
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                    #print("skip")
                    continue
                else:
                    kb[x+i][y+j].bomb = 0
                    kb[x+i][y+j].prob = 0
    #this is the case where cell is not bomb and is not 0
    else: 
        kb[x][y].val = grid[x][y].val
        kb[x][y].bomb = 0
        kb[x][y].prob = 0
        kb[x][y].visited = 1

        count = count_neigh(kb, dim, x, y)
        #add probabilities to neighboring cells
        for i in range(-1,2):
            for j in range(-1,2):
                #if neighboring cells are out of bound skip
                if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                    continue
                #else if neighboring cells have been visited or have 0 or 1 bomb prob
                elif (x+i==x and y+j==y) or kb[x+i][y+j].visited==1 or kb[x+i][y+j].prob == 0 or kb[x+i][y+j].prob == 1:
                    continue
                else:
                    #show probabilities of neighboring cells
                    root.after(delay+100, unknown, x+i, y+j)
                    kb[x+i][y+j].bomb = -1 #indicate unknown if bomb
                    if kb[x+i][y+j].prob < 0:
                        kb[x+i][y+j].prob = kb[x][y].val / count





            
        




    

