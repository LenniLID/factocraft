import pygame
import state

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            state.mouse_x, state.mouse_y = event.pos
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
