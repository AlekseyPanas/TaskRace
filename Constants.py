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
task_times = [3000, 50, 60, 30]

# Fonts.
helvetica_font = pygame.font.SysFont("Arial black", 25)

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

    # Loops until the chance fails
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


def combine_surfaces():
    pass


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
           Players.Player("Libros", deviation_init=100, deviation_decay=.99, surge_potency=0.6, surge_decay=.999,
                          surge=60, choke=1, skill=[5 for n in range(len(tasks))])]
