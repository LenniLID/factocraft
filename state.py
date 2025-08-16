import pygame

# Display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 40
SPEED = 1000

# Camera
camera_x = 0
camera_y = 0

# Mouse and selector
mouse_x = None
mouse_y = None
selector_pos = 0

# Cells
placed_cells_red = set()
placed_cells_green = set()
placed_cells_blue = set()
rotation = 360

# Ores
ore_cells = set()
ORE_THRESHOLD = 0.3
SEED = 1 #random.randint(0, 32767)
ORE_CHUNK_SIZE = 32
ore_chunks = {}

# minor
red_cell_ore_storage = {}
ore_timer = 0

# conveyor belt
green_cell_ore_storage = {}
ROT_TO_DIR = {
    0:   (0, -1),
    360: (0, -1),
    90:  (-1, 0),
    180: (0, 1),
    270: (1, 0)
}
ORE_MOVE_DELAY = 1
conveyor_timers = {}

# chest
chest_storage = {}