#Probabilistic based solver to minesweeper
import random
import minesweeper as ms

class Statement():
	def __init__(self, coords, mines):
		self.coords = coords #list of tuples representing coordinates
		self.mines = mines   #number of mines distributed across these coordinates
		
		
class KBCell(): 
	def __init__(self, val, bomb, coord, visited):
		self.val = val              #value to denote nearby bombs
		self.bomb = bomb            #value to denote if bomb/clear
		self.coord = coord          #tuple to indicate cell coordinates
		self.visited = visited      #value to indicate if cell has been visited
		
		
#generates a list of tuples representing valid neighbors for a cell		
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
	

#generates number of valid neighbors for a cell		
def num_neighbors(dim, x, y):
    sum = 0
    if x+1 < dim:
        sum = sum+1
        if y+1 < dim:
            sum = sum+1
        if y-1 > 0:
            sum = sum+1
    if y+1 < dim:
        sum = sum+1
    if x-1 > 0:
        sum = sum+1
        if y+1 < dim:
            sum = sum+1
        if y-1 > 0:
            sum = sum+1
    if y-1 > 0:
        sum = sum+1
    return sum


#updates list of logical statements based on cell currently being clicked
def update_ls(ls, x, y, b):
    if len(ls) != 0:
        for s in ls:
            for c in s.coords:
                if c == (x,y):
                    s.coords.remove((x,y))
                    s.mines = s.mines-b
                    
def update_kl(kl, x, y, b):
    if kl.count(Statement((x,y), b)) == 0:
        kl.append(Statement((x,y), b))
    return
                    
def zero_bfs(c, l, dim):
    for i in range(-1,2):
        for j in range(-1,2):
            if c[0]+i < 0 or c[0]+i >= dim or c[1]+j < 0 or c[1]+j >=dim:
                continue
            else:
                l.append((c[0]+i,c[1]+j))

#solver takes in original grid, dimension, button grid, and visual object root
def solver(grid, dim, button, root):
    #1)create 2d grid mirroring agent's knowledge of grid, priority queue for which cell to check next, list of logical statements, and list of cells whose values are known
    kb = []
    q = []
    ls = [] 
    kl = []
    for i in range(0,dim):
        kb.append([])
        for j in range(0,dim):
            kb[i].append(KBCell(-1, -1, (i,j), 0))
            q.append((i,j))

    #function for pressing a button
    query = lambda x, y: button[x][y].invoke()

    #2)query cell in given minesweeper grid (at random in the first query) and update KB accordingly:
    random.seed()
    #randomize priority queue for first query
    random.shuffle(q)
    
    #while priority queue still has cells to check
    while len(q) != 0:
        #visually query cell
        c = q.pop(0)
        x = c[0]
        y = c[1]
        delay = 500
        root.after(delay, query, x, y)
        b = -1
        
        #update KB based on acquired knowledge
        #if a clear cell's value is 0, all neighbors are clear, also find bordering 0s
        #for each uncovered cell, add to list of known cells, update list of logical statements, and remove from priority queue
        if grid[x][y].val == 0:
            l = []
            l.append((x,y))
 
            while len(l) != 0:
                c = l.pop()
                i = c[0]
                j = c[1]
                if kb[i][j].visited == 1:
                    pass
                elif grid[i][j].val == 0:
                    kb[i][j].visited = 1
                    kb[i][j].bomb = 0
                    update_kl(kl, i, j, 0)
                    update_ls(ls, i, j, 0)
                    if q.count((i,j)) != 0:
                        q.remove((i,j))
                    #run function to uncover all bordering 0s
                    zero_bfs(c, l, dim)
                else:
                    kb[i][j].visited = 1
                    kb[i][j].bomb = 0
                    update_kl(kl, i, j, 0)
                    update_ls(ls, i, j, 0)
                    if q.count((i,j)) != 0:
                        q.remove((i,j))
        
        #case that checked cell is a mine
        elif grid[x][y].bomb == 1:
            kb[x][y].bomb = 1
            kb[x][y].visited = 1
            b = 1
            update_kl(kl, x, y, b)
            update_ls(ls, x, y, b)
        
        #case that checked cell is not a mine    
        else:
            kb[x][y].bomb = 0
            kb[x][y].visited = 1
            b = 0
            update_kl(kl, x, y, b)
            update_ls(ls, x, y, b)
                               
        #if a clear cell's value is equal to the number of valid neighbors, all neighbors are mines 
        #for each neighbor, add to list of known cells, update list of logical statements, and remove from priority queue       
        if grid[x][y].val == num_neighbors(dim, x, y):
            kb[x][y].val = grid[x][y].val 
            if x+1 < dim:
                update_kl(kl, x+1, y, 1)
                update_ls(ls, x+1, y, 1)
                if q.count((x+1,y)) != 0:
                    q.remove((x+1,y))
                if y+1 < dim:
                    update_kl(kl, x+1, y+1, 1)
                    update_ls(ls, x+1, y+1, 1)
                    if q.count((x+1,y+1)) != 0:
                        q.remove((x+1,y+1))
                if y-1 > 0:
                    update_kl(kl, x+1, y-1, 1)
                    update_ls(ls, x+1, y-1, 1)
                    if q.count((x+1,y-1)) != 0:
                        q.remove((x+1,y-1))
            if y+1 < dim:
                update_kl(kl, x, y+1, 1)
                update_ls(ls, x, y+1, 1)
                if q.count((x,y+1)) != 0:
                    q.remove((x,y+1))
            if x-1 > 0:
                update_kl(kl, x-1, y, 1)
                update_ls(ls, x-1, y, 1)
                if q.count((x-1,y)) != 0:
                    q.remove((x-1,y))
                if y+1 < dim:
                    update_kl(kl, x-1, y+1, 1)
                    update_ls(ls, x-1, y+1, 1)
                    if q.count((x-1,y+1)) != 0:
                        q.remove((x-1,y+1))
                if y-1 > 0:
                    update_kl(kl, x-1, y-1, 1)
                    update_ls(ls, x-1, y-1, 1)
                    if q.count((x-1,y-1)) != 0:
                        q.remove((x-1,y-1))
            if y-1 > 0:
                update_kl(kl, x, y-1, 1)
                update_ls(ls, x, y-1, 1)
                if q.count((x,y-1)) != 0:
                    q.remove((x,y-1))     	      


