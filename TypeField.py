import Constants
import pygame


class Field:
    def __init__(self, pos, length):
        # Draw pos of field
        self.pos = pos
        # Is the type field selected
        self.selected = False
        # Length of the type field
        self.length = length
        # The text in the type field
        self.text = ""
        # A surface that will contain the rendered text
        self.rendered_text = None
        # The position where the cursor is
        self.cursor_index = -1
        self.cursor_pos = 0
        # Counter used for the cursor blinking
        self.blink_count = 0
        # Position of text
        self.text_pos = 10

        # The surface that everything will be blitted on
        self.surface = pygame.Surface((length, 60), pygame.SRCALPHA, 32)
        self.text_surface = pygame.Surface((length - 6, 60), pygame.SRCALPHA, 32)
        # Glass type field image
        self.image = pygame.transform.scale(Constants.field_image, (length, 60))

    def draw_handler(self, screen):
        if self.selected:
            self.blink_count += 1

        self.surface.fill((255, 255, 255, 0))
        self.text_surface.fill((255, 255, 255, 0))

        # Draws text
        self.rendered_text = Constants.impact_font.render(self.text, True, (0, 255, 0))
        self.text_surface.blit(self.rendered_text, (self.text_pos, -2))
        self.surface.blit(self.text_surface, (3, 0))

        # Finds cursor position based on index
        self.cursor_pos = Constants.impact_font.render(self.text[:self.cursor_index + 1], True, (0, 0, 0)).get_width()

        # Draws glass typing field image
        self.surface.blit(self.image, (0, 0))

        # Draws cursor
        if self.blink_count % 40 < 20 and self.selected:
            pygame.draw.line(self.surface, (200, 0, 0), ((self.text_pos - 1) + self.cursor_pos, 10),
                             ((self.text_pos - 1) + self.cursor_pos, 50), 2)

        # Determines if a shift of text is needed
        if (self.text_pos - 1) + self.cursor_pos < 0:
            self.text_pos += (0 - ((self.text_pos - 1) + self.cursor_pos)) + 10
        elif (self.text_pos - 1) + self.cursor_pos > self.length:
            self.text_pos += (self.length - ((self.text_pos - 1) + self.cursor_pos)) - 10

        screen.blit(self.surface, self.pos)

    def event_handler(self, event):
        # Checks to see if the box was clicked which causes it to become selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pos[0] < event.pos[0] < self.pos[0] + self.length and self.pos[1] < event.pos[1] < self.pos[1] + 60:
                self.selected = True
            else:
                self.selected = False
        # Key presses
        elif self.selected:
            if event.unicode == " " and event.key == pygame.K_SPACE:
                self.text = self.text[:self.cursor_index + 1] + " " + self.text[self.cursor_index + 1:]
                # Shifts cursor to right
                self.cursor_index += 1
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_index > -1:
                    self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
                    # Shifts cursor left
                    self.cursor_index -= 1

            # Checks if arrows were pressed and shifts cursor accordingly
            elif event.key == pygame.K_LEFT and self.cursor_index > -1:
                self.cursor_index -= 1
            elif event.key == pygame.K_RIGHT and self.cursor_index < len(self.text) - 1:
                self.cursor_index += 1

            elif len(event.unicode) > 0:
                self.text = self.text[:self.cursor_index + 1] + event.unicode + self.text[self.cursor_index + 1:]
                # Shifts cursor to right
                self.cursor_index += 1
