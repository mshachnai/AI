class Node():
    def __init__(self, data, children, parent):
        self.data = data # this is a tuple
        self.children = children # this is a list of Nodes
        self.parent = parent #this is a Node
    
def BFS(size, maze):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Edit: I'll have to change this to incorporate class Cell later
    Returns: a list of tuples if a valid path exists. Returns None otherwise """
    
    #FOR TESTING, DELETE LATER
    maze = [[1]]
    size = 1
    #END TESTING

    if maze[0][0] == 1:
        return None

    root = Node((0,0), [], None)
    queue = []
    queue.append(root)

    ret = []

    while len(queue) != 0:
        node = queue.pop(0)

        #check if node is the goal state 
        if node.data == (size-1, size-1):
            while(node):
                ret.append(node.data)
                node = node.parent
            return ret

        #if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        
        #check right
        if col < size-1:
            if(maze[row][col+1] == 0):
                #create a new node
                rightNode = Node((row,col+1), [], node)
                #enqueue
                queue.append(rightNode)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col+1] = 2

        #check down
        if row < size -1:
            if(maze[row+1][col] == 0):
                downNode = Node((row+1, col), [], node)
                queue.append(downNode)
                node.children.append(downNode)
                maze[row+1][col] = 2

        #check up
        if row > 0:
            if(maze[row-1][col] == 0): 
                upNode = Node((row-1, col), [], node)
                queue.append(upNode)
                node.children.append(upNode)
                maze[row-1][col] = 2

        #check left
        if col > 0: 
            if(maze[row][col-1] == 0):
                leftNode = Node((row, col-1), [], node)
                queue.append(leftNode)
                node.children.append(leftNode)
                maze[row][col-1] = 2


if __name__ == "__main__":
    myList = BFS(0,0)
    print(myList)
    print("xD")


