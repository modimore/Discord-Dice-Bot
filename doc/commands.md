# Bot Commands
All commands issued to this bot must be prefaced with a special character, *!*. The commands are listed below.

Your instance may use a different command prefix, but *!* will be used in all examples here.

## !roll
This is currently the only supported command. The command must be followed by a specification for what you are rolling, which is detailed on the [Roll Specification][roll-spec] page.

[roll-spec]: https://github.com/modimore/Discord-Dice-Bot/blob/master/doc/roll-spec.md

Write your command to the bot as `!roll (spec)`. Here are some examples.

- `!roll 1d10 - 2d8 + 3`
- `!roll -avg 2d8 + 3`
- `!roll 1d20:adv + 4`
