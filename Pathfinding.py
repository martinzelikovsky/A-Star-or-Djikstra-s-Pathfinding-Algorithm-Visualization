import pygame
import sys
import random
import numpy as np
import itertools
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
GREY = (105, 105, 105)
CURRENT_COL = (0, 128, 128) # Teal
END_COL = (255, 0, 255) # Magenta
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
GRID = (60, 60) # this is the number of tiles
CELL_COLOURS = np.random.choice(2, GRID, p=[0.35, 0.65]) # this is the distribution of valid and invalid tiles
BLOCK_SIZE = int(WINDOW_HEIGHT / (1.1 * GRID[0]))  # Set the size of the grid block
DIAGONAL = True # 8-directional movement if true, otherwise 4-directional movement
A_STAR = True # non-zero heuristic if true, else zero-valued heuristic and algorithm becomes Djikstra's


def draw_grid():
    '''
    This function updates the colours of the tiles to display the algorithm visualization.
    '''
    surfs = {}
    colours = (BLACK, WHITE)
    [visited_set.add(val) for val in prev_path_list] if prev_path_list else None
    for row in range(GRID[0]):
        for col in range(GRID[1]):
            surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            surf.fill(colours[CELL_COLOURS[row][col]])
            if current_loc == (row, col):
                surf.fill(CURRENT_COL)
            elif end_loc == (row, col):
                surf.fill(END_COL)
            loc = (int(1.1 * BLOCK_SIZE * row + 0.1 * BLOCK_SIZE), int(1.1 * BLOCK_SIZE * col + 0.1 * BLOCK_SIZE))
            SCREEN.blit(surf, loc)
            surfs[loc] = surf
    if visited_set:
        destination = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        destination.fill(CURRENT_COL)
        loc = (int(1.1 * BLOCK_SIZE * current_loc[0] + 0.1 * BLOCK_SIZE), int(1.1 * BLOCK_SIZE * current_loc[1] + 0.1 * BLOCK_SIZE))
        SCREEN.blit(destination, loc)
        for row, col in visited_set:
            path_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            path_tile.fill(GREY)
            loc = (int(1.1 * BLOCK_SIZE * row + 0.1 * BLOCK_SIZE), int(1.1 * BLOCK_SIZE * col + 0.1 * BLOCK_SIZE))
            SCREEN.blit(path_tile, loc)
    if path_list:
        destination = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        destination.fill(CURRENT_COL)
        loc = (int(1.1 * BLOCK_SIZE * current_loc[0] + 0.1 * BLOCK_SIZE), int(1.1 * BLOCK_SIZE * current_loc[1] + 0.1 * BLOCK_SIZE))
        SCREEN.blit(destination, loc)
        for row, col in path_list:
            path_tile = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            path_tile.fill(GREEN)
            loc = (int(1.1 * BLOCK_SIZE * row + 0.1 * BLOCK_SIZE), int(1.1 * BLOCK_SIZE * col + 0.1 * BLOCK_SIZE))
            SCREEN.blit(path_tile, loc)

def draw_path():
    '''
    This function will create a list of coordinate tuples that represent the path from the start location to the current
    location.
    '''
    global current_loc, path, path_list, temp, prev_path_list
    prev_path_list = path_list
    path_list = []
    temp_loc = current_loc
    while temp_loc in path.keys():
        temp_loc = path[temp_loc]
        path_list.insert(0, temp_loc)

def dist(current: tuple, node: tuple):
    '''
    This function returns the Euclidean distance between the current location and any other given location.
    '''
    return math.sqrt(sum((np.array(current) - np.array(node))**2))

def take_step():
    '''
    Here I am going to run the actual A* algorithm and update the position of the cursor block.
    Diagonal steps allowed
    '''
    global f, g, current_loc, end_loc, open_list, path, path_found

    if open_list:
        open_list.sort(key=lambda val: val[1]) # sorts locations in open_list by their F-score
        current_loc = open_list.pop(0)[0] # current location becomes the location with the lowest F-score
        draw_path() # draw path
        if current_loc == end_loc:
            path_found = True
        if DIAGONAL: # if 8-directional movement
            neighbour_list = [(current_loc[0] + row, current_loc[1] + col) for row, col in itertools.product([-1, 0, 1], [-1, 0, 1]) if (current_loc[0] + row, current_loc[1] + col) in valid_list and (row, col) != (0, 0)]
        else: # 4-directional movement
            neighbour_list = [(current_loc[0] + row, current_loc[1] + col) for row, col in [(0, -1), (0, 1), (1, 0), (-1, 0)] if (current_loc[0] + row, current_loc[1] + col) in valid_list]
        for neighbour in neighbour_list:
            g_neighbour = g[current_loc] + dist(current_loc, neighbour) # G-score for neighbour
            if g_neighbour < g[neighbour]: # if G-score of neighbour is lesser than the previous G-score for that location (default value is infinity)
                path[neighbour] = current_loc # add current location to path from neighbour
                g[neighbour] = g_neighbour # Update the G-score of the neighbour to the dictionary of neighbours
                h = dist(neighbour, end_loc) if A_STAR else 0 # for A* there is a non-zero heuristic; for Djikstra's the heuristic is zero-valued
                f[neighbour] = g_neighbour + h # Update the F-score of the neighbour to the dictionary of neighbours
                open_list.append((neighbour, f[neighbour])) if neighbour not in [open_list[0] for _ in open_list] else None # if neighbour is not in the open set, add it back in

def main():
    '''
    This is the main game function.
    '''
    global SCREEN, CLOCK, current_loc, end_loc, valid_list, blocked_list, f, g, h, open_list, path, path_list, path_found, prev_path_list, visited_set
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f'{"A*" if A_STAR else "Djikstra`s"} Pathfinding visualization with {"8-directional" if DIAGONAL else "4-directional"} movement')
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
    path = {}
    path_list = None
    prev_path_list = None
    visited_set = set()
    path_found = False
    open_list = [(current_loc, dist(current_loc, end_loc))] # maybe come back but I think this should be fine for now
    while True: # this is the main game loop. Each iteration of this loop will show a step of a trial path taken by the algorithm
        pygame.time.delay(3) # this is a delay to bound the refresh rate of the visualization
        draw_grid()
        take_step() if not path_found else None # stop updating paths and locations if the path to goal is found
        pygame.display.update() # Updates display
        for event in pygame.event.get(): # quits game if game window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
