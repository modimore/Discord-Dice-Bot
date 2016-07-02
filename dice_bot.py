import asyncio # Asynchronous I/O (from/to chat channel)

# Discord API (available at https://github.com/Rapptz/discord.py)
import discord
from discord.ext import commands

import re # regular expression support

from dice_tools import BasicRoller

patterns = {
    "simple roll": r"((\d+d\d+|\d+)\s*[\-\+]\s*)*\s*(\d+d\d+|\d+)",
    "flagged roll": r"(\-\w+\s+)+\s*((\d+d\d+|\d+)\s*[\-\+]\s*)*\s*(\d+d\d+|\d+)",
    "flag": r"\-\w+"
}

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
        (x1)d(y1) + (x2)d(y2) + ... + (xN)d(yN) + m1 + m2 + ... +  mN
        -max/-min (x1)d(y1) + ... + (xN)d(yN) + m1 + ... +  mN
    """
    author = ctx.message.author

    try:
        if re.match( patterns["simple roll"], roll ):
            # Handle a simple roll
            # 'XdY + ZdW + ... + M + N'
            roller = BasicRoller(roll)
            details = ' + '.join(roller.roll_detail_string())
            await bot.say( "{0} rolled a total of `{1}` from `{2}`".format(author.mention, roller.sum_all_rolls(), details) )

        elif re.match( patterns["flagged roll"], roll ):
            # Handle a roll with flags
            # '-max XdY + Z', '-min XdY + Z'

            # Find all flags
            flags = [ f[1:] for f in re.findall( patterns["flag"], roll) ]

            # Create a roller from just the dice spec
            roller = BasicRoller(re.sub(r"\s*\-\w+\s*", "", roll))

            # Say something based on the flags found
            if "max" in flags:
                await bot.say("{0} rolled `{1}` from `{2}`".format(author.mention, roller.max_all_rolls(), roll))
            elif "min" in flags:
                await bot.say("{0} rolled `{1}` from `{2}`".format(author.mention, roller.min_all_rolls(), roll))
            else:
                await bot.say("{0} has provided an invalid flag in `{1}`".format(author.mention, roll))

        else:
            await bot.say("{0}, you have specified an invalid roll. Please try again.".format(author.mention))
    except Exception as err:
        # If an exception is raised, have the bot say so in the channel
        await bot.say("{0} has specified an invalid roll producing `{1}`".format(author.mention, err))
        raise err

# Start the bot with the appropriate credentials
# bot.run(login_email, login_password)
# bot.run('login_token')
