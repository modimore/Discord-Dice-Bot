# Discord-Dice-Bot
A dicebot for Discord made to support more complex rolls.

## Requirements
### Software Prerequisites
Discord-Dice-Bot is written for Python 3.5. Some minor changes can be made to make it 3.4-compatible.
It uses random, re, and asyncio from the Python standard library, and [discord.py].

[discord.py]: https://github.com/Rapptz/discord.py

After installing discord.py, just download the source files for this project and you should be good to go.

To change this script to work with Python 3.4, replace `async def` with 
```
@asyncio.corouting
```
and `await` with `yield from`.

## Usage
### Running the Bot
This bot is currently designed to be run directly from *dice_bot.py* almost as provided.
Before you can use this you must supply a valid Discord login and password or bot token to a call to `bot.run` as follows:
```
bot.run(login_email, password)
```
or
```
bot.run(bot_token)
```
You and the bot cannot send messages at the same time, so you must have at least two separate Discord accounts
available to you to use this properly.

### Supported Commands
All commands issued to this bot must be prefaced with a *!*.

The only currently supported command is `!roll`, which has two use cases.

`!roll (x1)d(y1) + (x2)d(y2) + ... + (xN)d(yN) + (m1) + ... + (mN)` will roll all dice and modifiers and report the total.

`!roll max (x)d(y) + z` will choose the largest d(y) result and add z to it. `!roll min (x)d(y) + (z)` chooses the smallest.
