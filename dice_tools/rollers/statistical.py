'''
Dice rollers that calculate statistical values rather than random roll results.
'''

from . import DiceRoller

class StatRoller(DiceRoller):
    ''' Base statistical roller. Does not provide a result. '''
    def __init__(self, spec):
        ''' Initialization function that does not roll dice after parsing. '''
        self._rolls = self.parse_spec(spec)

    @property
    def result(self):
        ''' Not implemented, see derived classes. '''
        pass

class MaxRoller(StatRoller):
    @property
    def result(self):
        ''' Return sum of maximum possible values of rolls. '''
        return sum(roll.max for roll in self._rolls)

class MinRoller(StatRoller):
    @property
    def result(self):
        ''' Return sum of minimum possible value of rolls. '''
        return sum(roll.min for roll in self._rolls)

class AvgRoller(StatRoller):
    @property
    def result(self):
        ''' Return sum of average of rolls. '''
        return sum(roll.avg for roll in self._rolls)
