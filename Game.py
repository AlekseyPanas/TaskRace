import Constants


class Game:
    def __init__(self):
        pass

    @staticmethod
    def run_game(screen):
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
