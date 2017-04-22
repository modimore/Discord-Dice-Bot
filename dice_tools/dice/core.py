'''
Representations of core dice types.
'''

from .base import DiceBase

class SimpleDice(DiceBase):
    ''' Simple dice, value is sum of all rolls. '''
    @property
    def value(self):
        ''' Return sum of all rolls, multipled by sign. '''
        return sum(self._rolls) * self._sign

    @property
    def avg(self):
        ''' Contstant-time average calculation.'''
        return self._num_dice * self._sign * (self._low + self._high)/2

class PickOneDice(DiceBase):
    '''
    Base class for dice groups that will only use a single dice roll from many.
    No value implementation. Must be specified in a derived class.
    '''

    @property
    def max(self):
        ''' Return the highest value possible on a single dice. '''
        return self._high if not self._negative else (-1 * self._low)

    @property
    def min(self):
        ''' Return the lowest value possible on a single dice. '''
        return self._low if not self._negative else (-1 * self._high)

class HighestRollDice(PickOneDice):
    ''' Dice group for which value is the highest roll. '''

    @property
    def value(self):
        ''' Return the highest value rolled. '''
        if self._negative:
            return min(self._rolls) * -1
        else:
            return max(self._rolls)

class LowestRollDice(PickOneDice):
    ''' Dice group for which value is the lowest roll. '''

    @property
    def value(self):
        ''' Return the lowest value rolled. '''
        if self._negative:
            return max(self._rolls) * -1
        else:
            return min(self._rolls)
