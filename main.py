import pygame

pygame.init()

window_width = 800
window_height = 600

game_display = pygame.display.set_mode((window_width, window_height))

lines = 0
grid = 10
start_lines = (0, 0)
end_lines = (0, 600)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for lines in grid:
        pygame.draw.line(game_display, (255, 255 ,255) ,start_lines, end_lines, 3 )
        start_lines += (30, 0)
        end_lines += (30, 0)


    pygame.display.update()
pygame.quit()