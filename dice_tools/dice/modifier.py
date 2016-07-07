# Modifier class to present the same interface as a dice roller
class Modifier:
    def __init__(self, value):
        self._val = value

    @property
    def value(self):
        return self._val

    @property
    def rolls(self):
        return (self._val,)

    @property
    def highest(self):
        return self._val

    @property
    def lowest(self):
        return self._val
