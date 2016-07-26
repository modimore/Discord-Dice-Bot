# Running your own instance
This file contains instruction for running your own instance of the bot.

## Environment
### Python Version
Discord-Dice-Bot is written for Python 3.5.

Some minor changes can be made to make it 3.4-compatible.

### Packages
The only packages that you need to install to run this is [discord.py] and its dependencies, listed in *[requirements.txt]*.

[discord.py] is available via PyPI and can be installed using `pip install discord.py` or an equivalent command.

[discord.py]: https://github.com/Rapptz/discord.py
[requirements.txt]: https://github.com/modimore/Discord-Dice-Bot/blob/master/requirements.txt

To change this script to work with Python 3.4,
replace `async def` with `@asyncio.corouting`
and `await` with `yield from`.

## Running the bot
This bot is currently designed to be run directly from *dice_bot.py* almost as provided. There is however, one change that you will need to make to the last last line of the script.
Before you can use this you must supply a valid Discord login and password or bot token to a call to `bot.run` as follows:
```
bot.run(account_email, password)
```
or
```
bot.run(bot_token)
```
You and the bot cannot send messages at the same time on the same account, so you must have at least two separate Discord accounts
available to you to use this properly.
