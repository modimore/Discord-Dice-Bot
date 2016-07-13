# Roll Specification Syntax
A dice specification can consists of any combination of valid groups of the same type of dice and constant value modifiers. Only integers are supported by this program.

## Groups of Dice
A valid dice specification can take two forms.

The first, and more likely for you to use is `XdN`, as in `3d6`. `XdN` should suggest rolling *X* *N*-sided dice, each producing a number from *1* to *N* inclusive, just like a physical dice would do.

The second is `XdM~N`. `XdM~N` is similar to `XdN`, but the lowest possible value will be *M* rather than *1*.

### Options
A few options can be added to individual dice rolls by adding `:(opt)` to the end of the dice.

- `best`, `b`, `high`, `h`: Choose the highest single value from the roll
- `worst`, `w`, `low`, `l`: Choose the lowest single value from the roll
- `advantage`, `adv`, `a`: \[D&D5E\] Roll with advantage (roll in pairs and count the higher of each)
- `disadvantage`, `disadv`, `da`: \[D&D5E\] Roll with disadvantage (roll in pairs and count the lower of the two)

Rolling `4d10:best` with rolls of *2*, *4*, *6*, and *7* would get you a result of *7*.

Rolling `2d20:adv` you could get *(1, 13)* and *(17, 14)*. You would take the best from each pair, dropping *1* and *12*, to end up with *17 + 13*.

## Modifiers
Modifiers are simpler. A modifier is just an integer. `5`. You got it.

## Bringing it all together
Combining groups of dice and modifiers is done just like adding numbers. `1d20 + 5` will result in *17* if you rolled a *12*. Just to make the rest of these examples easier let's assume you always roll *12* on a d20 in this section.

You can also subtract things, so if the specification above was `1d20 - 5` instead you would get a result of *7*. If it was `5 - 1d20` we would end up with *-7*.

It is worth noting that in most cases, the spaces between dice groups and modifiers will not matter. `1d20 - 5 + 2d6` is functionally equivalent to `1d20-5+2d6` and `1d20- 5 +2d6`, but `1d 20 + 5 + 3 d6` will produce unexpected behaviour. The same goes for dice options. `1d20 :adv` and `1d20: adv` are not guaranteed to get you what you were looking for.

## Global Flags
Global flags given at the start of your roll specification will change the type of output you get. The format for this is `-(flag)`.

The currently supported flags are:
- `max`: Get the maximum possible result of the specified roll
- `min`: Get the minimum possible result of the specified roll
- `avg`: Get (something close to) the average result of the specified roll

`-avg 1d20` will give you a result of `10.5`. Roll options and flags can be combined also. `!roll -avg 1d20:adv` will give you a result around `13.8`.
