from noise import pnoise2
import state



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
        for storage in state.red_cell_ore_storage:
            state.red_cell_ore_storage[storage] += 1
        state.ore_timer -= 1.0

def con_belt(dt):
    # make sure timers exist
    if not hasattr(state, "conveyor_timers"):
        state.conveyor_timers = {}  # {(x,y): elapsed_time}

    # position maps
    miner_positions = {(mx, my): rot for (mx, my, rot) in state.placed_cells_red}
    green_positions = {(gx, gy): rot for (gx, gy, rot) in state.placed_cells_green}

    # 1) advance timers
    for (gx, gy, rot) in state.placed_cells_green:
        key = (gx, gy)
        state.conveyor_timers.setdefault(key, 0.0)
        state.conveyor_timers[key] += dt

    # 2) schedule transfers (but don't apply yet)
    transfers = []              # list of (from_pos, to_pos)
    scheduled_from = set()      # sources already scheduled this tick
    scheduled_to = set()        # destinations already scheduled this tick

    for (gx, gy, rot) in state.placed_cells_green:
        key = (gx, gy)
        # handle multiple whole delays if dt is large (keeps timing consistent)
        while state.conveyor_timers[key] >= state.ORE_MOVE_DELAY:
            state.conveyor_timers[key] -= state.ORE_MOVE_DELAY

            # ensure storage exists
            state.green_cell_ore_storage.setdefault((gx, gy), 0)

            out_dx, out_dy = state.ROT_TO_DIR[rot]
            in_dx, in_dy = -out_dx, -out_dy

            # helper positions
            miner_pos = (gx + in_dx, gy + in_dy)
            con_pos   = (gx + in_dx, gy + in_dy)
            next_pos  = (gx + out_dx, gy + out_dy)

            # Try miner -> this conveyor (priority)
            if (miner_pos in miner_positions
                and (miner_pos not in scheduled_from)
                and ((gx, gy) not in scheduled_to)
                and state.green_cell_ore_storage[(gx, gy)] < 1
                and state.red_cell_ore_storage.get(miner_pos, 0) > 0):
                scheduled_from.add(miner_pos)
                scheduled_to.add((gx, gy))
                transfers.append((miner_pos, (gx, gy)))
                # one transfer per delay for this conveyor; continue to next possible delay
                continue

            # Try conveyor -> this conveyor (pull from neighbor)
            if (con_pos in green_positions
                and (con_pos not in scheduled_from)
                and ((gx, gy) not in scheduled_to)
                and state.green_cell_ore_storage.get(con_pos, 0) > 0
                and state.green_cell_ore_storage[(gx, gy)] < 1):
                scheduled_from.add(con_pos)
                scheduled_to.add((gx, gy))
                transfers.append((con_pos, (gx, gy)))
                continue

            # Try this conveyor -> next conveyor (push forward)
            if (next_pos in green_positions
                and ((gx, gy) not in scheduled_from)
                and (next_pos not in scheduled_to)
                and state.green_cell_ore_storage[(gx, gy)] > 0
                and state.green_cell_ore_storage.get(next_pos, 0) < 1):
                scheduled_from.add((gx, gy))
                scheduled_to.add(next_pos)
                transfers.append(((gx, gy), next_pos))
                continue

            # nothing to do for this delay tick — break the while loop
            break

    # 3) apply transfers (safe single-step move per scheduled transfer)
    for from_pos, to_pos in transfers:
        # subtract from source (but check availability)
        if from_pos in state.red_cell_ore_storage:
            if state.red_cell_ore_storage[from_pos] <= 0:
                continue
            state.red_cell_ore_storage[from_pos] -= 1
        elif from_pos in state.green_cell_ore_storage:
            if state.green_cell_ore_storage[from_pos] <= 0:
                continue
            state.green_cell_ore_storage[from_pos] -= 1
        else:
            # unknown source type
            continue

        # add to destination (only if empty, enforce capacity 1)
        state.green_cell_ore_storage.setdefault(to_pos, 0)
        if state.green_cell_ore_storage[to_pos] < 1:
            state.green_cell_ore_storage[to_pos] += 1

def chest_collect():
    # neighbor offsets (4 directions)
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    blue_list = getattr(state, "placed_cells_blue", [])

    # Precompute maps of positions -> rotation for quick lookups
    miner_map = {(mx, my): rot for (mx, my, rot) in state.placed_cells_red}
    green_map = {(gx, gy): rot for (gx, gy, rot) in state.placed_cells_green}

    # Ensure chest_storage exists
    state.chest_storage = getattr(state, "chest_storage", {})

    for (bx, by, _rot) in blue_list:
        chest_pos = (bx, by)
        state.chest_storage.setdefault(chest_pos, 0)

        for dx, dy in neighbors:
            src_pos = (bx + dx, by + dy)

            # Helper to check if a source at src_pos outputs into chest_pos
            def outputs_into(src_pos, src_rot):
                out = state.ROT_TO_DIR.get(src_rot)
                if not out:
                    return False
                return (src_pos[0] + out[0], src_pos[1] + out[1]) == chest_pos

            # Priority: miner first
            if src_pos in miner_map:
                src_rot = miner_map[src_pos]
                if outputs_into(src_pos, src_rot):
                    if state.red_cell_ore_storage.get(src_pos, 0) > 0:
                        state.red_cell_ore_storage[src_pos] -= 1
                        state.chest_storage[chest_pos] += 1
                        # taken from this neighbor, continue to next neighbor
                        continue

            # Then conveyor
            if src_pos in green_map:
                src_rot = green_map[src_pos]
                if outputs_into(src_pos, src_rot):
                    if state.green_cell_ore_storage.get(src_pos, 0) > 0:
                        state.green_cell_ore_storage[src_pos] -= 1
                        state.chest_storage[chest_pos] += 1
                        continue