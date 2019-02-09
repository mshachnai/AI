from maze_gen import maze_gen

def generateHardMaze(size):
    #create a random maze 
    #do random starting probabilities until we find a good one

    dim = int(input("Enter maze dimensions: "))
    prob = float(input("Enter starting probability: "))
    beamSize = int(input("Enter beam size: "))

    maze = maze_gen(dim, prob)
    
    #this is a queue of mazes. 
    queue = []

    queue.append(maze)

    while len(queue) != 0:
        currMaze = queue.pop(0)



   
def mazeEval(maze, search, metric):
    """ mazeEval evaluates a maze based on characteristics such as 
            the length of the shortest path 
            number of nodes expended while solving 
            maximum size of fringe 
        note that all of these are measured in relation to their dimension

        search is a string that is either ["bfs", "dfs", "astare", "astarm"]
        metric is an int that corresponds to a metric. The mapping can be described as follows:
                {0: "maximal shortest path", 1: "maximal fringe size", 2: maximal nodes expanded}
    """

    if search not in ["bfs", "dfs", "astare", "astarm"]:
        print("invalid search type")
        return -1

    if metric not in [0,1,2]:
        print("invalid metric")
        return -1

    if search == "bfs":
        return 
    elif search == "dfs":     
        return 
    elif search == "astare":
        return 
    elif search == "astarm":
        return








