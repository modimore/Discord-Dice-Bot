from .simple import SimpleDice

class AdvantageDice(SimpleDice):
    def roll(self):
        self._rolls_kept = []
        self._all_rolls = []

        for i in range(self._num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls_kept.append(max(pair))
            self._all_rolls.extend(pair)

    @property
    def value(self):
        return sum(self._rolls_kept) * self._sign

    @property
    def rolls(self):
        return self._all_rolls

    @property
    def avg(self, num_samples=100000):
        total = sum(max(self.roll_die(), self.roll_die()) for i in range(num_samples))
        return self._num_dice * total / num_samples * self._sign

class DisadvantageDice(AdvantageDice):
    def roll(self):
        self._rolls_kept = []
        self._all_rolls = []

        for i in range(self._num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls_kept.append(min(pair))
            self._all_rolls.extend(pair)

    @property
    def avg(self, num_samples=100000):
        total = sum(min(self.roll_die(), self.roll_die()) for i in range(num_samples))
        return self._num_dice * total / num_samples * self._sign
