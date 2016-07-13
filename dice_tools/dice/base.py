from ..exceptions import DiceToolsError, NotRolledError

# RNG for roll results
from random import randint

# Base dice class
# Implements straightforward rolling functionality and basic utilities
class DiceBase:
    def __init__(self, face_max, face_min=1, num_dice=1, negative=False):
        # Set high and low face values
        self._low = face_min if face_min is not None else 1
        self._high = face_max
        # Set number of dice in pool
        self._num_dice = num_dice
        # Set whether result is to be subtracted
        self._negative = negative

        if self._low > self._high or self._num_dice < 0:
            raise DiceToolsError()

    # Implementation of rolling functionality
    def roll_die(self):
        return randint(self._low, self._high)

    # Driving roll function
    def roll(self):
        # Roll dice of correct type of times specified
        self._rolls = [self.roll_die() for i in range(self._num_dice)]

    def get_spec(self):
        if self._low == 1:
            return "{0}d{1}".format(self._num_dice, self._high)
        else:
            return "{0}d{1}~{2}".format(self._num_dice, self._low, self._high)

    # Intended accessor functions
    @property
    def value(self):
        # Primary return value for DicePool
        # Implement in derived classes
        pass

    @property
    def _sign(self):
        return -1 if self._negative else 1

    @property
    def rolls(self):
        # Return the entire roll cache as a tuple
        try:
            return tuple(self._rolls)
        except:
            raise NotRolledError(self)

    @property
    def max(self):
        # Maximum possible value from rolling this group
        if not self._negative:
            return self._num_dice * self._high
        else:
            return self._num_dice * self._low * -1

    @property
    def min(self):
        # Minimum possible value from rolling this group
        if not self._negative:
            return self._num_dice * self._low
        else:
            return self._num_dice * self._high * -1

    @property
    def avg(self):
        # Average result of rolling this group
        return self._num_dice * (self._low + self._high) / 2 * self._sign

    def __str__(self):
        try:
            return "({0})".format(', '.join(str(x) for x in self.rolls))
        except NotRolledError:
            raise DiceToolsError(self.get_spec())
