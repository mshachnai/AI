#Probabilistic solver for minesweeper -- Rutgers University -- M.Shachnai
import random
import minesweeper as ms
DELAY = 1000

def time():
    delay = 1000
    delay += DELAY
    return delay

#function to count how many valid neighbors a cell has
def count_neighbors(kb, dim, x, y):
    count = 9
    #print(x,y, " in counting")
    for i in range(-1,2):
          for j in range(-1,2):
            #if neighboring cell is out of bound subtract one neighbor
              if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                  count -= 1
                  #print("not counting: ", x+i,y+j)
            #else if neighboring cells have been visited or have 0 or 1 bomb prob                
              elif (x+i==x and y+j==y) or kb[x+i][y+j].visited==1 or kb[x+i][y+j].prob == 1 or kb[x+i][y+j].updated == 1:
                  #print("not counting: ", x+i,y+j)
                  count -= 1
    return count

def is_normalized(kb, dim, x, y):

    return 

#function to reset updated cell probabilities from last iteration
def reset_updates(kb, dim, x = -1, y = -1):
    if x != -1 and y != -1:
        for i in range(-1,2):
            for j in range(-1,2):
            #skip if neighboring cells out of bound
                if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                    continue
                else:
                    kb[x+i][y+j].updated = 0
    else:
        for i in range(0,dim):
            for j in range(0,dim):
                kb[i][j].updated = 0

#function to sum up neighboring updated cells to calculate correct probs
def sum_updated(kb, dim, x, y):
    updated_sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                #print(x,y,"skipping - out of bounds",x+i,y+j)
                continue
            #skip if neighboring cells have been visited or have 0 or 1 bomb prob
            elif kb[x+i][y+j].updated == 1 or kb[x+i][y+j].bomb == 1:
                #print("adding to sum", x+i, y+j, kb[x+i][y+j].prob)
                updated_sum += kb[x+i][y+j].prob
    return updated_sum
    
#function to count bombs and assign prob 0 to every neighbor if number of bombs
#equals value of cell
def bomb_update(kb, dim, x, y):
    num_bombs = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                #print(x,y,"skipping - out of bounds",x+i,y+j)
                continue
            #skip if neighboring cells have been visited or have 0 or 1 bomb prob
            elif kb[x+i][y+j].prob == 1 or kb[x+i][y+j].bomb == 1:
                num_bombs += 1
    if num_bombs == kb[x][y].val:
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                    continue
                elif kb[x+i][y+j].prob == 1 or kb[x+i][y+j].bomb == 1:
                    continue
                else:
                    kb[x+i][y+j].bomb = 0
                    kb[x+i][y+j].prob = 0


#function to add probabilities to neighboring cells
def assign_probabilities(kb, button, dim, root, x, y, count):
    sum_of_updated = 0
    update_list = []
    unknown = lambda x, y: button[x][y].config(text = kb[x][y].prob)
    boom = lambda x, y: button[x][y].config(text = "Boom", foreground = "red")
    #print(x,y, " in assign probs")

    for i in range(-1,2):
        for j in range(-1,2):
            #skip if neighboring cells are out of bound 
            if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim:
                #print("skipping - out of bounds",x+i,y+j)
                continue
            #skip if neighboring cells have been visited or have 0 or 1 bomb prob
            elif (x+i==x and y+j==y) or kb[x+i][y+j].visited==1 or kb[x+i][y+j].prob == 1 :
                #print("skipping - not out of bounds",x+i,y+j)
                continue
            else:
                #show probabilities of neighboring cells
                #print("not skipping ",x+i,y+j)
                #print("count = ", count)
                #print( kb[x+i][y+j].prob < 0, kb[x+i][y+j].updated == 0)
                if kb[x+i][y+j].prob < 0 or kb[x+i][y+j].updated == 0:
                    if count == 0:
                        #print("in this case")
                        kb[x+i][y+j].prob = 0
                    else:
                        update_list.insert(0,kb[x+i][y+j])
                        sum_of_updated = sum_updated(kb, dim, x, y)
                        #print("updated sum = ", sum_of_updated)
                        if kb[x][y].val / count - sum_of_updated <= 0: 
                            kb[x+i][y+j].prob = 0
                        else:
                            kb[x+i][y+j].prob = round(kb[x][y].val / count - sum_of_updated, 2)
                        #print(x,y, " val =", kb[x][y].val, "count = ", count, "sum =", sum_of_updated)
                        #######this is to show probabilities
                        #root.after(500, unknown, x+i, y+j)
                
    #flag cells that have been updated
    for i in range (len(update_list)):
        update_list[i].updated = 1

#function to create 2d array of cells to represent knowledge base
def create_kb(kb, dim):
    for i in range(0,dim):
        kb.append([])
        for j in range(0,dim):
            kb[i].append(ms.Cell(-1, (i,j), -1))

#function to uncover all bordering zeroes and assign proper values to them
def zero_bfs_assign(kb, grid, button, root, cell, q, dim):
    #print("in bfs")
    x = cell.coord[0]
    y = cell.coord[1]
    for i in range(-1,2):
        for j in range(-1,2):
            #print(cell.coord[0]+i,cell.coord[1]+j)
            #if cells are out of bounds, ignore
            if x+i < 0 or x+i >= dim or y+j < 0 or y+j >=dim: #or (x+i == x and y+j == y):
                #print("skip")
                continue
            #else update cell value and check for more zeroes
            else:
                kb[x+i][y+j].val = grid[x+i][y+j].val
                #if cell value is not 0, update and continue
                if kb[x+i][y+j].val > 0:
                    kb[x+i][y+j].bomb = 0
                    kb[x+i][y+j].prob = 0
                    kb[x+i][y+j].visited = 1
                #else if cell value is 0, update and add to queue
                else:
                    kb[x+i][y+j].bomb = 0
                    kb[x+i][y+j].prob = 0
                    #kb[x+i][y+j].visited = 1
                    q.append(grid[x+i][y+j])

#function to update knowledgebase
def update_kb(kb, grid, button, root, dim, x, y):        
    #print(x,y)
    if grid[x][y].bomb == 1:
        kb[x][y].bomb = 1
        kb[x][y].prob = 1
        kb[x][y].visited = 1
        return
        #root.after(DELAY+100, boom, x, y)

    elif grid[x][y].val == 0:
        #print(x,y)
        kb[x][y].val = 0
        kb[x][y].bomb = 0
        kb[x][y].prob = 0
        #uncover neighboring cells before adding probabilities
        q = []
        q.append(grid[x][y])
        while len(q) != 0:
            cell = q.pop()
            if kb[cell.coord[0]][cell.coord[1]].visited == 1:
                continue
            else:
                zero_bfs_assign(kb, grid, button, root, cell, q, dim)
                kb[cell.coord[0]][cell.coord[1]].visited = 1
 
    #this is the case where cell is not bomb and is not val == 0
    else: 
        kb[x][y].val = grid[x][y].val
        kb[x][y].bomb = 0
        kb[x][y].prob = 0
        kb[x][y].visited = 1
   
    #assign probabilities to neighbors 
    for i in range(0,dim):
        for j in range(0,dim):
            if kb[i][j].visited == 1:
                #count valid neighboring cells
                count = count_neighbors(kb, dim, i, j)
                #print(i,j, f"sum updated:  {sum_updated(kb, dim, i, j)}")
                #if i == 1 and j == 2: return
                if sum_updated(kb, dim, i, j) < kb[i][j].val and count == 0:
                    #print(i,j, "in end case------------------------")
                    reset_updates(kb, dim, i, j)
                    count = count_neighbors(kb, dim, i, j)
                #add probabilities to neighboring cells
                assign_probabilities(kb, button, dim, root, i, j, count) 

#function to decide which cell to query on grid next
def query_cell(kb, grid, dim, root):
    terminate = 1
    #query cells that have no bombs in them and haven't been visited
    for i in range(0,dim):
        for j in range(0,dim):
            if kb[i][j].prob == 0 and kb[i][j].visited == 0 and kb[i][j].bomb != 1:
                terminate = 0
                #print(1)
                x = i
                y = j
                return x, y
    #query cells that we know nothing about
    for i in range(0,dim):
        for j in range(0,dim):
            if kb[i][j].prob < 0 and kb[i][j].visited == 0 and kb[i][j].bomb != 1 :
                terminate = 0
                #print(2)
                x = i
                y = j
                return x, y
    #query cells with the lowest probability of exploding
    min = 1
    for i in range(0,dim):
        for j in range(0,dim):
            if kb[i][j].prob > 0 and kb[i][j].prob < 1 and kb[i][j].visited == 0 and kb[i][j].bomb != 1:
                if min > kb[i][j].prob:
                    terminate = 0
                    #print(2)
                    min = kb[i][j].prob
                    x = i
                    y = j
    if terminate == 1:
        return -1, -1
    #print("returning ", x,y)
    return x, y



#solver takes in original grid, dimension, button grid, and visual object root
def solver(grid, dim, button, root):
    #function to allow AI to query a button
    query = lambda x, y: button[x][y].invoke()
    #function to allow AI to flag suspected bomb cells
    unknown = lambda x, y: button[x][y].config(text = kb[x][y].prob)
    boom = lambda x, y: button[x][y].config(text = "Boom", foreground = "red")


    #1)create 2d grid that will represent agent knowledge base(KB)
    kb = []
    create_kb(kb, dim)
    
    #2)query cell in given minesweeper grid (at random in the first query) and update KB accordingly:
    #track cell value and given probability of bomb in each neighboring cell
    random.seed()
    x = 1
    y = 1
    #x = random.randint(0,dim-1)  #random x coordinate
    #y = random.randint(0,dim-1)  #random y coordinate
    #visually query cell
    root.after(500, query, x, y)
    #print("queried cell 1: ", x,y)
    
    #3)update KB based on acquired knowledge
    #reset updated cell probabilities from last iteration
    update_kb(kb, grid, button, root, dim, x, y)
    reset_updates(kb, dim)
    
    for i in range(dim*dim):
        x, y = query_cell(kb, grid, dim, root)
        if x == -1 and y == -1:
            return
        #print(f"queried cell {i+2} : ", x,y)
        update_kb(kb, grid, button, root, dim, x, y)
        root.after(time(), query, x, y)

   
    #4)go through kb and look for any cells with prob > 1 and indicate those as bombs
        for i in range(0,dim):
            for j in range(0,dim):
                if kb[i][j].prob >= 1:
                    kb[i][j].bomb = 1
                    kb[i][j].prob = 1
                    root.after(time(), boom, i, j)

   #5)update kb based new knowledge
    #update_kb(kb, grid, button, root, dim, 1, 1)
        for i in range(0,dim):
            for j in range(0,dim):
                if kb[i][j].visited == 1:
                    #print(i,j)
                    bomb_update(kb, dim, i, j)
        

        #for i in range(0,dim):
        #    for j in range(0,dim):
        #        print(kb[i][j].val, kb[i][j].prob, kb[i][j].updated)

    

    

