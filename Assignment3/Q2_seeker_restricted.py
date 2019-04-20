#solver for search and destroy -- Rutgers University -- M.Shachnai
import random
import search_and_destroy as SD

def normalize(kb, dim):
    #sum all probabilities on board 
    summ = 0
    for i in range(0,dim):
        for j in range(0,dim):
            summ += kb[i][j].prob
    #print(summ)
    #divide all cell probabilities by sum to normalize to 1
    for i in range(0,dim):
        for j in range(0,dim):
            kb[i][j].prob = kb[i][j].prob / summ
    return 

#function to create 2d array of cells to represent knowledge base
def create_kb(grid, kb, dim):
    for i in range(0,dim):
        kb.append([])
        for j in range(0,dim):
            kb[i].append(SD.Cell(coord = (i,j)))
            kb[i][j].ltype = grid[i][j].ltype
            kb[i][j].prob = 1 / (dim * dim)
    return

#function to update knowledgebase
def update_kb(kb, grid, dim, x, y, type1, type2):        
    #print(x,y)
    rand = random.random()
    #if target is found, finish search (and return 1 for finished)
    if kb[x][y].ltype == "flat":
        if grid[x][y].target == 1 and rand <= 0.9 : 
            return 1
        else:
            kb[x][y].prob = kb[x][y].prob * 0.1
    elif kb[x][y].ltype == "hill":
        if grid[x][y].target == 1 and rand <= 0.7 : 
            return 1
        else:
            kb[x][y].prob = kb[x][y].prob * 0.3
    elif kb[x][y].ltype == "forest":
        if grid[x][y].target == 1 and rand <= 0.3 : 
            return 1
        else:
            kb[x][y].prob = kb[x][y].prob * 0.7
    elif kb[x][y].ltype == "cave":
        if grid[x][y].target == 1 and rand <= 0.1 : 
            return 1
        else:
            kb[x][y].prob = kb[x][y].prob * 0.9
        
        
    #go through grid and set every cell probability that is not of type1 or type2
    #to 0 and also distibute probabilities between target cells
    if type1 == "a":
        pass
    else:
        tot = 0
        count = 0
        for i in range(0,dim):
            for j in range(0,dim):
                if kb[i][j].ltype != type1 and kb[i][j].ltype != type2:
                    #sum probabilities of irrelevant cells
                    tot += kb[i][j].prob
                    #set prob of said cells to 0
                    kb[i][j].prob = 0
                    count += 1
        dist = dim * dim - count
        for i in range(0,dim):
            for j in range(0,dim):
                if kb[i][j].ltype == type1 or kb[i][j].ltype == type2:
                    #distribute probabilities equally between target cells
                    kb[i][j].prob += tot / dist

    #normalize all other cells after failed search
    normalize(kb, dim)
    #return 0 to signal search isn't complete
    return 0

#function to simulate target movement and return landtypes moved between
def update_target_loc(kb, grid, dim, x, y):
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
            return kb[x][y].ltype, kb[x+row][y+col].ltype, x+row, y+col 


#function to find target (for moving purposes)
def find_target(grid, dim):
    for i in range(0,dim):
        for j in range(0,dim):
            if grid[i][j].target == 1:
                return i, j

#function to decide which cell to query on grid next(rule 1 and 2)
def query_cell(kb, grid, dim, rule, prev_x, prev_y):
    done = 0
    max_prob = kb[prev_x][prev_y].prob
    x = prev_x
    y = prev_y
    num_actions = 1
    
    #query cells that have highest chance of containing target (rule 1)
    if rule == 1:
    	  if prev_x-1 > -1:
    	      if kb[prev_x-1][prev_y].prob >= max_prob:
    	          max_prob = kb[prev_x-1][prev_y].prob
    	          x = prev_x-1
    	          y = prev_y
    	          num_actions = 2
    	          
    	  if prev_x+1 < dim:
    	      if kb[prev_x+1][prev_y].prob >= max_prob:
    	          max_prob = kb[prev_x+1][prev_y].prob
    	          x = prev_x+1
    	          y = prev_y
    	          num_actions = 2
    	          
    	  if prev_y+1 < dim:
    	      if kb[prev_x][prev_y+1].prob >= max_prob:
    	          max_prob = kb[prev_x][prev_y+1].prob
    	          x = prev_x
    	          y = prev_y+1
    	          num_actions = 2
    	          
    	  if prev_y-1 > -1:
    	      if kb[prev_x][prev_y-1].prob >= max_prob:
    	          max_prob = kb[prev_x][prev_y-1].prob
    	          x = prev_x
    	          y = prev_y-1
    	          num_actions = 2

    #query cells that have highest chance of finding target given it is contained in
    #cell (rule 2) 
    if rule == 2:
        if prev_x-1 > -1:
            i = prev_x-1
            j = prev_y
            if kb[i][j].ltype == "flat":
                if kb[i][j].prob * 0.9 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2

            elif kb[i][j].ltype == "hill":
                if kb[i][j].prob * 0.7 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "forest":
                if kb[i][j].prob * 0.3 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2
                
            elif kb[i][j].ltype == "cave":
                if kb[i][j].prob * 0.1 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    

        if prev_x+1 < dim:
            i = prev_x+1
            j = prev_y
            if kb[i][j].ltype == "flat":
                if kb[i][j].prob * 0.9 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    

            elif kb[i][j].ltype == "hill":
                if kb[i][j].prob * 0.7 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "forest":
                if kb[i][j].prob * 0.3 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "cave":
                if kb[i][j].prob * 0.1 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                    
        if prev_y-1 > -1:
            i = prev_x
            j = prev_y-1
            if kb[i][j].ltype == "flat":
                if kb[i][j].prob * 0.9 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    

            elif kb[i][j].ltype == "hill":
                if kb[i][j].prob * 0.7 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "forest":
                if kb[i][j].prob * 0.3 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "cave":
                if kb[i][j].prob * 0.1 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                    
        if prev_y+1 < dim:
            i = prev_x
            j = prev_y+1
            if kb[i][j].ltype == "flat":
                if kb[i][j].prob * 0.9 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    

            elif kb[i][j].ltype == "hill":
                if kb[i][j].prob * 0.7 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "forest":
                if kb[i][j].prob * 0.3 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j
                    num_actions = 2                    
                
            elif kb[i][j].ltype == "cave":
                if kb[i][j].prob * 0.1 >= max_prob:
                    max_prob = kb[i][j].prob
                    x = i
                    y = j    
                    num_actions = 2                                    

    #print("querying :", x, y)
    #print(kb[i][j].prob)
    return x, y, num_actions

#solver takes in original grid, dimension, button grid, and visual object root
def seeker(grid, dim, button = [], root = None, rule = 1):
    #function to allow AI to query a button
    tot_actions = 1
    query = lambda x, y: button[x][y].invoke()
    #rule = int(input("Enter rule(1 or 2): "))

    #1)create 2d grid that will represent agent knowledge base(KB)
    kb = []
    create_kb(grid, kb, dim)
    
    #type1 and type2 denote land types target moves between
    type1 = "a"
    type2 = "b"
    
    #t1 is x coord, t2 is y coord, of target
    t1, t2 = find_target(grid, dim)

    #2)query cell in given search and destroy grid (at random in the first query) and update KB accordingly:
    random.seed()
    x = random.randint(0,dim-1)  #random x coordinate
    y = random.randint(0,dim-1)  #random y coordinate
    
    #visually query cell
    if root != None:
        root.after(500, query, x, y)
    #print_target(grid, dim)
    
    #3)update KB based on acquired knowledge (update searched cell probability and
    #normalize all other cells to keep ratios intact) 
    found = update_kb(kb, grid, dim, x, y, type1, type2)
    type1, type2, t1, t2 = update_target_loc(kb, grid, dim, t1, t2)
    #print_prog(kb, dim)

    while found == 0:
        prev_x = x
        prev_y = y
        x, y, num_actions = query_cell(kb, grid, dim, rule, prev_x, prev_y)
        found = update_kb(kb, grid, dim, x, y, type1, type2)
        tot_actions = tot_actions+num_actions 
        type1, type2, t1, t2 = update_target_loc(kb, grid, dim, t1, t2)
        #print_prog(kb, dim)
        if root != None:
            root.after(500, query, x, y)

    return tot_actions
    
       

