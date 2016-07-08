# Regular Expressions for input validation and parsing
import re

# Import dice classes
from ..dice.basic import SimpleDice, HighestRollDice, LowestRollDice
from ..dice.dnd_5e import AdvantageDice, DisadvantageDice
from ..dice.modifier import Modifier

# Class to manage all dice rolls
# Serves both as a factory for dice and a reporting agent for results
class DiceRoller:
    # Initialization Functions =================================================
    # Roll specification parsing function
    @staticmethod
    def parse_spec(spec):
        # RegEx Patterns used in this parser
        patterns = {}

        patterns["dice"] = r"(?P<num_dice>\d+)d(?:(?P<min_val>\d+)~)?(?P<max_val>\d+)(?:\:(?P<option>\w+))?"
        patterns["mod"]  = r"(?P<mod>[\+\-]?\s*\d+)"

        patterns["match_unit"] = r"\b{0}\b".format('|'.join( [patterns["dice"], patterns["mod"]] ))

        # Parse out all dice rolls and range rolls
        results = []

        # Iterate through all parsable results
        for match in re.finditer(patterns["match_unit"], spec):
            # Get the dictionary with the keyword matches
            groups = match.groupdict()
            # All missing match groups will have a value of None

            # Check the possible match patterns
            if groups["mod"] is not None:
                # The match is a modifier
                results.append( Modifier( int(groups["mod"].replace(" ", "")) ) )
            elif groups["num_dice"] is not None:
                # The match is a dice roll
                if groups["option"] is None:
                    results.append( SimpleDice(
                                               face_max=int(groups["max_val"]),
                                               face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                               num_dice=int(groups["num_dice"])
                                              ))
                elif groups["option"] in ["best", "b", "high", "h"]:
                    results.append( HighestRollDice(
                                                    face_max=int(groups["max_val"]),
                                                    face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                    num_dice=int(groups["num_dice"])
                                                   ))
                elif groups["option"] in ["worst", "w", "low", "l"]:
                    results.append( LowestRollDice(
                                                   face_max=int(groups["max_val"]),
                                                   face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                   num_dice=int(groups["num_dice"])
                                                  ))
                elif groups["option"] in ["advantage", "adv", "a"]:
                    results.append( AdvantageDice(
                                                  face_max=int(groups["max_val"]),
                                                  face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                  num_dice=int(groups["num_dice"])
                                                 ))
                elif groups["option"] in ["disadvantage", "disadv", "dis", "da", "d"]:
                    results.append( DisadvantageDice(
                                                     face_max=int(groups["max_val"]),
                                                     face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                                     num_dice=int(groups["num_dice"])
                                                    ))
                else:
                    results.append( SimpleDice(
                                               face_max=int(groups["max_val"]),
                                               face_min=int(groups["min_val"]) if groups["min_val"] is not None else None,
                                               num_dice=int(groups["num_dice"])
                                              ))

        return results

    # DiceRoller Constructor
    def __init__(self, spec):
        self._rolls = self.parse_spec(spec)
        for roll in self._rolls:
            roll.roll()
    # ==========================================================================

    # Report sum of all rolls
    def sum_all_rolls(self):
        return sum(res.value for res in self._rolls)

    # Return all individual rolls from a dice
    def roll_details(self):
        return [ res.rolls for res in self._rolls ]

    def roll_detail_strings(self):
        return [ "({})".format( ', '.join(str(x) for x in vals)) for vals in self.roll_details() ]

    # Intended accessors to roll results =======================================
    @property
    def result(self):
        return sum(res.value for res in self._rolls)
    # ==========================================================================
