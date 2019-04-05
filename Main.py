import pygame
import Constants

pygame.init()

screen = pygame.Surface(Constants.SCREEN_SIZE)
visual = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)

pygame.display.set_icon(Constants.logo_image)
pygame.display.set_caption("TaskRace")

clock = pygame.time.Clock()

# Convert alpha to all images.
Constants.crown_image = Constants.crown_image.convert_alpha()
Constants.logo_image = Constants.logo_image.convert_alpha()
Constants.paused_image = Constants.paused_image.convert_alpha()

last_fps_show = 0
fps = 0
while Constants.running:
    Constants.GAME.game_handler(screen, visual)

    # Checks for every event
    for event in pygame.event.get():
        # Checks if the window was closed
        if event.type == pygame.QUIT:
            Constants.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not Constants.GAME.paused:
                list(filter(lambda pl: pl.user, Constants.players))[0].event()
            if event.key == pygame.K_ESCAPE:
                Constants.GAME.pausing = True

    # sets fps to a variable. can be set to caption any time for testing.
    last_fps_show += 1
    if last_fps_show == 30:  # every 30th frame:
        fps = clock.get_fps()
        pygame.display.set_caption("TaskRace" + "   FPS: " + str(fps))
        last_fps_show = 0

    # fps max 60
    clock.tick(60)

    # Updates display
    if not Constants.GAME.paused:
        visual.blit(screen, (0, 0))
    pygame.display.update()
