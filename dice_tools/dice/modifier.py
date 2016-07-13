# Modifier class to present the same interface as a dice roller
class Modifier:
    def __init__(self, value):
        self._val = value

    def roll(self):
        pass

    @property
    def value(self):
        return self._val

    @property
    def rolls(self):
        return (self._val,)

    @property
    def max(self):
        return self._val

    @property
    def min(self):
        return self._val

    @property
    def avg(self):
        return self._val

    def __str__(self):
        return str(self._val)
