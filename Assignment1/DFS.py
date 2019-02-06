class Node():
    def __init__(self, data, children, parent):
        self.data = data # this is a tuple
        self.children = children # this is a list of Nodes
        self.parent = parent #this is a Node
    
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


def DFS(size, maze):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Edit: I'll have to change this to incorporate class Cell later
    Returns: a list of tuples if a valid path exists. Returns None otherwise """

    #why do we need the size? the input just needs to be the map and we can do len(map) and len(map[0])

    #edge case: checking if the starting cell is somehow not empty
    if maze[0][0].val == 1:
        return None

    root = Node((0,0), [], None)
    fringe = Stack()
    fringe.push(root)

    ret = []

    while (fringe.isEmpty() == False):
        node = fringe.pop()

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
            if(maze[row][col+1].val == 0):
                #create a new node
                rightNode = Node((row,col+1), [], node)
                #enqueue
                fringe.push(rightNode)
                #add new node to current node's children
                node.children.append(rightNode)
                #mark the child node as "visited"
                maze[row][col+1].val = 2

        #check down
        if row < size -1:
            if(maze[row+1][col].val == 0):
                downNode = Node((row+1, col), [], node)
                fringe.push(downNode)
                node.children.append(downNode)
                maze[row+1][col].val = 2

        #check up
        if row > 0:
            if(maze[row-1][col].val == 0):
                upNode = Node((row-1, col), [], node)
                fringe.push(upNode)
                node.children.append(upNode)
                maze[row-1][col].val = 2

        #check left
        if col > 0: 
            if(maze[row][col-1].val == 0):
                leftNode = Node((row, col-1), [], node)
                fringe.push(leftNode)
                node.children.append(leftNode)
                maze[row][col-1].val = 2


if __name__ == "__main__":
    myList = DFS(0,0)
    print(myList)


