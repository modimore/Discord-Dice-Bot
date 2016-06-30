import asyncio # Asynchronous I/O (from/to chat channel)

# Discord API (available at https://github.com/Rapptz/discord.py)
import discord
from discord.ext import commands

import re # regular expression support

from dice_util import roll_total, roll_extreme

# A dice bot for use with Discord
bot = commands.Bot(command_prefix='!', description="A Discord chat bot for Tabletop RPG players.")

@bot.event
async def on_ready():
    print("Bot running as {0}({1})...".format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    print(message, message.server, message.author)
    print(message.content)

    try:
        await bot.process_commands(message)
    except Exception as err:
        print(err)

# Testing Commands
'''
@bot.command()
async def echo(*, message : str):
    await bot.say(message)

@bot.command()
async def add(*nums):
    """Adds an arbitrary number of integers together."""
    await bot.say(sum(map(int, nums)))

@bot.command()
async def repeat(times : int, *, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times): await bot.say(content)
'''

# !roll command
@bot.command(pass_context=True, description='Rolls dice.')
async def roll(ctx, *, roll : str):
    """
    Rolls dice based on user messages.
    Reports result back to channel.

    Currently supports:
        XdY + ZdW + ... + M + N
        -max/-min XdY + Z
    """
    author = ctx.message.author

    try:
        if re.match(r"((\d+d\d+|\d+)\s*[\-\+]+\s*)*\s*(\d+d\d+|\d+)", roll):
            # 'XdY + ZdW + ... + M + N'
            res = roll_total(roll)
            print("Bot result:", res)
            await bot.say("{0} rolled `{1}` from `{2}`".format(author.mention, res[0], roll))
        elif re.match(r"(-max |-min )+\s*(\d+d\d+)(\s*[\-\+]\d+)?", roll):
            # '-max XdY + Z', '-min XdY + Z'
            res = roll_extreme(re.sub(r"(-max|-min)\s+", "", roll), minimum=roll.find("-min") == 0)
            await bot.say("{0} rolled `{1}` from `{2}`".format(author.mention, res, roll))
        else:
            await bot.say("{0}, you have specified an invalid roll. Please try again.".format(author.mention))
    except Exception as err:
        await bot.say("{0} has specified an invalid roll producing {1}".format(author.mention, err))
        raise err

# Start the bot with the appropriate credentials
bot.run('sirmodimore+pythia@gmail.com', 'SnakeCity')
# bot.run('login_token')
