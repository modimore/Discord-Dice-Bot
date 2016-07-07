from .dice_base import DiceBase

# Dice class to implement rolling functionality
class SimpleDice(DiceBase):
    # Roll History Accessors
    @property
    def value(self):
        # Return the specified value for the dice object
        return self.total

class HighestRollDice(DiceBase):
    @property
    def value(self):
        return self.highest

class LowestRollDice(DiceBase):
    @property
    def value(self):
        return self.lowest
