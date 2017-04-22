'''
Representations of dice types for use with 5th Edition D&D.
Provides functionality for rolling with advantage and disadvantage.
'''

from .base import DiceBase

class AdvantageDice(DiceBase):
    ''' Dice for rolling with Advantage in D&D 5E. '''
    '''
    Here advantage means for each die,
    roll twice and take the higher value.
    '''

    def roll(self):
        '''
        Roll with advantage.
        Keep track of both the rolls kept and all rolls separately.
        '''
        self._rolls_kept = []
        self._all_rolls = []

        for i in range(self._num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls_kept.append(max(pair))
            self._all_rolls.extend(pair)

    @property
    def value(self):
        ''' Return the sum of only the rolls kept. '''
        return sum(self._rolls_kept) * self._sign

    @property
    def rolls(self):
        ''' Return a list of every value rolled, both kept and discarded. '''
        return self._all_rolls

class DisadvantageDice(AdvantageDice):
    def roll(self):
        '''
        Roll with disadvantage.
        Keep track of rolls kept and all rolls separetely.
        '''
        self._rolls_kept = []
        self._all_rolls = []

        for i in range(self._num_dice):
            pair = ( self.roll_die(), self.roll_die() )
            self._rolls_kept.append(min(pair))
            self._all_rolls.extend(pair)
