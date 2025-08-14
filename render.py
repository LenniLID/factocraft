import pygame
from noise import pnoise2
import state
import events

def draw_grid(screen):
    width, height = screen.get_size()
    for x in range(0, width + state.CELL_SIZE, state.CELL_SIZE):
        screen_x = x - (state.camera_x % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (screen_x, 0), (screen_x, height))

    for y in range(0, height + state.CELL_SIZE, state.CELL_SIZE):
        screen_y = y - (state.camera_y % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (0, screen_y), (width, screen_y))

def draw_cells(screen, red_arrow, green_arrow, blue_arrow):
    # Draw red clicked cells
    for (cx, cy, rot) in state.clicked_cells_red:
        screen_x = cx * state.CELL_SIZE - state.camera_x
        screen_y = cy * state.CELL_SIZE - state.camera_y
        rotated_image = pygame.transform.rotate(red_arrow, rot)
        screen.blit(rotated_image, (screen_x, screen_y))

    # Draw green clicked cells
    for (cx, cy, rot) in state.clicked_cells_green:
        screen_x = cx * state.CELL_SIZE - state.camera_x
        screen_y = cy * state.CELL_SIZE - state.camera_y
        rotated_image = pygame.transform.rotate(green_arrow, rot)
        screen.blit(rotated_image, (screen_x, screen_y))

    # Draw blue clicked cells
    for (cx, cy, rot) in state.clicked_cells_blue:
        screen_x = cx * state.CELL_SIZE - state.camera_x
        screen_y = cy * state.CELL_SIZE - state.camera_y
        rotated_image = pygame.transform.rotate(blue_arrow, rot)
        screen.blit(rotated_image, (screen_x, screen_y))

def draw_selector(screen):
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 40, 40))
    pygame.draw.rect(screen, (0, 255, 0), (40, 0, 40, 40))
    pygame.draw.rect(screen, (0, 0, 255), (80, 0, 40, 40))
    pygame.draw.rect(screen, (0, 0, 0), (state.selector_pos, 0, 40, 40), 5)

def draw_ores(screen):
    width, height = screen.get_size()

    start_x = int(state.camera_x // state.CELL_SIZE) - 1
    end_x = int((state.camera_x + width) // state.CELL_SIZE) + 1
    start_y = int(state.camera_y // state.CELL_SIZE) - 1
    end_y = int((state.camera_y + height) // state.CELL_SIZE) + 1

    for cx in range(start_x, end_x):
        for cy in range(start_y, end_y):
            value = pnoise2(cx / 20, cy / 20, octaves=3, base=state.SEED)
            if value > state.ORE_THRESHOLD:
                # save ore cell coordinates
                state.ore_cells.add((cx, cy))

                # draw it
                screen_x = cx * state.CELL_SIZE - state.camera_x
                screen_y = cy * state.CELL_SIZE - state.camera_y
                pygame.draw.rect(screen, (139, 69, 19), (screen_x, screen_y, state.CELL_SIZE, state.CELL_SIZE))


def ghost_preview(screen, red_arrow, green_arrow, blue_arrow):
    if state.selector_pos == 0:
        selected_cell = red_arrow
    elif state.selector_pos == 40:
        selected_cell = green_arrow
    elif state.selector_pos == 80:
        selected_cell = blue_arrow
    else:
        return

    ghost_image = selected_cell.copy().convert_alpha()
    ghost_image.set_alpha(128)

    # Convert world coords to screen coords for drawing
    screen_x = events.cell_x * state.CELL_SIZE - state.camera_x
    screen_y = events.cell_y * state.CELL_SIZE - state.camera_y

    screen.blit(pygame.transform.rotate(ghost_image, state.rotation), (screen_x, screen_y))
