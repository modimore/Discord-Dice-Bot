from dice_tools import DiceRoller

while True:
    roll = input()

    roller = DiceRoller(roll)
    print(roller.sum_all_rolls())
    print(roller.roll_detail_strings())
