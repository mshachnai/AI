#Search algorithms for solving generated mazes
import copy
import math

class Node():
    def __init__(self, data, children, parent, dist = 0):
        self.data = data #this is a tuple
        self.children = children #this is a list of Nodes
        self.parent = parent #this is a Node
        self.dist = dist #this is the distance already traveled
                        #is set to 0 for DFS and BFS, because it's only considered for A*

    
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


   
def BFS(maze1):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Returns: a list of tuples if a valid path exists. Returns None otherwise"""

    size = len(maze1)

    #make a deep copy of maze to use it without changing original values
    maze = copy.deepcopy(maze1)
    if maze[0][0].val == 1:
        return None

    root = Node((0,0), [], None)
    queue = []
    queue.append(root)

    ret = []

    #initialize counters for max fringe size, max nodes expanded
    maxFringe = 0
    maxNodes = 0

    while len(queue) != 0:
        #max fringe counter
        maxFringe = max(maxFringe, len(queue))

        node = queue.pop(0)

        #check if node is the goal state 
        if node.data == (size-1, size-1):
            while(node):
                ret.append(node.data)
                node = node.parent
            return (ret, [len(ret), maxFringe, maxNodes])

        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        
        #check right
        if col < size-1:
            if(maze[row][col+1].val == 0):
                #create a new node
                rightNode = Node((row,col+1), [], node)
                #enqueue
                queue.append(rightNode)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col+1].val = 2
                #increment nodes expanded
                maxNodes+=1
        #check down
        if row < size -1:
            if(maze[row+1][col].val == 0):
                downNode = Node((row+1, col), [], node)
                queue.append(downNode)
                node.children.append(downNode)
                maze[row+1][col].val = 2
                maxNodes+=1
        #check up
        if row > 0:
            if(maze[row-1][col].val == 0):
                upNode = Node((row-1, col), [], node)
                queue.append(upNode)
                node.children.append(upNode)
                maze[row-1][col].val = 2
                maxNodes+=1
        #check left
        if col > 0: 
            if(maze[row][col-1].val == 0):
                leftNode = Node((row, col-1), [], node)
                queue.append(leftNode)
                node.children.append(leftNode)
                maze[row][col-1].val = 2
                maxNodes+=1


def DFS(maze1):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Returns: a list of tuples if a valid path exists. Returns None otherwise"""

    size  = len(maze1)

    #make a deep copy of maze to use it without changing original values
    maze = copy.deepcopy(maze1)
 
    #edge case: checking if the starting cell is somehow not empty
    if maze[0][0].val == 1:
        return None

    root = Node((0,0), [], None)
    fringe = Stack()
    fringe.push(root)

    ret = []

    #initialize counters for max fringe size, max nodes expanded
    maxFringe = 0
    maxNodes = 0

    while (fringe.isEmpty() == False):
        #max fringe counter
        maxFringe = max(maxFringe, fringe.size())
       
        node = fringe.pop()

        #check if node is the goal state 
        if node.data == (size-1, size-1):
            while(node):
                ret.append(node.data)
                node = node.parent
            return (ret, [len(ret), maxFringe, maxNodes])

        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        
        #check up
        if row > 0:
            if(maze[row-1][col].val == 0):
                #create a new node
                upNode = Node((row-1, col), [], node)
                #enqueue
                fringe.push(upNode)
                #add new node to current node's children
                node.children.append(upNode)
                #mark the child node as "visited"
                maze[row-1][col].val = 2
                #increment nodes expanded
                maxNodes+=1
        #check left
        if col > 0: 
            if(maze[row][col-1].val == 0):
                leftNode = Node((row, col-1), [], node)
                fringe.push(leftNode)
                node.children.append(leftNode)
                maze[row][col-1].val = 2
                maxNodes+=1
        #check right
        if col < size-1:
            if(maze[row][col+1].val == 0):
                rightNode = Node((row,col+1), [], node)
                fringe.push(rightNode)
                node.children.append(rightNode)
                maze[row][col+1].val = 2
                maxNodes+=1
        #check down
        if row < size -1:
            if(maze[row+1][col].val == 0):
                downNode = Node((row+1, col), [], node)
                fringe.push(downNode)
                node.children.append(downNode)
                maze[row+1][col].val = 2
                maxNodes+=1

def AStarM(maze1):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Returns: a list of tuples if a valid path exists. Returns None otherwise"""

    size = len(maze1)

    #make a deep copy of maze to use it without changing original values
    maze = copy.deepcopy(maze1)
    if maze[0][0].val == 1:
        return None

    #need to store distance traveled to prioritize nodes
    root = Node((0, 0), [], None, 0)
    queue = []
    queue.append(root)

    ret = []

    #initialize counters for max fringe size, max nodes expanded
    maxFringe = 0
    maxNodes = 0

    while len(queue) != 0:
        #max fringe counter
        maxFringe = max(maxFringe, len(queue))
        
        node = queue.pop(0)

        #check if node is the goal state
        if node.data == (size - 1, size - 1):
            while (node):
                ret.append(node.data)
                node = node.parent
            return (ret, [len(ret), maxFringe, maxNodes])


        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist

        #check right
        if col < size - 1:
            if (maze[row][col + 1].val == 0):
                #create a new node
                rightNode = Node((row, col + 1), [], node, dist + 1)
                #add node by priority
                estDist = estTotalDistM(dist + 1, row, col + 1, size)
                queue = insertNodeByPriorityM(queue, rightNode, estDist, size)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col + 1].val = 2
                #increment nodes expanded
                maxNodes+=1
        #check down
        if row < size - 1:
            if (maze[row + 1][col].val == 0):
                downNode = Node((row + 1, col), [], node, dist + 1)
                estDist = estTotalDistM(dist + 1, row + 1, col, size)
                queue = insertNodeByPriorityM(queue, downNode, estDist, size)
                node.children.append(downNode)
                maze[row + 1][col].val = 2
                maxNodes+=1
        #check up
        if row > 0:
            if (maze[row - 1][col].val == 0):
                upNode = Node((row - 1, col), [], node, dist + 1)
                estDist = estTotalDistM(dist + 1, row - 1, col, size)
                queue = insertNodeByPriorityM(queue, upNode, estDist, size)
                node.children.append(upNode)
                maze[row - 1][col].val = 2
                maxNodes+=1
        #check left
        if col > 0:
            if (maze[row][col - 1].val == 0):
                leftNode = Node((row, col - 1), [], node, dist + 1)
                estDist = estTotalDistM(dist + 1, row, col - 1, size)
                queue = insertNodeByPriorityM(queue, leftNode, estDist, size)
                node.children.append(leftNode)
                maze[row][col - 1].val = 2
                maxNodes+=1

def estTotalDistM(dist, row, col, size):
    #use distance already traveled and Manhattan distance to estimate total distance
    return dist + size-1-row + size-1-col


def AStarE(maze1):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Returns: a list of tuples if a valid path exists. Returns None otherwise"""

    size = len(maze1)

    #make a deep copy of maze to use it without changing original values
    maze = copy.deepcopy(maze1)
    if maze[0][0].val == 1:
        return None
    
    #need to store distance traveled to prioritize nodes
    root = Node((0, 0), [], None, 0)
    queue = []
    queue.append(root)

    ret = []

    #initialize counters for max fringe size, max nodes expanded
    maxFringe = 0
    maxNodes = 0

    while len(queue) != 0:
        #max fringe counter
        maxFringe = max(maxFringe, len(queue))
     
        node = queue.pop(0)

        #check if node is the goal state
        if node.data == (size - 1, size - 1):
            while (node):
                ret.append(node.data)
                node = node.parent
            return (ret, [len(ret), maxFringe, maxNodes])

        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist

        #check right
        if col < size - 1:
            if (maze[row][col + 1].val == 0):
                #create a new node
                rightNode = Node((row, col + 1), [], node, dist + 1)
                #add node by priority
                estDist = estTotalDistE(dist + 1, row, col + 1, size)
                queue = insertNodeByPriorityE(queue, rightNode, estDist, size)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col + 1].val = 2
                #increment nodes expanded
                maxNodes+=1
        #check down
        if row < size - 1:
            if (maze[row + 1][col].val == 0):
                downNode = Node((row + 1, col), [], node, dist + 1)
                estDist = estTotalDistE(dist + 1, row + 1, col, size)
                queue = insertNodeByPriorityE(queue, downNode, estDist, size)
                node.children.append(downNode)
                maze[row + 1][col].val = 2
                maxNodes+=1
        #check up
        if row > 0:
            if (maze[row - 1][col].val == 0):
                upNode = Node((row - 1, col), [], node, dist + 1)
                estDist = estTotalDistE(dist + 1, row - 1, col, size)
                queue = insertNodeByPriorityE(queue, upNode, estDist, size)
                node.children.append(upNode)
                maze[row - 1][col].val = 2
                maxNodes+=1
        #check left
        if col > 0:
            if (maze[row][col - 1].val == 0):
                leftNode = Node((row, col - 1), [], node, dist + 1)
                estDist = estTotalDistE(dist + 1, row, col - 1, size)
                queue = insertNodeByPriorityE(queue, leftNode, estDist, size)
                node.children.append(leftNode)
                maze[row][col - 1].val = 2
                maxNodes+=1
    

def estTotalDistE(dist, row, col, size):
    #use distance already traveled and Euclidean distance to estimate total distance
    return dist + math.sqrt(math.pow(size-1-row, 2) + math.pow(size-1-col, 2))

def insertNodeByPriorityM(queue, newNode, estDist, size):
    i = 0
    while i < len(queue):
        node = queue[i]
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist
        if estTotalDistM(dist, row, col, size) > estDist:
            #insert new node giving smaller estimated distance more priority
            queue.insert(i, newNode)
            return queue
        i = i + 1
    #if new node has highest estimated distance add to end of queue
    queue.append(newNode)
    return queue


def insertNodeByPriorityE(queue, newNode, estDist, size):
    i = 0
    while i < len(queue):
        node = queue[i]
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist
        if estTotalDistE(dist, row, col, size) > estDist:
            #insert new node giving smaller estimated distance more priority
            queue.insert(i, newNode)
            return queue
        i = i + 1
    #if new node has highest estimated distance add to end of queue
    queue.append(newNode)
    return queue


