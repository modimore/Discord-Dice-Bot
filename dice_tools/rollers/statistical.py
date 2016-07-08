from .default import DiceRoller

class StatRoller(DiceRoller):
    def __init__(self, spec):
        self._rolls = self.parse_spec(spec)

    @property
    def result(self):
        pass

class MaxRoller(StatRoller):
    @property
    def result(self):
        return sum(roll.max for roll in self._rolls)

class MinRoller(StatRoller):
    @property
    def result(self):
        return sum(roll.min for roll in self._rolls)

class AvgRoller(StatRoller):
    @property
    def result(self):
        return sum(roll.avg for roll in self._rolls)
