import Constants
import time
import math
import pygame
from PIL import Image, ImageFilter


class Game:
    def __init__(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        # Is game paused
        self.paused = False
        # The process of pausing the game (Animation)
        self.pausing = False
        # Variable makes sure blurring code runs only once when pause is pressed
        self.blurred = False
        # Surfaces used for blurring
        self.pil_blurred = 0
        self.screen_blurred = 0

        # Pause menu animation variables.
        # Used to determine how far each line has been drawn.
        self.line_pos = 0
        # The needed line position.
        self.line_pos_dest = 0

        # The paused image
        self.paused_image = Constants.paused_image
        self.paused_image_copy = None

    def game_handler(self, screen, visual):
        if self.paused:
            # Checks if escape was pressed to unpause
            if self.pausing:
                # Sets animation destinations
                self.line_pos_dest = 0

            # Runs blurring once
            if not self.blurred:
                self.blurred = True

                # Gets a blurred version of the screen surface
                self.pil_blurred = Image.frombytes('RGBA', screen.get_size(),
                                              pygame.image.tostring(screen, 'RGBA', False)).filter(
                    ImageFilter.GaussianBlur(radius=3))
                self.screen_blurred = pygame.image.fromstring(self.pil_blurred.tobytes(), self.pil_blurred.size, self.pil_blurred.mode).convert_alpha()

            # Makes sure that the timer doesn't run during pause
            self.start_time += time.time() - self.start_time - self.elapsed_time
            # Calls handler to manage pause menu.
            self.pause_handler(screen, visual)
        else:
            # Immediately freezes game upon pause and sets animation variables.
            if self.pausing:
                self.paused = True
                self.pausing = False
                # Sets animation variable.
                self.line_pos_dest = 700
            # When unpaused, this variable is set to false so image blur can run on next pause
            if self.blurred:
                self.blurred = False
            self.run_game(screen)

    def pause_handler(self, screen, visual):
        # Runs animation
        # Checks if the distance between the needed pos and current pos is within a certain range.
        if math.fabs(self.line_pos - self.line_pos_dest) > 25:
            # Moves lines towards destination.
            self.line_pos += 25 if self.line_pos < self.line_pos_dest else -25
        # If destination is reached it ensures that it didnt skip over the destination and fixes it
        elif not self.line_pos_dest == self.line_pos:
            self.line_pos = self.line_pos_dest
        # Checks if the game is being unpaused and unpauses it.
        else:
            if self.pausing:
                self.pausing = False
                self.paused = False

        # Clears entire screen
        visual.fill((0, 0, 0))
        # Blits frozen paused surface
        visual.blit(self.screen_blurred, (0, 0))
        # Creates a new alpha surface for the pause overlay
        paused_surface = pygame.Surface(Constants.SCREEN_SIZE, pygame.SRCALPHA, 32)
        # Draws a partially transparent white line at the position and paused image text
        pygame.draw.line(paused_surface, (255, 255, 255, 200), (150, 0), (150 + self.line_pos, 0 + self.line_pos), 200)
        pygame.draw.line(paused_surface, (255, 255, 255, 200), (450 - self.line_pos, 700 - self.line_pos), (450, 700), 200)
        # Sets surface transparency.
        self.paused_image_copy = self.paused_image.copy()
        self.paused_image_copy.fill((255, 255, 255, int(self.line_pos / 4.5)), None, pygame.BLEND_RGBA_MULT)
        paused_surface.blit(self.paused_image_copy, (145, 300))
        # Blits paused overlay
        visual.blit(paused_surface, (0, 0))

    def run_game(self, screen):
        screen.fill((30, 30, 30))

        # Used to track the position at which to draw each player's info
        draw_pos = 10

        # Iterates all players who are done (filtered out) and then sorts the list based on the finish time
        for player in sorted(list(filter(lambda pl: pl.done, Constants.players)), key=lambda pl: pl.finish_time):
            player.draw(screen, draw_pos)

            draw_pos += 33

        # Draws the non-finished players next (filters them out) and then reverse sorts the list based on the
        # progress in the tasks
        for player in sorted(list(filter(lambda pl: not pl.done, Constants.players)),
                             key=lambda pl: (pl.current_task_index * 100) + pl.current_percent, reverse=True):
            player.draw(screen, draw_pos)
            player.update()

            draw_pos += 33

        # The elapsed time of game
        self.elapsed_time = time.time() - self.start_time

        draw_text = str(int((time.time() - self.start_time) / 60)) + ":" + ("0" if self.elapsed_time % 60 < 10 else "") + str(round(self.elapsed_time % 60, 2))

        screen.blit(Constants.combine_surfaces((Constants.algerian_font.render("Time: ", True, (0, 0, 0)),
                                                Constants.iso_font.render(draw_text, True, (0, 0, 0)))), (10, 667))

        # Draws total elapsed time
        screen.blit(Constants.combine_surfaces((Constants.algerian_font.render("Time: ", True, (165, 165, 165)),
                                                Constants.iso_font.render(draw_text, True, (9, 255, 9)))), (7, 663))
