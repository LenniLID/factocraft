import math

import pygame
from pygame import RESIZABLE

pygame.init()

screen = pygame.display.set_mode((800, 600), RESIZABLE)

camera_x = 0
camera_y = 0

#just for defining
mouse_x = None
mouse_y = None
world_x = 0
world_y = 0

# pixels between grid lines
cell_size = 40

#clicked cells
clicked_cells = set()


clock = pygame.time.Clock()
speed = 200


running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

    #camera movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        dx -= 1
    if keys[pygame.K_RIGHT]:
        dx += 1
    if keys[pygame.K_UP]:
        dy -= 1
    if keys[pygame.K_DOWN]:
        dy += 1

    length = math.sqrt(dx * dx + dy * dy)
    if length != 0:
        dx /= length
        dy /= length

    camera_x += dx * speed * dt
    camera_y += dy * speed * dt

    #mouse click
    if mouse_y and mouse_x != None:
        world_x = mouse_x + camera_x
        world_y = mouse_y + camera_y

        cell_x = world_x // cell_size
        cell_y = world_y // cell_size

        clicked_cells.add((cell_x, cell_y))

    screen.fill((40, 40, 40))
    width, height = screen.get_size()

    print(clicked_cells)

    # Rectangels
    for (cx, cy) in clicked_cells:
        screen_x = cx * cell_size - camera_x
        screen_y = cy * cell_size - camera_y
        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, cell_size, cell_size))

    # Vertical lines
    for x in range(0, width + cell_size, cell_size):
        world_x = x + camera_x - (camera_x % cell_size)
        screen_x = x - (camera_x % cell_size)
        pygame.draw.line(screen, (200, 200, 200), (screen_x, 0), (screen_x, height))

    # Horizontal lines
    for y in range(0, height + cell_size, cell_size):
        world_y = y + camera_y - (camera_y % cell_size)
        screen_y = y - (camera_y % cell_size)
        pygame.draw.line(screen, (200, 200, 200), (0, screen_y), (width, screen_y))

    mouse_x = None
    mouse_y = None
    pygame.display.update()
pygame.quit()