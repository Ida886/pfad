import pygame
import sys

pygame.init()

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Magic_BAll")

circle_x, circle_y = 400, 300
circle_radius = 20
circle_speed = 0.5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:
        circle_x += circle_speed
    if keys[pygame.K_UP]:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN]:
        circle_y += circle_speed

    mouse_x, mouse_y = pygame.mouse.get_pos()

    color = (mouse_x % 256, mouse_y % 256, (mouse_x + mouse_y) % 256)

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, color, (circle_x, circle_y), circle_radius)

    pygame.display.flip()

pygame.quit()
sys.exit()