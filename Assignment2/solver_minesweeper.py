#Probabilistic based solver to minesweeper
import random
import minesweeper as ms

class Statement():
	def __init__(self, coords, mines):
		self.coords = coords #list of tuples representing coordinates
		self.mines = mines   #number of mines distributed across these coordinates
		
		
class KBCell(): 
	def __init__(self, val, bomb, coord, visited):
		self.val = val     #value to denote nearby bombs
		self.bomb = bomb   #value to denote if bomb/clear
		self.coord = coord #tuple to indicate cell coordinates
		self.visited       #value to indicate if cell has been visited
		
def neigh_eval(dim, x, y):
	coords = []
	if x+1 < dim:
		coords.append((x+1,y))
		if y+1 < dim:
			coords.append((x+1,y+1))
		if y-1 > 0:
			coords.append((x+1,y-1))
	if y+1 < dim:
		coords.append((x,y+1))
		
	if x-1 > 0:
		coords.append((x-1,y))
		if y+1 < dim:
			coords.append((x-1,y+1))
		if y-1 > 0:
			coords.append((x-1,y-1))
	if y-1 > 0:
		coords.append((x,y-1))  
	return coords


#solver takes in original grid, dimension, button grid, and visual object root
def solver(grid, dim, button, root):
    #1)create 2d grid that will represent agent knowledge base(KB)
    kb = []
    statements = []
    for i in range(0,dim):
        kb.append([])
        for j in range(0,dim):
            kb[i].append(KBCell(-1, -1, (i,j), 0))

    #function for pressing a button
    query = lambda x, y: button[x][y].invoke()

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
        kb[x][y].visited = 1
        statements.append(Statement((x,y), 1))

    elif grid[x][y].val == 0:
        kb[x][y].val = 0
        kb[x][y].bomb = 0
        kb[x][y].visited = 1
        statements.append(Statement((x,y), 0))  
        if x+1 < dim:
            statements.append(Statement((x+1,y), 0))
            if y+1 < dim:
                statements.append(Statement((x+1,y+1), 0))
            if y-1 > 0:
                statements.append(Statement((x+1,y-1), 0))
            if y+1 < dim:
                statements.append(Statement((x,y+1), 0))
        if x-1 > 0:
            statements.append(Statement((x-1,y), 0))
            if y+1 < dim:
                statements.append(Statement((x-1,y+1), 0))
            if y-1 > 0:
                statements.append(Statement((x-1,y-1), 0))
            if y-1 > 0:
                statements.append(Statement((x,y-1), 0))        	      
        
    #this is the case where cell is not bomb and is not 0
    else: 
        kb[x][y].val = grid[x][y].val
        kb[x][y].bomb = 0
        kb[x][y].visited = 1
        coords = neigh_eval(dim, x, y)
        statements.append(Statement(coords, val))





            
        




    

