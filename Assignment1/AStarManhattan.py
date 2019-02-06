class Node():
    def __init__(self, data, children, parent, dist):
        self.data = data # this is a tuple
        self.children = children # this is a list of Nodes
        self.parent = parent #this is a Node
        self.dist = dist #this is the distance already traveled


def AStarM(size, maze):
    """Given the size and the maze itself, the target should be at position (size-1,size-1)
    and the start is at (0,0). The maze is represented as a list of lists with 0's and 1's
    Edit: I'll have to change this to incorporate class Cell later
    Returns: a list of tuples if a valid path exists. Returns None otherwise """

    if maze[0][0].val == 1:
        return None

    #need to store distance traveled to prioritize nodes
    root = Node((0, 0), [], None, 0)
    queue = []
    queue.append(root)

    ret = []

    while len(queue) != 0:
        node = queue.pop(0)

        # check if node is the goal state
        if node.data == (size - 1, size - 1):
            while (node):
                ret.append(node.data)
                node = node.parent
            return ret

        # if node is not goal state, check up/down/left/right for unvisited children
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist

        # check right
        if col < size - 1:
            if (maze[row][col + 1].val == 0):
                # create a new node
                rightNode = Node((row, col + 1), [], node, dist + 1)
                # add node by priority
                estDist = estTotalDist(dist + 1, row, col + 1, size)
                queue = insertNodeByPriority(queue, rightNode, estDist, size)
                # add new node to current node's children
                node.children.append(rightNode)
                # mark the child node as "visited"
                maze[row][col + 1].val = 2

        # check down
        if row < size - 1:
            if (maze[row + 1][col].val == 0):
                downNode = Node((row + 1, col), [], node, dist + 1)
                estDist = estTotalDist(dist + 1, row + 1, col, size)
                queue = insertNodeByPriority(queue, downNode, estDist, size)
                node.children.append(downNode)
                maze[row + 1][col].val = 2

        # check up
        if row > 0:
            if (maze[row - 1][col].val == 0):
                upNode = Node((row - 1, col), [], node, dist + 1)
                estDist = estTotalDist(dist + 1, row - 1, col, size)
                queue = insertNodeByPriority(queue, upNode, estDist, size)
                node.children.append(upNode)
                maze[row - 1][col].val = 2

        # check left
        if col > 0:
            if (maze[row][col - 1].val == 0):
                leftNode = Node((row, col - 1), [], node, dist + 1)
                estDist = estTotalDist(dist + 1, row, col - 1, size)
                queue = insertNodeByPriority(queue, leftNode, estDist, size)
                node.children.append(leftNode)
                maze[row][col - 1].val = 2


def estTotalDist(dist, row, col, size):
    #use distance already traveled and Manhattan distance to estimate total distance
    return dist + size-1-row + size-1-col


def insertNodeByPriority(queue, newNode, estDist, size):
    i = 0
    while i < len(queue):
        node = queue[i]
        data = node.data
        row = data[0]
        col = data[1]
        dist = node.dist
        if estTotalDist(dist, row, col, size) > estDist:
            #insert new node giving smaller estimated distance more priority
            queue.insert(i, newNode)
            return queue
        i = i + 1
    #if new node has highest estimated distance add to end of queue
    queue.append(newNode)
    return queue


if __name__ == "__main__":
    print(estTotalDist(10, 0, 2, 5))