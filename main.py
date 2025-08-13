import os

import pygame
from pygame import RESIZABLE

import state
import events
import game
import render

pygame.init()
pygame.display.set_caption('Factocraft')
screen = pygame.display.set_mode((state.WINDOW_WIDTH, state.WINDOW_HEIGHT), RESIZABLE)

clock = pygame.time.Clock()
running = True


red_arrow = pygame.image.load("red_arrow.png").convert_alpha()
red_arrow = pygame.transform.scale(red_arrow, (state.CELL_SIZE, state.CELL_SIZE))

while running:
    dt = clock.tick(60) / 1000
    running = events.handle_events()
    events.handle_keys(dt)
    game.process_mouse_click()

    screen.fill((40, 40, 40))
    render.draw_ores(screen)
    render.draw_cells(screen, red_arrow)
    render.draw_grid(screen)
    render.draw_selector(screen)

    pygame.display.update()

pygame.quit()
