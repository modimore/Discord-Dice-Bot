# RNG for roll results
from random import randint
# Regular Expressions for input validation and parsing
import re

# Dice class to implement rolling functionality
class BasicDice:
    def __init__(self, face_max, face_min=1, num_dice=0):
        # Set high and low face values
        self.high_val = face_max
        self.low_val = face_min

        if num_dice != 0:
            self.roll(num_dice)

    # Driving roll function
    def roll(self, num_dice=1):
        # Roll dice of correct type of times specified
        self.roll_cache = [randint(self.low_val, self.high_val) for i in range(num_dice)]
        # print("Roll Cache:", self.roll_cache)
        self.total = sum(self.roll_cache)
        # print("Roll Total:", self.total)

    # Roll History Accessors
    def get_last_rollspec(self):
        # return last rolls made in XdY format
        if not self.roll_cache:
            return "No roll made."
        elif self.low_val != 1:
            return "{0}d{1}".format(len(self.roll_cache), self.high_val)
        else:
            return "{0}d{1}-{2}".format(len(self.roll_cache), self.low_val, self.high_val)

    def get_roll_total(self):
        # Return the integer value of the runnning total of rolls
        return self.total

    def get_roll_cache(self):
        # Return the entire roll cache as a tuple
        return tuple(self.roll_cache)

    def get_highest_roll(self):
        # Get the highest roll from the roll cache
        return max(self.roll_cache)

    def get_lowest_roll(self):
        # Get the lowest roll from the roll cache
        return min(self.roll_cache)

    def __repr__(self):
        return "<BasicDice [{}-{}] Last Roll: {} ({})>".format(self.low_val, self.high_val, self.result, ', '.join(self.roll_cache))

# Class to manage and report results of all dice rolls
class DiceRoller:
    # Roll specification parsing function
    @staticmethod
    def parse_spec(spec):
        # Parse out all dice rolls and range rolls
        dice_results = []

        for dice in re.finditer(r"\b(\d+)d(\d+)\b", spec):
            num_dice, max_val = [ int(x) for x in dice.groups() ]
            dice_results.append(BasicDice(face_max=max_val, num_dice=num_dice))

        for dice in re.finditer(r"\b(\d+)d(\d+)-(\d+)\b", spec):
            num_dice, min_val, max_val = [ int(x) for x in dice.groups() ]
            dice_results.append(BasicDice(face_min=min_val, face_max=max_val, num_dice=num_dice))

        # Parse out all modifiers
        mods = []
        for mod in re.findall(r"\b[\+\-]?\s*\d+\b", spec):
            mods.append(int(mod))

        return dice_results, mods

    # DiceRoller Constructor
    def __init__(self, spec):
        self.dice_results, self.mods = self.parse_spec(spec)

    # Report sum of all rolls
    def sum_all_rolls(self):
        result = 0

        for res in self.dice_results:
            result += res.get_roll_total()

        result += sum(self.mods)
        return result

    # Return all individual rolls from a dice
    def roll_details(self):
        details = []
        for res in self.dice_results:
            details.append(res.get_roll_cache())
        return details

    # Get maximum roll from all rolls
    def max_all_rolls(self):
        max_all = 0

        for res in self.dice_results:
            max_all += res.get_highest_roll()

        max_all += sum(self.mods)
        return max_all

    # Get minimum roll from all rolls
    def min_all_rolls(self):
        min_all = 0

        for res in self.dice_results:
            min_all += res.get_lowest_roll()

        min_all += sum(self.mods)
        return min_all

# Main section for testing
if __name__ == '__main__':
    from sys import argv
    # from collections import defaultdict
    #
    # def is_int(s):
    #     try:
    #         int(s)
    #         return int(s) == s
    #     except:
    #         return False

    roll = ' '.join(argv[1:])

    if re.fullmatch(r"((\d+d\d+|\d+)\s*[\-\+]\s*)*\s*(\d+d\d+|\d+)", roll) != None:
        dr = DiceRoller(roll)
        print(dr.sum_all_rolls())
    elif re.fullmatch(r"(-max |-min )\s*(\d+d\d+)\s*([\-\+]\s*\d+)?", roll) != None:
        dr = DiceRoller( re.sub(r"(-max|-min)\s*", "", roll) )
        if roll.find("-min ") == 0:
            print(dr.min_all_rolls())
        else:
            print(dr.max_all_rolls())
    else:
        print("Invalid Roll")
