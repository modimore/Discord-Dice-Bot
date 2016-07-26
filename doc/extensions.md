# Writing Extensions
There are two major types of extensions you can write for this program, extra [dice types][] and extra [rollers][].

[dice types]: [#dice-types]
[rollers]: [#rollers]

## Dice Types
In order to make a dice type that is fully compliant with this program, your class has have these properties: `value`, `max`, `min`, `avg`, `rolls`

and one method, `roll`, which is called by the roller class.

Defaults for everything except `value` are included in the `DiceBase` class in [base.py][base.py].

[base.py]: https://github.com/modimore/Discord-Dice-Bot/blob/master/dice_tools/dice/base.py

If you write a new dice type, make sure to add it to the default roller so that it can be used.

### Properties
The required properties for a dice type are described below.

- `value`: a randomly determined result for a roll of this type, integer
- `max`: the highest possible roll value, integer
- `min`: the lowest possible roll value, integer
- `avg`: the average value of a roll (or hopefully close to it), real number
- `rolls`: raw rolls from this dice, tuple of integers

All of these are expected by the roller classes, and must return a result of the type listed.

Currently implemented dice classes have these as methods with an `@property` decorator. This is the suggested pattern for dice types.

### Methods
The only required method, `roll`, is intended used to generate random results and assign them to a private variable for the later use of the object that rolled the results.

You do not actually have to do this here, but it is suggested that you do. This is not done in a classes `__init__` method so accessing a constant value (such as the maximum possible value of many dice) can happen constant time.

### Additional Properties and Methods
Besides those listed above, properties and methods exist on a case-by-case basis. Additional methods and classes can be made to help the implementation of your dice type, but will not be accessed by any roller.

One possible exception to this is the `get_spec` method. Only `DiceBase` has an implementation right now, and it is only used in the `__str__` method for that class. It is designed to recreate the dice specification string used to create the dice. Not having it should not crash the program or raise an error.

## Rollers
Rollers parse dice specifications and summarize results. To write a roller you just have to overwrite one method: `result`. Result should be defined with an `@property` decorator and be calculated using dice properties listed above.
