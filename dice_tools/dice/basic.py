from .dice_base import DicePool

# Dice class to implement rolling functionality
class SimpleDice(DicePool):
    # Roll History Accessors
    @property
    def value(self):
        # Return the specified value for the dice object
        return sum(self._rolls)

class PickOneDice(DicePool):
    @property
    def max(self):
        return self._high

    @property
    def min(self):
        return self._low

class HighestRollDice(PickOneDice):
    @property
    def value(self):
        return max(self._rolls)

    @property
    def avg(self, num_samples=100000):
        total = 0
        for i in range(num_samples):
            total += max(self.roll_die() for i in range(self._num_dice))
        return total / num_samples

class LowestRollDice(PickOneDice):
    @property
    def value(self):
        return min(self._rolls)

    @property
    def avg(self, num_samples=100000):
        total = 0
        for i in range(num_samples):
            total += min(self.roll_die() for i in range(self._num_dice))
        return total / num_samples
