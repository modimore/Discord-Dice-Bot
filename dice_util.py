# RNG for roll results
from random import randint
# Regular Expressions for input validation and parsing
import re

class DiceSet:
    def __init__(self, face_max, face_min=1):
        self.face_max=face_max
        self.face_min=face_min
        self.roll_cache = []
        self.result = 0

    def roll(self, num_times=1):
        self.result = 0
        self.roll_cache.clear()

        for i in range(num_times):
            last_roll = randint(self.face_min,self.face_max)
            self.result += last_roll
            self.roll_cache.append(last_roll)

        return self.result

    def get_roll_cache(self):
        return tuple(self.roll_cache)

    def __repr__(self):
        return "<DiceSet [{}-{}] Last Roll: {}, {}>".format(self.face_min, self.face_max, self.result, self.roll_cache)

def roll_single(dice_max,dice_min=1):
    if dice_max < dice_min:
        raise Exception('Error: invalid dice specificed')
    return randint(dice_min,dice_max)

def roll_many(num_dice,dice_max,dice_min=1):
    if dice_max < dice_min:
        raise Exception('Error: invalid dice specified')

    results = []
    for i in range(num_dice):
        results.append(randint(dice_min,dice_max))
    return sum(results), tuple(results)

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
        dice = DiceSet(roll[1])
        total += dice.roll(roll[0])
        details.append(dice.get_roll_cache())

    total += sum(mods)
    details.extend(mods)

    return total, details

def roll_extreme(roll_str, minimum=False):
    print(roll_str)
    rolls = re.search(r"(\d+)d(\d+)", roll_str)
    num_dice, dice_max = [int(s) for s in rolls.groups()]

    mod = 0
    for m in re.findall(r"\b(\-|\+|)\s*(\d+)\b", roll_str):
        print(m)
        mod += int(m.replace(" ", ""))

    if minimum == True:
        return min([ roll_single(dice_max) for i in range(num_dice) ]) + mod
    else:
        return max([ roll_single(dice_max) for i in range(num_dice) ]) + mod

if __name__ == '__main__':
    from sys import argv

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
        elif re.fullmatch(r"(max|min)\s*(\d+d\d+)\s*([\-\+]\s*\d+)?", roll) != None:
            res = roll_extreme( re.sub(r"(max|min)\s*", "", roll), minimum=roll.find("min ") == 0)
            print(res)
        else:
            print("Invalid Roll")

    try:
        print(argv)
        dice_test(' '.join(argv[1:]))
    except Exception as err:
        print(err)
