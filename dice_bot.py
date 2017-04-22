import asyncio # Asynchronous I/O (from/to chat channel)

# Discord API (available at https://github.com/Rapptz/discord.py)
import discord
from discord.ext import commands

import re # regular expression support

from dice_tools.rollers import DiceRoller
from dice_tools.rollers.statistical import MaxRoller, MinRoller, AvgRoller

from dice_tools.exceptions import DiceToolsError

# RegEx patterns used in this script
patterns = {}

patterns["flag"] = r"\-[^\W\d]+"

patterns["sign"] = r"[\+\-]"
patterns["dice"] = r"\d+d(\d+~)?\d+(:\w+)?"
patterns["mod"]  = r"\d+"

patterns["single roll"] = r"{0}?\s*({1}|{2})\b".format(patterns["sign"], patterns["dice"], patterns["mod"])

patterns["simple roll"] = r"({0})+".format(patterns["single roll"])
patterns["flagged roll"] = r"({0}\s+)+\s*{1}".format(patterns["flag"], patterns["simple roll"])

# Create dice bot and register commands
bot = commands.Bot(command_prefix='!', description="A Discord chat bot for Tabletop RPG players.")

@bot.event
async def on_ready():
    """The callback invoked when login and connection succeed."""
    print("Bot running as {0}({1})...".format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    """
    The callback invoked when the bot receives a message.
    
    The only difference from the default is that when an error occurs,
    the message and error are printed here.
    
    :param message: The message that was received.
    """
    try:
        await bot.process_commands(message)
    except Exception as err:
        print(message, err)

def construct_message(roller, author, detail=True):
    """Constructs the result message for a random dice roll as as a string.
    
    :param roller: The dice roller object with the roll result
    :param author: The original message author
    :param detail: Flag indicating whether or not to include roll details.
    """
    if verbose == False:
        message = "{0} rolled a total of `{1}`.".format(author.mention, roller.result)
    else:
        details = '; '.join(roller.roll_detail_strings())
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
            roll = re.sub(r"\s*\-[^\W\d]+\s*", "", roll)

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
            await bot.say("{0}, the specification you provided did not match any of our roll patterns. Please try again.".format(author.mention))
    except DiceToolsError as err:
        await bot.say("{0}, your roll has produced an error with the following message:\n**{1}**\n Please fix your roll and try again.".format(author.mention, err.get_message()))
    except Exception as err:
        # If an exception is raised, have the bot say so in the channel
        await bot.say("{0}, an unexpected error has occured: {1}.".format(author.mention, err))
        raise err

# Start the bot with the appropriate credentials
# bot.run(login_email, password)
# bot.run('login_token')
