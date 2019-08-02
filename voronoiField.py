from copy import deepcopy
import numpy as np
from scipy.spatial import KDTree
from scipy.spatial import distance

ALPHA = 5.
DO_MAX = 100.
AMPLIFIER = 50.

class voronoiField:
    def __init__(self, grid, obstacles):
        self.grid = deepcopy(grid)
        self.obstacles = deepcopy(obstacles)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.obstacleList = []
        for i in range(len(self.obstacles)):
            self.obstacleList += self.obstacles[i]
        self.obstacleTree = KDTree(self.obstacleList)
        
    def generateVoronoiDiagram(self):
        self.diagram = np.zeros([self.height, self.width])
        for i in range(self.height):
            for j in range(self.width):
                closestObstacleIndex = self.obstacleTree.query([i,j],1)[1]
                obstaclePoint = self.obstacleList[closestObstacleIndex]
                for k in range(len(self.obstacles)):
                    if(obstaclePoint in self.obstacles[k]):
                        self.diagram[i][j] = k
                        break
        self.diagramEdge = np.zeros([self.height, self.width])
        delta = [[-1, 0 ], # go up
                 [ 0, -1], # go left
                 [ 1, 0 ], # go down
                 [ 0, 1 ]] # go right
        for i in range(self.height):
            for j in range(self.width):
                x = i
                y = j
                for k in range(len(delta)):
                    x2 = x + delta[k][0]
                    y2 = y + delta[k][1]
                    if(x2>=0 and x2<self.height and y2>0 and y2<self.width):
                        if(self.diagram[x][y] != self.diagram[x2][y2]):
                            self.diagramEdge[x][y] = 1
                            break
        
        self.edgeList = []
        for i in range(self.height):
            for j in range(self.width):
                if(self.diagramEdge[i][j]):
                    self.edgeList.append([i,j])
                            
        self.edgeTree = KDTree(self.edgeList)
        
    def generateVoronoiField(self):
        self.field = np.zeros([self.height,self.width])
        for i in range(self.height):
            for j in range(self.width):
                if([i,j] in self.obstacleList):
                    value = 1
                else:
                    do = self.obstacleTree.query([i,j],1)[0]
                    dv = self.edgeTree.query([i,j],1)[0]
                    if(do < DO_MAX):
                        value = (ALPHA/(ALPHA + do)) * (dv/(do + dv)) * (do-DO_MAX)**2/(DO_MAX)**2
                    else:
                        value = 0.
                self.field[i][j] = value * AMPLIFIER
                
                
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    #define a list of obstacles
    obstacles = []
    
    #you might want to see a bunch of points as ONE obstacle, like a section of line
    obstacle = []
    for i in range(30):
        obstacle.append([45,20+i])
        obstacle.append([46,20+i])
    obstacles.append(obstacle)

    obstacle = []
    for i in range(30):
        obstacle.append([30,20+i])
        obstacle.append([29,20+i])
    obstacles.append(obstacle)

    obstacle = []
    for i in range(17):
        obstacle.append([29+i,20])
        obstacle.append([29+i,21])
    obstacles.append(obstacle)

    obstacle = []
    for i in range(100):
        obstacle.append([0,0+i])
    obstacles.append(obstacle)

    obstacle = []   
    for i in range(100):
        obstacle.append([0+i,0])
    obstacles.append(obstacle)

    obstacle = []    
    for i in range(100):
        obstacle.append([99,0+i])
    obstacles.append(obstacle)

    obstacle = []    
    for i in range(100):
        obstacle.append([0+i,99])
    obstacles.append(obstacle)

    obstacle = []    
    for i in range(100):
        obstacle.append([0+i,99])
    obstacles.append(obstacle)

    obstacle = []    
    for i in range(2):
        obstacle.append([80+i,80])
    obstacles.append(obstacle)


    #define a 2D binary map, and set the obstacle position to one
    HEIGHT = 100
    WIDTH = 100
    grid = np.zeros([HEIGHT, WIDTH])
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for k in range(len(obstacles)):
                for l in range(len(obstacles[k])):
                    x = obstacles[k][l][0]
                    y = obstacles[k][l][1]
                    if(x>=0 and x<HEIGHT and y>=0 and y<WIDTH):
                        grid[x][y] = 1

    #declare a voronoi class and initial with the 2D map and obstacle list
    vor = voronoiField(grid, obstacles)
    #generate voronoi diagram
    vor.generateVoronoiDiagram()
    #generate voronoi field, must run generateVoronoiDiagram first
    vor.generateVoronoiField()

    #show the result
    fig = plt.figure()
    ax = fig.add_subplot(2,2,1)
    bx = fig.add_subplot(2,2,2)
    cx = fig.add_subplot(2,2,3)
    dx = fig.add_subplot(2,2,4)

    ax.imshow(grid)
    bx.imshow(vor.diagram)
    cx.imshow(vor.diagramEdge)
    dx.imshow(vor.field)

    plt.show()