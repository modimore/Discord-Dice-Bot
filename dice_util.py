# RNG for roll results
from random import randint
# Regular Expressions for input validation and parsing
import re

class DiceGroup:
    def __init__(self, face_max, face_min=1):
        # Set high and low face values
        self.face_max = face_max
        self.face_min = face_min

        # Explicitly nullify roll cache

    # Driving roll function
    def roll(self, num_times=1):
        # Roll dice of correct type of times specified
        self.roll_cache = [randint(self.face_min, self.face_max) for i in range(num_times)]
        print("Roll Cache:", self.roll_cache)
        self.total = sum(self.roll_cache)
        print("Roll Total:", self.total)

    # Roll History Accessors
    def get_last_rollspec(self):
        # return last rolls made in XdY format
        if not self.roll_cache:
            return "No roll made."
        elif self.face_min != 1:
            return "{0}d{1}".format(len(self.roll_cache), self.face_max)
        else:
            return "{0}d{1}-{2}".format(len(self.roll_cache), self.face_min, self.face_max)

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
        return "<DiceGroup [{}-{}] Last Roll: {} ({})>".format(self.face_min, self.face_max, self.result, ', '.join(self.roll_cache))

def parse_roll(roll_str):
    rolls_out = []
    mods_out = []

    for r in re.findall(r"\b(\d+)d(\d+)\b", roll_str):
        rolls_out.append( (int(r[0]), int(r[1])) )

    for r in re.findall(r"\b(\-|\+|)\s*(\d+)\b", roll_str):
        if r[0] != "-":
            mods_out.append(int(r[1]))
        else:
            mods_out.append(-1*int(r[1]))

    return rolls_out, mods_out

def roll_total(roll_str):
    try:
        dice_rolls, mods = parse_roll(roll_str)
    except Exception as err:
        print(err)
        return 0, []

    details = []
    total = 0

    for roll in dice_rolls:
        dice = DiceGroup(roll[1])
        dice.roll(roll[0])
        total += dice.get_roll_total()
        details.append(dice.get_roll_cache())

    total += sum(mods)
    details.extend(mods)

    return total, details

def roll_extreme(roll_str, minimum=False):
    # Sum up the total modifier
    mod = 0
    for m in re.findall(r"\b(\-|\+|)\s*(\d+)\b", roll_str):
        mod += int(m.replace(" ", ""))

    # Create the dice specified in the roll string
    rolls = re.search(r"(\d+)d(\d+)", roll_str)
    num_dice, dice_max = [int(s) for s in rolls.groups()]
    dice = DiceGroup(dice_max)

    dice.roll(num_dice)
    if minimum == True:
        return dice.get_lowest_roll() + mod
    else:
        return dice.get_highest_roll() + mod

# Main section for testing
if __name__ == '__main__':
    from sys import argv
    from collections import defaultdict

    def is_int(s):
        try:
            int(s)
            return int(s) == s
        except:
            return False

    def dice_test(roll : str):
        if re.fullmatch(r"((\d+d\d+|\d+)\s*[\-\+]\s*)*\s*(\d+d\d+|\d+)", roll) != None:
            res = roll_total(roll)
            print(res[0], res[1])
        elif re.fullmatch(r"(-max |-min )\s*(\d+d\d+)\s*([\-\+]\s*\d+)?", roll) != None:
            res = roll_extreme( re.sub(r"(-max|-min)\s*", "", roll), minimum=roll.find("-min ") == 0)
            print(res)
        else:
            print("Invalid Roll")

    try:
        print(argv)
        for i in range(100):
            dice_test(' '.join(argv[1:]))

    except Exception as err:
        print(err)
