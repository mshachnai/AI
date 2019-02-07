AStar(5, [[0,1,0,0,0],
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,0,0,1,0]])
#output:[(4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]
#this works

AStar(5, [[0,1,0,0,0],
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,1,0,1,0],
        [0,0,0,0,0]])
#output:[(4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]
#this shows that the shortest path will be taken

AStar(1, [[0]])
#output: [(0,0)]

AStar(1, [[1]])
#output: None