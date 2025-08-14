import pygame
import state
from state import camera_x

cell_x = 0
cell_y = 0

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            state.mouse_x, state.mouse_y = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                state.rotation -= 90
                if state.rotation == 0:
                    state.rotation = 360
    return True

def handle_keys(dt):
    keys = pygame.key.get_pressed()
    dx = dy = 0

    if keys[pygame.K_LEFT]:
        dx -= 1
    if keys[pygame.K_RIGHT]:
        dx += 1
    if keys[pygame.K_UP]:
        dy -= 1
    if keys[pygame.K_DOWN]:
        dy += 1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                state.rotation += 90
                if state.rotation >= 360:
                    state.rotation = 0

    length = (dx ** 2 + dy ** 2) ** 0.5
    if length:
        dx /= length
        dy /= length

    state.camera_x += dx * state.SPEED * dt
    state.camera_y += dy * state.SPEED * dt

    if keys[pygame.K_1]:
        state.selector_pos = 0
    elif keys[pygame.K_2]:
        state.selector_pos = 40
    elif keys[pygame.K_3]:
        state.selector_pos = 80

    global cell_x, cell_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell_x = int((mouse_x + state.camera_x) // state.CELL_SIZE)
    cell_y = int((mouse_y + state.camera_y) // state.CELL_SIZE)

