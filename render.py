import pygame
import state

def draw_grid(screen):
    width, height = screen.get_size()
    for x in range(0, width + state.CELL_SIZE, state.CELL_SIZE):
        screen_x = x - (state.camera_x % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (screen_x, 0), (screen_x, height))

    for y in range(0, height + state.CELL_SIZE, state.CELL_SIZE):
        screen_y = y - (state.camera_y % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (0, screen_y), (width, screen_y))

def draw_cells(screen):
    for cells, color in [
        (state.clicked_cells_red, (255, 0, 0)),
        (state.clicked_cells_green, (0, 255, 0)),
        (state.clicked_cells_blue, (0, 0, 255)),
    ]:
        for (cx, cy) in cells:
            screen_x = cx * state.CELL_SIZE - state.camera_x
            screen_y = cy * state.CELL_SIZE - state.camera_y
            pygame.draw.rect(screen, color, (screen_x, screen_y, state.CELL_SIZE, state.CELL_SIZE))

def draw_selector(screen):
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, state.CELL_SIZE, state.CELL_SIZE))
    pygame.draw.rect(screen, (0, 255, 0), (40, 0, state.CELL_SIZE, state.CELL_SIZE))
    pygame.draw.rect(screen, (0, 0, 255), (80, 0, state.CELL_SIZE, state.CELL_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (state.selector_pos, 0, state.CELL_SIZE, state.CELL_SIZE), 5)
