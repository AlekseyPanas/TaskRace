import Players
import pygame
import random
import Game

pygame.init()


class SkillLengthException(Exception):
    pass


SCREEN_SIZE = (600, 700)

# The tasks and their corresponding predicted completion time
tasks = ["Wash Dishes", "Wash Floor", "Do Homework", "Go to bank"]
task_times = [30, 50, 60, 30]

crown_image = pygame.transform.scale(pygame.image.load("assets/crown.png"), (40, 40))
logo_image = pygame.image.load("assets/logo.png")

# Fonts.
times_roman_font = pygame.font.SysFont("Time New Roman", 25)
helvetica_font = pygame.font.SysFont("Helvetica", 28)
arial_black_font = pygame.font.SysFont("Arial black", 25)
arial_font = pygame.font.SysFont("Arial", 28)

# is the program running
running = True

# Players who finished the entire race
done_players = []

# Holds the game instance
GAME = Game.Game()

# Utility functions
# ====================


# This randomizer runs a loop repeatedly cutting the chance of another run by the decay each time.
def decreasing_chance_randomizer(decay, initial_chance):
    # Real_chance is used to save the full decimal version of the chance for calculations.
    real_chance = initial_chance
    chance = initial_chance
    # Highest value to roll up to. Increases once the chance goes into decimals in order to remove the decimal.
    highest = 100
    roll = random.randint(1, highest)
    # The amount of times the while loop runs.
    count = 0

    # Loops until the chance fails.
    while roll <= chance:
        count += 1

        real_chance *= decay
        chance = round(real_chance, 2)
        # Checks for decimal and continuously multiplies by 10 to remove decimal.
        while chance != int(chance):
            chance *= 10
            real_chance *= 10
            highest *= 10

        roll = random.randint(1, highest)

    return count


def combine_surfaces(surfaces):
    # New surface's width and height.
    new_width = 0
    new_height = 0
    # The points at which each surface will be blitted onto the new one.
    blit_points = [0]

    for idx, surface in enumerate(surfaces):
        # Adds the width of each iterated surface to the total new width.
        new_width += surface.get_width()
        # Takes largest height of all surfaces.
        if new_height < surface.get_height():
            new_height = surface.get_height()
        # Adds the blit point for this surface.
        blit_points.append(sum(blit_points[:idx + 1]) + surface.get_width())

    # Creates new surface.
    new_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA, 32)
    # Blits onto new surface.
    for idx in range(len(surfaces)):
        new_surface.blit(surfaces[idx], (blit_points[idx], 0))

    return new_surface


# All the players
players = [Players.User("Alex"),
           Players.Player("VoidLord"),
           Players.Player("Phantom"),
           Players.Player("Carnivore"),
           Players.Player("Predator"),
           Players.Player("TalonFang"),
           Players.Player("Volca"),
           Players.Player("John Caplin"),
           Players.Player("John Conner"),
           Players.Player("Freddy"),
           Players.Player("Ericson"),
           Players.Player("Gargantuan", skill=[5.1 for y in range(len(tasks))]),
           Players.Player("Venomous", skill=[float(random.randint(1, 60)) / 10 for z in range(len(tasks))]),
           Players.Player("Rendro", skill=[float(random.randint(40, 60)) / 10 for x in range(len(tasks))]),
           Players.Player("Archetype", surge=10, choke=3, skill=[6 for p in range(len(tasks))]),
           Players.Player("Libros", deviation_init=90, deviation_decay=.99, surge_potency=0.5, surge_decay=.999,
                          surge=60, choke=1, skill=[.5 for n in range(len(tasks))])]

greatest_name_length = 0
for ply in players:
    if len(ply.name) > greatest_name_length:
        greatest_name_length = len(ply.name)

for ply in players:
    if len(ply.name) < greatest_name_length:
        ply.name = ply.name + "".join([" " for x in range(greatest_name_length - len(ply.name))])
