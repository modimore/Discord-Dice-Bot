'''
Errors specifically relating to this module.
'''

class DiceToolsError(Exception):
    ''' General dice tools error. '''
    ''' Just states that the error occured in this module. '''
    def get_message(self):
        return "Unknown DiceToolsError encountered"

class NotRolledError(DiceToolsError):
    ''' Error for when a request value has not been rolled for. '''
    def __init__(self, dice):
        self.dice = dice

    def get_message(self):
        return "Attempted to access results of `{0}` without first rolling".format(dice.get_spec())

class InvalidDiceSpecError(DiceToolsError):
    ''' Error signaling an improper dice specification. '''
    def __init__(self, spec):
        self.spec = spec

    def get_message(self):
        return "Invalid dice specification provided: `{0}`".format(self.spec)

class InvalidDiceOptionError(DiceToolsError):
    ''' Error signaling an invalid dice option was given. '''
    def __init__(self, opt):
        self.opt = opt

    def get_message(self):
        return "Invalid dice option specified: `{0}`".format(self.opt)
