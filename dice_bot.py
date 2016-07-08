import asyncio # Asynchronous I/O (from/to chat channel)

# Discord API (available at https://github.com/Rapptz/discord.py)
import discord
from discord.ext import commands

import re # regular expression support

from dice_tools import DiceRoller
from dice_tools.rollers.statistical import MaxRoller, MinRoller, AvgRoller

# RegEx patterns used in this script
patterns = {}

patterns["flag"] = r"\-\w+"

patterns["simple roll"] = r"((\d+d(\d+\-)?\d+(:\w+)?|\d+)\s*[\-\+]\s*)*\s*(\d+d(\d+\-)?\d+(:\w+)|\d+)"
patterns["flagged roll"] = r"({0}\s+)+\s*{1}".format(patterns["flag"], patterns["simple roll"])

# Create dice bot and register commands
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

def construct_message(roller, author, verbose=True):
    if verbose == False:
        message = "{0} rolled a total of `{1}`.".format(author.mention, roller.result)
    else:
        details = ' + '.join(roller.roll_detail_strings())
        message = "{0} rolled a total of `{1}` from `{2}`.".format(author.mention, roller.result, details)
    return message

# !roll command
@bot.command(pass_context=True, description='Rolls dice.')
async def roll(ctx, *, roll : str):
    """
    Rolls dice based on user messages.
    Reports result back to channel.

    Currently supports:
        (x1)d(y1) + (x2)d(y2) + ... + (xN)d(yN) + m1 + m2 + ... +  mN
        with the following dice-specific options applied as '(x)d(y):opt':
            advantage (adv, a)
            disadvantage (disadv, da, d)
            best (b, high, h)
            worst (w, low, l)
        and the following roll-global flags added as '-flagname'
        to the start of the whole roll:
            max
            min
            avg
    """
    author = ctx.message.author

    try:
        if re.match( patterns["flagged roll"], roll):
            # Find all flags
            flags = [ f[1:] for f in re.findall( patterns["flag"], roll) ]

            # Create a roller from just the dice spec
            roll = re.sub(r"\s*\-\w+\s*", "", roll)

            # Say something based on the flags found
            if "max" in flags:
                roller = MaxRoller(roll)
                await bot.say("{0}, `{2}` is the maximum possible result of `{1}`.".format(author.mention, roll, roller.result))
            elif "min" in flags:
                roller = MinRoller(roll)
                await bot.say("{0}, `{2}` is the minimum possible result of `{1}`.".format(author.mention, roll, roller.result))
            elif "avg" in flags:
                roller = AvgRoller(roll)
                await bot.say("{0}, `{2}` is (close to) the average result of `{1}`.".format(author.mention, roll, roller.result))
            else:
                await bot.say("{0} has provided an invalid flag.".format(author.mention, roll))
        elif re.match( patterns["simple roll"], roll ):
            # Handle a simple roll
            # 'XdY + ZdW + ... + M + N'
            roller = DiceRoller(roll)
            await bot.say( construct_message(roller, author) )
        else:
            await bot.say("{0}, you have specified an invalid roll. Please try again.".format(author.mention))
    except Exception as err:
        # If an exception is raised, have the bot say so in the channel
        await bot.say("{0} has specified an invalid roll producing `{1}`".format(author.mention, err))
        raise err

# Start the bot with the appropriate credentials
bot.run(login_email, password)
# bot.run('login_token')
