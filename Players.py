import Constants
import math
import random


class Parent:
    def __init__(self, name):
        # To make each entry in the list move switch positions gradually a velocity variable is used.
        self.velocity = 0
        self.pos = 0
        self.needed_pos = 0
        # If all tasks are done.
        self.done = False
        # Name of player.
        self.name = name
        # Finish time in seconds.
        self.finish_time = 0
        # The index of the task currently being done.
        self.current_task_index = 0
        # Progress in current task.
        self.current_percent = 0
        # Used to calculate player's place.
        self.place = 0
        # What to blit (Done vs not Done).
        self.blitting_text = ""
        # The combination of all text surfaces that will be drawn.
        self.combined_surface = 0

    def update(self):
        pass

    def draw(self, screen, needed_pos):
        # Calculates the place of this player in the list.
        self.place = int(needed_pos / 33) + 1

        # Checks if the entry needs to be moved.
        if not needed_pos == self.pos:
            self.velocity = (needed_pos - self.pos) / 20

        # Ends movement once done.
        if math.fabs(needed_pos - self.pos) <= self.velocity * 2:
            self.pos = needed_pos
            self.velocity = 0

        # Moves entry.
        self.pos += self.velocity

        self.blitting_text = Constants.combine_surfaces(
            (Constants.arial_font.render("Done in ", True, (0, 255, 219)),
             Constants.arial_font.render(str(self.finish_time) + "s", True, (0, 255, 0)))) if self.done else Constants.combine_surfaces((
              Constants.arial_font.render(Constants.tasks[self.current_task_index] + " ", True, (255, 255 - ((250 / len(Constants.tasks)) * self.current_task_index), 255)),
              Constants.arial_font.render(str(self.current_percent) + "%", True, (255, 255, 0))))

        screen.blit(
            Constants.combine_surfaces(
                (Constants.helvetica_font.render(str(self.place) + ". ", True, (255, (255 / len(Constants.players)) * (len(Constants.players) - self.place), 0)),
                 Constants.arial_black_font.render(self.name + "   ", True, (120, 200, (200 / len(Constants.players)) * (len(Constants.players) - self.place))),
                 self.blitting_text)
            ), (45, self.pos))

        if self.place == 1:
            screen.blit(Constants.crown_image, (2, self.pos - 5))


class User(Parent):
    def __init__(self, name):
        super().__init__(name)
        self.count = 0
        self.user = True

    def update(self):
        self.count += 1

        if self.count >= 60:
            self.count = 0

            self.finish_time += 1

    # Called when space is pressed.
    def event(self):
        if not self.current_task_index + 1 == len(Constants.tasks):
            self.current_task_index += 1
        elif not self.done:
            # Adds fractional seconds to finish time.
            self.finish_time += round(self.count / 60, 2)
            self.done = True


class Player(Parent):
    def __init__(self, name, surge=None, surge_init=100, surge_decay=.95, surge_potency=None, choke=None, deviation_init=60, deviation_decay=.8, skill=None):
        super().__init__(name)
        # Is the player a user
        self.user = False

        # Checks for custom skill and creates its own if no custom skill is passed.
        self.skill = skill
        if self.skill is None:
            # Uses a formula to randomly create a skill
            self.skill = [round(1 + ((-.7 if random.randint(1, 2) == 1 else 1) * 0.1 * Constants.decreasing_chance_randomizer(.9, 99)), 2) for x in range(len(Constants.tasks))]
            # Ensures that skill has no negatives or 0s
            map(lambda x: 0.1 if x <= 0 else x, self.skill)
            # There is a 33% chance that the skill will get a multiplier boost.
            map(lambda x: x * (1 + (0.1 * Constants.decreasing_chance_randomizer(.95, 95))) if random.randint(1, 3) == 3 else x, self.skill)
        # Ensures that the length of the skill list corresponds the the # of tasks. Raises error otherwise
        if len(self.skill) != len(Constants.tasks):
            raise Constants.SkillLengthException

        # Counts how many times update has been called to ensure it updates only every second.
        self.count = 0
        # Progress in current task which isn't yet converted to percent.
        self.current_progress = 0

        # Deviation initial percent and the decay rate to calculate the deviation of a player's progress
        # Deviation makes it so that players get occasional progress surges or slow-downs to make the game feel more
        # alive.
        self.deviation_decay = deviation_decay
        self.deviation_init = deviation_init
        self.deviation = 0
        # The chance of being delayed in progress
        self.choke = random.randint(1, 3) if choke is None else choke
        # The percent chance that the percent will surge forward.
        self.surge = random.randint(1, 20) if surge is None else surge
        # The decay and the init % which is used to calculate the potency of the surge.
        self.surge_decay = surge_decay
        self.surge_init = surge_init
        # How potent the surge will be
        self.surge_potency = random.randint(1,3) / 10 if surge_potency is None else surge_potency

        #print(self.name + str(self.skill) + "  " + str(self.choke) + "  " + str(self.surge) + "  " + str(self.surge_potency))

    def update(self):
        # Converts to percent.
        self.current_percent = round((float(self.current_progress + (self.count * (self.skill[self.current_task_index] + self.deviation) / 60)) / float(Constants.task_times[self.current_task_index])) * 100, 2)

        self.count += 1

        # Once one second passes, runs the code.
        if self.count >= 60:
            self.count = 0

            # Adds to progress based on skill and deviation.
            self.current_progress += round(self.skill[self.current_task_index] + self.deviation, 2)

            # Calculates the deviation.
            self.deviation = (self.skill[self.current_task_index] / 3) * Constants.decreasing_chance_randomizer(self.deviation_decay, self.deviation_init)
            self.deviation *= -1 if random.choice([-1 for x in range(self.choke)] + [1]) == -1 else 1

            if self.skill[self.current_task_index] + self.deviation < 0:
                self.deviation = self.skill[self.current_task_index] / -1.2

            # Calculates surge and adds it to deviation
            if random.randint(1, 100) <= self.surge:
                self.deviation *= 1 + (self.surge_potency * Constants.decreasing_chance_randomizer(self.surge_decay, self.surge_init))
                self.deviation *= -1 if self.deviation < 0 else 1

            # Counts the finish time in seconds until all tasks are done.
            self.finish_time += 1

        # Checks if task is done.
        if self.current_percent >= 100:
            if not self.current_task_index + 1 == len(Constants.tasks):
                # Next task.
                self.current_task_index += 1
                # Resets progress
                self.current_progress = 0

            else:
                # Adds fractional seconds to finish time.
                self.finish_time += round(self.count / 60, 2)
                # Sets done to true is all tasks are done.
                self.done = True
