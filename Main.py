import pygame
import Constants

pygame.init()

screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)

clock = pygame.time.Clock()

last_fps_show = 0
while Constants.running:
    screen.fill((30, 30, 30))

    Constants.GAME.run_game(screen)

    # Checks for every event
    for event in pygame.event.get():
        # Checks if the window was closed
        if event.type == pygame.QUIT:
            Constants.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                list(filter(lambda pl: pl.user, Constants.players))[0].event()

    last_fps_show += 1
    if last_fps_show == 30:  # every 30th frame:
        pygame.display.set_caption(str(clock.get_fps()))
        last_fps_show = 0

    # fps max 75
    clock.tick(60)

    pygame.display.update()
