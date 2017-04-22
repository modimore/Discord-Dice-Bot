'''
Base classes for all dice types.
DiceBase and Modifier classes are defined here.
'''

from ..exceptions import DiceToolsError, NotRolledError

# RNG for roll results
from random import randint

class DiceBase(object):
    '''
    Base dice class.
    Implements the most likely to be used version of some common functions.
    '''
    def __init__(self, face_max, face_min=1, num_dice=1, negative=False):
        # Set high and low face values
        self._low = face_min if face_min is not None else 1
        self._high = face_max
        # Set number of dice in pool
        self._num_dice = num_dice
        # Set whether result is to be subtracted
        self._negative = negative

        if self._low > self._high or self._num_dice < 0:
            raise DiceToolsError()

    def roll_die(self):
        ''' Roll a single die. '''
        return randint(self._low, self._high)

    def roll(self):
        ''' Roll the specified number of dice. '''
        self._rolls = [self.roll_die() for i in range(self._num_dice)]

    def get_spec(self):
        ''' Recreate the specification that created these dice.. '''
        if self._low == 1:
            return "{0}d{1}".format(self._num_dice, self._high)
        else:
            return "{0}d{1}~{2}".format(self._num_dice, self._low, self._high)

    # Intended accessor functions
    @property
    def value(self):
        '''
        Accessor for the result of the dice rolled.
        Not implemented here, as each derived class should have a unique version of this.
        '''
        pass

    @property
    def _sign(self):
        ''' Internal method to get the sign of the result. '''
        return -1 if self._negative else 1

    @property
    def rolls(self):
        ''' Return the entire roll cache as a tuple. '''
        try:
            return tuple(self._rolls)
        except:
            raise NotRolledError(self)

    @property
    def max(self):
        ''' Return maximum possible value from rolling this group. '''
        if not self._negative:
            return self._num_dice * self._high
        else:
            return self._num_dice * self._low * -1

    @property
    def min(self):
        ''' Return minimum possible value from rolling this group. '''
        if not self._negative:
            return self._num_dice * self._low
        else:
            return self._num_dice * self._high * -1

    @property
    def avg(self, num_samples=10000):
        ''' Returns an good estimate of the average roll of these dice. '''
        '''
        Actually rolls many times to do so, calculating average from results.
        Override with more efficient versions where possible.
        '''

        total = 0
        for i in range(num_samples):
            self.roll()
            total += self.value
        return total / num_samples

    def __str__(self):
        try:
            return "({0})".format(', '.join(str(x) for x in self.rolls))
        except NotRolledError:
            raise DiceToolsError(self.get_spec())

class Modifier(object):
    '''
    Integer modifier to a dice roll.
    Provides the same interface as a dice type for program compatability.
    '''
    def __init__(self, value):
        self._val = value

    def roll(self):
        pass

    @property
    def value(self):
        return self._val

    @property
    def rolls(self):
        return (self._val,)

    @property
    def max(self):
        return self._val

    @property
    def min(self):
        return self._val

    @property
    def avg(self):
        return self._val

    def __str__(self):
        return str(self._val)
