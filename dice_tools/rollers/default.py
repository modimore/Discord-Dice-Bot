'''
Default dice roller class implementation.
'''

# Regular Expressions for input validation and parsing
import re

# Import dice classes
from ..dice import SimpleDice, HighestRollDice, LowestRollDice, Modifier
from ..dice.dnd_5e import AdvantageDice, DisadvantageDice

# Import dice errors
from ..exceptions import DiceToolsError, InvalidDiceSpecError, InvalidDiceOptionError

# Class to manage all dice rolls
# Serves both as a factory for dice and a reporting agent for results
class DiceRoller:
    ''' A class that parses and executes dice rolls. '''
    # Initialization Functions =================================================
    @staticmethod
    def parse_spec(spec):
        ''' Roll specification parsing function '''

        # RegEx Patterns used in this parser
        patterns = {}

        patterns["dice"] = r"(?:(?P<num_dice>\d+)d(?:(?P<min_val>\d+)~)?(?P<max_val>\d+)(?:\:(?P<option>\w+))?)"
        patterns["mod"]  = r"(?P<mod_val>\d+)"

        patterns["match_unit"] = r"((?P<sign>\-)?\s*({0}))\b".format('|'.join( [patterns["dice"], patterns["mod"]] ))

        # Parse out all dice rolls and range rolls
        results = []

        # Iterate through all parsable results
        for match in re.finditer(patterns["match_unit"], spec):
            try:
                # Get the dictionary with the keyword matches
                groups = match.groupdict()
                # All missing match groups will have a value of None

                # Check the possible match patterns
                if groups["mod_val"] is not None:
                    # The match is a modifier
                    results.append( Modifier( int(match.expand("\g<1>").replace(" ", "")) ) )
                elif groups["num_dice"] is not None:
                    # The match is a dice roll
                    if groups["option"] is None:
                        results.append( SimpleDice(
                                                   face_max=int(groups["max_val"]),
                                                   face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                   num_dice=int(groups["num_dice"]),
                                                   negative=groups["sign"] is not None
                                                  ))
                    elif groups["option"] in ["best", "b", "high", "h"]:
                        results.append( HighestRollDice(
                                                        face_max=int(groups["max_val"]),
                                                        face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                        num_dice=int(groups["num_dice"]),
                                                        negative=groups["sign"] is not None
                                                       ))
                    elif groups["option"] in ["worst", "w", "low", "l"]:
                        results.append( LowestRollDice(
                                                       face_max=int(groups["max_val"]),
                                                       face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                       num_dice=int(groups["num_dice"]),
                                                       negative=groups["sign"] is not None
                                                      ))
                    elif groups["option"] in ["advantage", "adv", "a"]:
                        results.append( AdvantageDice(
                                                      face_max=int(groups["max_val"]),
                                                      face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                      num_dice=int(groups["num_dice"]),
                                                      negative=groups["sign"] is not None
                                                     ))
                    elif groups["option"] in ["disadvantage", "disadv", "dis", "da", "d"]:
                        results.append( DisadvantageDice(
                                                         face_max=int(groups["max_val"]),
                                                         face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                         num_dice=int(groups["num_dice"]),
                                                         negative=groups["sign"] is not None
                                                        ))
                    else:
                        raise InvalidDiceOptionError(groups["option"])
                else:
                    raise DiceToolsError()
            except DiceToolsError:
                raise InvalidDiceSpecError(match.expand("\g<1>"))

        return results

    # DiceRoller Constructor
    def __init__(self, spec):
        self._rolls = self.parse_spec(spec)
        for roll in self._rolls:
            roll.roll()
    # ==========================================================================

    # Intended accessors to roll results =======================================
    @property
    def result(self):
        ''' Return sum of the values of all rolls. '''
        return sum(res.value for res in self._rolls)

    @property
    def details(self):
        ''' Return list of individual rolled values for each roll. '''
        return [ res.rolls for res in self._rolls ]

    def roll_detail_strings(self):
        ''' Return list of string conversions of rolls. '''
        return [ str(roll) for roll in self._rolls ]
    # ==========================================================================
