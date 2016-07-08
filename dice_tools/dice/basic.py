from .dice_base import DicePool

# Dice class to implement rolling functionality
class SimpleDice(DicePool):
    # Roll History Accessors
    @property
    def value(self):
        # Return the specified value for the dice object
        return sum(self._rolls)

class HighestRollDice(DicePool):
    @property
    def value(self):
        return max(self._rolls)

class LowestRollDice(DicePool):
    @property
    def value(self):
        return min(self._rolls)
