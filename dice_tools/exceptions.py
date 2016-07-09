class DiceToolsError(Exception):
    def get_message(self):
        return "Unknown DiceToolsError encountered"

class NotRolledError(DiceToolsError):
    def __init__(self, dice):
        self.dice = dice

    def get_message(self):
        return "Attempted to access results of `{0}` without first rolling".format(dice.get_spec())

class InvalidDiceSpecError(DiceToolsError):
    def __init__(self, spec):
        self.spec = spec

    def get_message(self):
        return "Invalid dice specification provided: `{0}`".format(self.spec)

class InvalidDiceOptionError(DiceToolsError):
    def __init__(self, opt):
        self.opt = opt

    def get_message(self):
        return "Invalid dice option specified: `{0}`".format(self.opt)
