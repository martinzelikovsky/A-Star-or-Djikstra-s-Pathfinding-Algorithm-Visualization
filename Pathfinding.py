import pygame
import sys
import random
import numpy as np
import itertools
import math
'''
I want to create a few projects that I will list below and elaborate with some detail. I'll be working on them 
sequentially because they will build on each other or just complement each other well. 

1. {short_path} Given a knwon map, a start point and a destination, determine the shortest path. I want this project be 
visualized in pygame on a two dimensional grid. 
    Requirements/steps:
        1. Map that generates itself with randomly, but allowing for a path to the node (non-segmenting map). 
        2. Ability for the user to edit the map via clicking (drawing). 
        3. The process of determining the shortest path will be visualized with a current position block (blue), viable 
        next steps (green), and dead-ends (red). The Algorithm used with be A* pathfinding algorithm. 
        
2. {frontier_exploration} Given an unknown map, a start point, and a radius of discovery a node will travel across the 
entire map and discover the entire map. 
    Requirements:
    1. Map that generates itself with randomly, but allowing for a path to the each valid point (non-segmenting map). 
    2. 


'''

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CURRENT_COL = (255, 0, 255) # Magenta
END_COL = (0, 128, 128) # Magenta
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
GRID = (15, 15)
CELL_COLOURS = np.random.choice(2, GRID, p=[0.15, 0.85])





def draw_grid():
    block_size = int(WINDOW_HEIGHT/(1.1*GRID[0])) #Set the size of the grid block
    surfs = {}
    colours = (BLACK, WHITE)
    for row in range(GRID[0]):
        for col in range(GRID[1]):
            surf = pygame.Surface((block_size, block_size))
            surf.fill(colours[CELL_COLOURS[row][col]])
            if current_loc == (row, col):
                surf.fill(CURRENT_COL)
            elif end_loc == (row, col):
                surf.fill(END_COL)
            loc = (int(1.1*block_size*row + 0.1*block_size), int(1.1*block_size*col + 0.1*block_size))
            SCREEN.blit(surf, loc)
            surfs[loc] = surf

def dist(current, node):
    return math.sqrt(sum((np.array(current) - np.array(node))**2))

def take_step(diag=True):
    '''
    Here I am going to run the actual A* algorithm and update the position of the cursor block.
    Diagonal steps allowed
    '''
    global f, g, current_loc, end_loc, open_list, path

    while open_list:
        # open_list.sort(key=lambda f_score: f.values())
        current_loc = open_list.pop(0)
        if diag:
            neighbour_list = [(current_loc[0] + row, current_loc[1] + col) for row, col in itertools.product([-1, 0, 1], [-1, 0, 1]) if (current_loc[0] + row, current_loc[1] + col) in valid_list and (row, col) != (0, 0)]
        else:
            raise NotImplementedError
        for neighbour in neighbour_list:
            if neighbour == end_loc:
                quit()
            test_g = g[current_loc] + dist(current_loc, neighbour)
            if test_g < g[neighbour]:
                path.append(neighbour)
                g[neighbour] = test_g
                f[neighbour] = test_g + dist(neighbour, end_loc)
                open_list.append(neighbour) if neighbour not in open_list else None
        break

    # if diag:
    #     neighbour_list = [(current_loc[0] + row, current_loc[1] + col) for row, col in itertools.product([-1, 0, 1], [-1, 0, 1]) if (row, col) in valid_list and (row, col) != (0, 0)]
    #     distance_tup = sorted([(neighbour, dist(current_loc, neighbour)) for neighbour in neighbour_list], key=lambda distance: distance[1]) # I don't think I need to sort this one
    # else:
    #     raise NotImplementedError
    # for neighbour, distance in distance_tup:
    #     test_path = path.copy()
    #     test_path.append(neighbour)
    #     g = sum([dist(loc_0, loc_1) for loc_0, loc_1 in [(test_path[loc], test_path[loc + 1]) for loc in range(len(test_path)-1)]]) # todo watch out for bug here lol
    #     h = dist(current_loc, end_loc)
    #     f[neighbour] = g + h
    # f_list = sorted(f.items(), key=lambda val: val[1])
    # current_loc = f_list[0][0]
    # return


def main():
    global SCREEN, CLOCK, current_loc, end_loc, valid_list, blocked_list, f, g, h, path, open_list
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('A* Pathfinding Visualization')
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    current_loc = random.choice([(row, col) for row, col in itertools.product(range(GRID[0]), range(GRID[1])) if CELL_COLOURS[row][col]])
    end_loc = random.choice([(row, col) for row, col in itertools.product(range(GRID[0]), range(GRID[1])) if CELL_COLOURS[row][col]])
    valid_list = [(row, col) for row, col in itertools.product(range(GRID[0]), range(GRID[1])) if CELL_COLOURS[row][col]]
    blocked_list = [(row, col) for row, col in itertools.product(range(GRID[0]), range(GRID[1])) if not CELL_COLOURS[row][col]]
    valid_list.append(end_loc) if end_loc not in valid_list else None
    valid_list.remove(current_loc)
    g = {key: float('inf') for key in valid_list}
    g[current_loc] = 0
    f = {key: float('inf') for key in valid_list}
    f[current_loc] = dist(current_loc, end_loc)
    path = []
    open_list = [current_loc] # maybe come back but I think this should be fine for now
    while True:
        pygame.time.delay(200)
        draw_grid()
        take_step()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
