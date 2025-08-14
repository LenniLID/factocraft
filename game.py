import time
from noise import pnoise2
import state
from state import stored_ore


def process_mouse_click():
    if state.mouse_y is None or state.mouse_x is None:
        return

    world_x = state.mouse_x + state.camera_x
    world_y = state.mouse_y + state.camera_y
    cell_x = world_x // state.CELL_SIZE
    cell_y = world_y // state.CELL_SIZE

    if state.selector_pos == 0:
        state.placed_cells_red.add((cell_x, cell_y, state.rotation))
    elif state.selector_pos == 40:
        state.placed_cells_green.add((cell_x, cell_y, state.rotation))
    elif state.selector_pos == 80:
        state.placed_cells_blue.add((cell_x, cell_y, state.rotation))

    state.mouse_x = None
    state.mouse_y = None

def generate_ore_chunk(chunk_x, chunk_y, seed):
    if not hasattr(state, "ore_cells"):
        state.ore_cells = set()

    cells = set()
    start_x = chunk_x * state.ORE_CHUNK_SIZE
    start_y = chunk_y * state.ORE_CHUNK_SIZE

    for cx in range(start_x, start_x + state.ORE_CHUNK_SIZE):
        for cy in range(start_y, start_y + state.ORE_CHUNK_SIZE):
            value = pnoise2(cx / 20, cy / 20, octaves=3, base=seed)
            if value > state.ORE_THRESHOLD:
                cells.add((cx, cy))
                state.ore_cells.add((cx, cy))

    return cells


def miner(dt):
    for pos in state.placed_cells_red:
        rx, ry = pos[0], pos[1]  # ignore rotation
        if (rx, ry) in state.ore_cells:
            if (rx, ry) not in state.red_cell_ore_storage:
                state.red_cell_ore_storage[(rx, ry)] = 0

    state.ore_timer += dt
    while state.ore_timer >= 1.0:  # 1 second passed
        for key in state.red_cell_ore_storage:
            state.red_cell_ore_storage[key] += 1
            state.stored_ore += 1
        state.ore_timer -= 1.0

