import random

from src.classes.Stats.StatABC import StatABC
import math


class Agilidad(StatABC):

    def __init__(self, value):
        self.value = value

    def get_p(self):
        return math.tanh(self.value * 0.01)

    def __hash__(self):
        return hash((self.value, Agilidad))

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Agilidad):
            return self.value == other.value
        else:
            return False

    def __str__(self):
        return self.value.__str__()

    def mutate(self):
        new_val = random.uniform(0, 150)
        return Agilidad(new_val)
