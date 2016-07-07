# RNG for roll results
from random import randint

# Base dice class
# Implements straightforward rolling functionality and basic utilities
class DiceBase:
    def __init__(self, face_max, face_min=1, num_dice=0):
        # Set high and low face values
        self._low = face_min if face_min is not None else 1
        self._high = face_max

        if num_dice != 0:
            self.roll(num_dice)

    def roll_die(self):
        return randint(self._low, self._high)

    # Driving roll function
    def roll(self, num_dice=1):
        # Roll dice of correct type of times specified
        self._rolls = [self.roll_die() for i in range(num_dice)]

    @property
    def total(self):
        return sum(self._rolls)

    @property
    def rolls(self):
        # Return the entire roll cache as a tuple
        return tuple(self._rolls)

    @property
        # Get the highest roll from the roll cache
    def highest(self):
        return max(self._rolls)

    @property
    def lowest(self):
        # Get the lowest roll from the roll cache
        return min(self._rolls)
