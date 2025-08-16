# === Display & Camera ===
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 40
SPEED = 1000

camera_x = 0
camera_y = 0

# === Input ===
mouse_x = None
mouse_y = None
selector_pos = 0
rotation = 0  # rotation in degrees, 0 = up

# === Cells ===
placed_cells_red = set()
placed_cells_green = set()
placed_cells_blue = set()

# === Ores ===
ore_cells = set()
ORE_THRESHOLD = 0.3
SEED = 1  # or: random.randint(0, 32767)
ORE_CHUNK_SIZE = 32
ore_chunks = {}

# Miner state
red_cell_ore_storage = {}
ore_timer = 0

# === Conveyor Belts ===
green_cell_ore_storage = {}

ROT_TO_DIR = {
    0:   (0, -1),  # up
    90:  (-1, 0),  # left
    180: (0, 1),   # down
    270: (1, 0),   # right
}

ORE_MOVE_DELAY = 1.0  # seconds per move
conveyor_timers = {}

# === Chest ===
chest_storage = {}
