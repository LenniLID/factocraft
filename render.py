import pygame
from noise import pnoise2

import state
import events
from game import generate_ore_chunk


def draw_grid(screen):
    """Draw the background grid based on camera position."""
    width, height = screen.get_size()

    # Vertical lines
    for x in range(0, width + state.CELL_SIZE, state.CELL_SIZE):
        screen_x = x - (state.camera_x % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (screen_x, 0), (screen_x, height))

    # Horizontal lines
    for y in range(0, height + state.CELL_SIZE, state.CELL_SIZE):
        screen_y = y - (state.camera_y % state.CELL_SIZE)
        pygame.draw.line(screen, (200, 200, 200), (0, screen_y), (width, screen_y))


def _draw_cell(screen, arrow, rot, cx, cy, stored_ore, font):
    """Helper to draw a rotated cell with ore count text."""
    screen_x = cx * state.CELL_SIZE - state.camera_x
    screen_y = cy * state.CELL_SIZE - state.camera_y

    # Draw rotated cell
    rotated_image = pygame.transform.rotate(arrow, rot)
    screen.blit(rotated_image, (screen_x, screen_y))

    # Draw ore count
    text_surf = font.render(str(stored_ore), True, (255, 255, 255))
    text_rect = text_surf.get_rect(
        center=(screen_x + state.CELL_SIZE // 2, screen_y + state.CELL_SIZE // 2)
    )
    screen.blit(text_surf, text_rect)


def draw_cells(screen, red_arrow, green_arrow, blue_arrow, font):
    """Draw all placed cells and their ore contents."""

    # Red cells (miners)
    for (cx, cy, rot) in state.placed_cells_red:
        stored_ore = state.red_cell_ore_storage.get((cx, cy), 0)
        _draw_cell(screen, red_arrow, rot, cx, cy, stored_ore, font)

    # Green cells (belts)
    for (cx, cy, rot) in state.placed_cells_green:
        stored_ore = state.green_cell_ore_storage.get((cx, cy), 0)
        _draw_cell(screen, green_arrow, rot, cx, cy, stored_ore, font)

    # Blue cells (chests)
    for (cx, cy, rot) in state.placed_cells_blue:
        stored_ore = state.chest_storage.get((cx, cy), 0)
        _draw_cell(screen, blue_arrow, rot, cx, cy, stored_ore, font)


def draw_selector(screen):
    """Draw the selector bar at the top of the screen."""
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 40, 40))   # Red
    pygame.draw.rect(screen, (0, 255, 0), (40, 0, 40, 40))  # Green
    pygame.draw.rect(screen, (0, 0, 255), (80, 0, 40, 40))  # Blue

    # Highlight selected
    pygame.draw.rect(screen, (0, 0, 0), (state.selector_pos, 0, 40, 40), 5)


def draw_ores(screen):
    """Draw ores from generated noise-based chunks."""
    width, height = screen.get_size()

    # Visible cell range
    start_x = int(state.camera_x // state.CELL_SIZE) - 1
    end_x = int((state.camera_x + width) // state.CELL_SIZE) + 1
    start_y = int(state.camera_y // state.CELL_SIZE) - 1
    end_y = int((state.camera_y + height) // state.CELL_SIZE) + 1

    # Visible chunk range
    start_chunk_x = start_x // state.ORE_CHUNK_SIZE
    end_chunk_x = end_x // state.ORE_CHUNK_SIZE
    start_chunk_y = start_y // state.ORE_CHUNK_SIZE
    end_chunk_y = end_y // state.ORE_CHUNK_SIZE

    for chunk_x in range(start_chunk_x, end_chunk_x + 1):
        for chunk_y in range(start_chunk_y, end_chunk_y + 1):
            # Generate chunk if not cached
            if (chunk_x, chunk_y) not in state.ore_chunks:
                state.ore_chunks[(chunk_x, chunk_y)] = generate_ore_chunk(
                    chunk_x, chunk_y, state.SEED
                )

            # Draw ores in this chunk
            for (cx, cy) in state.ore_chunks[(chunk_x, chunk_y)]:
                screen_x = cx * state.CELL_SIZE - state.camera_x
                screen_y = cy * state.CELL_SIZE - state.camera_y
                pygame.draw.rect(
                    screen, (139, 69, 19),
                    (screen_x, screen_y, state.CELL_SIZE, state.CELL_SIZE)
                )


def ghost_preview(screen, red_arrow, green_arrow, blue_arrow):
    """Draw transparent preview of the currently selected cell."""
    if state.selector_pos == 0:
        selected_cell = red_arrow
    elif state.selector_pos == 40:
        selected_cell = green_arrow
    elif state.selector_pos == 80:
        selected_cell = blue_arrow
    else:
        return

    # Transparent image
    ghost_image = selected_cell.copy().convert_alpha()
    ghost_image.set_alpha(128)

    # Convert world coords to screen coords
    screen_x = events.cell_x * state.CELL_SIZE - state.camera_x
    screen_y = events.cell_y * state.CELL_SIZE - state.camera_y

    screen.blit(pygame.transform.rotate(ghost_image, state.rotation), (screen_x, screen_y))
