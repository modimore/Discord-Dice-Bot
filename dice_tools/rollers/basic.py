# Regular Expressions for input validation and parsing
import re

# BasicDice class to handle rolling
from ..dice.basic import SimpleDice, HighestRollDice, LowestRollDice
from ..dice.dnd_5e import AdvantageDice, DisadvantageDice
from ..dice.modifier import Modifier

# Class to manage and report results of all dice rolls
class BasicRoller:
    # Roll specification parsing function
    @staticmethod
    def parse_spec(spec):
        # Parse out all dice rolls and range rolls
        results = []

        # Iterate through all parsable results
        for match in re.finditer(r"\b(?P<num_dice>\d+)d(?:(?P<min_val>\d+)\-)?(?P<max_val>\d+)(?:\:(?P<option>\w+))?|(?P<mod>[\+\-]?\s*\d+)\b", spec):
            # Get the dictionary with the keyword matches
            groups = match.groupdict()
            # All missing match groups will have a value of None

            # Check the possible match patterns
            if groups["mod"] is not None:
                # The match is a modifier
                results.append( Modifier( int(groups["mod"].replace(" ", "")) ) )
            elif groups["num_dice"] is not None:
                # The match is a dice roll
                if groups["option"] in ["best", "b", "high", "h"]:
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
                elif groups["option"] in ["disadvantage", "disadv", "da", "d"]:
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
        self.results = self.parse_spec(spec)

    # Report sum of all rolls
    def sum_all_rolls(self):
        return sum(res.value for res in self.results)

    # Return all individual rolls from a dice
    def roll_details(self):
        return [ res.rolls for res in self.results ]

    def roll_detail_strings(self):
        return [ "({})".format( ', '.join(str(x) for x in vals)) for vals in self.roll_details() ]

    # Get maximum roll from all rolls
    def max_all_rolls(self):
        return sum(res.highest for res in self.results)

    # Get minimum roll from all rolls
    def min_all_rolls(self):
        return sum(res.lowest for res in self.results)
