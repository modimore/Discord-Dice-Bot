# Discord-Dice-Bot
A dicebot for Discord made to support more complex rolls.

## Requirements
### Software Prerequisites
Discord-Dice-Bot is written for Python 3.5. Some minor changes can be made to make it 3.4-compatible.
It uses random, re, and asyncio from the Python standard library, and [discord.py].

[discord.py]: https://github.com/Rapptz/discord.py

After installing discord.py, just download the source files for this project and you should be good to go.

To change this script to work with Python 3.4,
replace `async def` with `@asyncio.corouting`
and `await` with `yield from`.

## Usage
### Running the Bot
This bot is currently designed to be run directly from *dice_bot.py* almost as provided.
Before you can use this you must supply a valid Discord login and password or bot token to a call to `bot.run` as follows:
```
bot.run(account_email, password)
```
or
```
bot.run(bot_token)
```
You and the bot cannot send messages at the same time, so you must have at least two separate Discord accounts
available to you to use this properly.

### Supported Commands
All commands issued to this bot must be prefaced with a *!*.

If you are downloading this script and running it yourself, you can change the command prefix character, but *!* is used in all examples here.

#### `!roll`
This is currently the only supported command. The command must be followed by a specification for what you are rolling, which is detailed in the [Dice Specification](#dice-specification-syntax) section.

Write your command to the bot as `!roll (spec)`. Here are some examples.

- `!roll 1d10 + 2d8 + 3`
- `!roll -avg 2d8 + 3`
- `!roll 1d20:adv + 4`

## Dice Specification Syntax
A dice specification can consists of any combination of valid groups of the same type of dice and constant value modifiers. Only integers are supported by this program.

#### Groups of Dice
A valid dice specification can take two forms.
The first, and more likely for you to use is `XdN`, as in `3d6`. The second is `XdM~N`. `XdN` should suggest rolling *X* *N*-sided dice, each producing a number from *1* to *N* inclusive, just like a physical dice would do. `XdM~N` is similar, but the lowest possible value will be *M* rather than *1*.

A few options can be added to individual dice rolls by adding `:opt` to the end of the dice.

- Choose the highest single value from the roll: `best`, `b`, `high`, `h`
- Choose the lowest single value from the roll: `worst`, `w`, `low`, `l`
- Roll with advantage \[D&D5E\] (roll in pairs and count the higher of each): `advantage`, `adv`, `a`
- Roll with disadvantage \[D&D5E\] (roll in pairs and count the lower of the two): `disadvantage`, `disadv`, `da`

As an example, rolling `4d10:best` with rolls of *2*, *4*, *6*, and *7* would get you a result of *7*. Rolling `2d20:adv` you could get *(1, 13)* and *(17, 14)*. You would take the best from each pair, dropping *1* and *12*, to end up with *17 + 13*.

#### Modifiers
Modifiers are simpler. A modifier is just an integer. `5`. You got it.

#### Bringing it all together
Combining groups of dice and modifiers is done just like adding numbers. `1d20 + 5` will result in *17* if you rolled a *12*.

You can also subtract modifiers, so if the specification above was `1d20 - 5` instead you would get a result of *7*. Dice groups cannot be subtracted, only added, but this may be changed in the future.

It is worth noting that in most cases, the spaces between dice groups and modifiers will not matter. `1d20 - 5 + 2d6` is functionally equivalent to `1d20-5+2d6` and `1d20- 5 +2d6`, but `1d 20 + 5 + 3 d6` will produce unexpected behaviour. The same goes for dice options. `1d20 :adv` and `1d20: adv` are not guaranteed to get you what you were looking for.

#### Global Flags
Global flags given at the start of your roll specification will change the type of output you get. The format for this is `-flag`.

The currently supported flags are:
- Get the maximum possible result of the specified roll: `max`
- Get the minimum possible result of the specified roll: `min`
- Get (something close to) the average result of the specified roll: `avg`

`!roll -avg 1d20` will give you a result of `10.5`. Roll options and flags can be combined also. `!roll -avg 1d20:adv` will give you a result around `13.8`.
