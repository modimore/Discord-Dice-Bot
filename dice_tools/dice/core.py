from .base import DiceBase

# Dice class to implement rolling functionality
class SimpleDice(DiceBase):
    # Roll History Accessors
    @property
    def value(self):
        # Return the specified value for the dice object
        return sum(self._rolls) * self._sign

class PickOneDice(DiceBase):
    @property
    def max(self):
        return self._high if not self._negative else self._low

    @property
    def min(self):
        return self._low if not self._negative else self._high

class HighestRollDice(PickOneDice):
    @property
    def value(self):
        return max(self._rolls) * self._sign

    @property
    def avg(self, num_samples=100000):
        total = 0
        for i in range(num_samples):
            total += max(self.roll_die() for i in range(self._num_dice))
        return total / num_samples * self._sign

class LowestRollDice(PickOneDice):
    @property
    def value(self):
        return min(self._rolls) * self._sign

    @property
    def avg(self, num_samples=100000):
        total = 0
        for i in range(num_samples):
            total += min(self.roll_die() for i in range(self._num_dice))
        return total / num_samples * self._sign
