import math
import random

# Display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 30
SPEED = 1000

# Camera
camera_x = 0
camera_y = 0

# Mouse and selector
mouse_x = None
mouse_y = None
selector_pos = 0

# Cells
clicked_cells_red = set()
clicked_cells_green = set()
clicked_cells_blue = set()
rotation = 360

# Ores
ore_cells = set()
ORE_THRESHOLD = 0.3
SEED = random.randint(0, 32767)
ORE_CHUNK_SIZE = 32
ore_chunks = {}
