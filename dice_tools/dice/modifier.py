# Modifier class to present the same interface as a dice roller
class Modifier:
    def __init__(self, value):
        self._val = value

    def __int__(self):
        return self._val

    def __str__(self):
        return str(self._val)
    
    @property
    def total(self):
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
