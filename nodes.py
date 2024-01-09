import pygame as pg
import sys
import numpy as np

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (106, 223, 230)

pg.init()
fps = 60
fpsClock = pg.time.Clock()
width = height = 640
screen = pg.display.set_mode((width, width))



nodes = [[None]*8, [None]*8, [None]*8, [None]*8, [None]*8] 
radius = 5 #of node
length = len(nodes)


class Node:
    def __init__(self, x, y, velx, vely, neighbours): 
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.neighbours = neighbours
    def draw_node(self):
        pg.draw.circle(screen, WHITE, (self.x, self.y), radius)
    def update_pos(self):
        self.x += self.velx/fps
        if self.x > width:
            self.x = 0
        self.y += self.vely/fps
        if self.y > width:
            self.y = 0
        if self.y < 0:
            self.y = height

    def update_neighbours(self):
        neighbors = []       
        distances = np.array(nodes)
        for i in range(length):
            for j in range(len(nodes[i])):
                comparison = nodes[i][j]
                distances[i][j] = (comparison.x - self.x)**2 + (comparison.y - self.y)**2
        
        for i in range(7):
                neighbour = np.unravel_index(distances.argmin(), distances.shape)
                distances[neighbour] = 10000000
                neighbors.append(neighbour)
        self.neighbours = neighbors

    def draw_neighbours(self):
        npnodes = np.array(nodes) # np array = [[node, node, node, node], [node, node, node, node]]
        for neighbour in self.neighbours: # neighbours = ()
            pg.draw.line(screen, BLACK, (self.x, self.y), (npnodes[neighbour].x, npnodes[neighbour].y) )

#class Triangle:
 #   def __init__(self, colour, vertices):
 #       self.colour = colour
 #       self.vertices = vertices
 #   
 #   def update_vertices(self):
  #      pass
#
  #  def update_colour(self):
 #       pass

    

speed = 100



#initialise nodes, row by row
for i in range(length):
    l = len(nodes[i])
    space = width//l#only if more than one element in each subarray
    borderspace = space // 2
    # y = int(((length-i)/(length+1))*width) # last in array at top
    y = int(((i+1)/(length+1))*width) #first in array at the top

    for j, node in enumerate(nodes[i]):
        x = borderspace + (space * (j))
        nodes[i][j] = Node(x, y, speed/(i+1), np.random.randint(-50, 50), None)
        


def draw_nodes():
    for arr in nodes:
        for node in arr:
            node.draw_node()
            

def update_all():
    for arr in nodes:
        for node in arr:
            node.update_pos()

def draw_polygons():
    pass

for row in nodes:
    for node in row:
        node.update_neighbours()


while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()   
                
    
    screen.fill(BLUE)
    update_all()
    draw_nodes()

    for row in nodes:
        for node in row:
            node.update_neighbours()
            node.draw_neighbours()            

    pg.display.flip()
    fpsClock.tick(fps)
        
