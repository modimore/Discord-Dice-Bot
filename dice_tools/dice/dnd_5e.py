from .basic import SimpleDice

class AdvantageDice(SimpleDice):
    def roll(self, num_dice=1):
        self._rolls = []
        self._all_rolls = []

        for i in range(num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls.append(max(pair))
            self._all_rolls.extend(pair)

    @property
    def rolls(self):
        return self._all_rolls

class DisadvantageDice(SimpleDice):
    def roll(self, num_dice=1):
        self._rolls = []
        self._all_rolls = []

        for i in range(num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls.append(min(pair))
            self._all_rolls.extend(pair)

    @property
    def rolls(self):
        return self._all_rolls
