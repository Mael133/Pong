import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("My Pygame Window")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # --- Logica ---



    # --- Construção da tela ---
    screen.fill((255, 255, 255))



    # --- Atualiza a Tela
    pygame.display.flip()

pygame.quit()
