from Levenshtein import distance as levenshtein_distance

from levenshtein.utils.process import *
from levenshtein.utils.computation import CalculationCache


class LDAlgorithm (Process):
    # Probably will want an approximation algorithm here. Those have to
    # be equipped with some error factor.

    def __call__(self, str1, str2):
        raise NotImplemented


class Absolute (LDAlgorithm):
    """Simple wrapper class for encapsulating the
    Levenshtein.StringMatcher.distance LD algorithm."""

    def __call__(self, str1, str2):
        return levenshtein_distance(str1, str2)


class LevenDistance (Calculation):

    def __init__(self, algorithm=Absolute(), **kwargs):
        super(LevenDistance, self).__init__(algorithm, kwargs)

    def distance(self, str1, str2):
        return self.get_algorithm().__call__(str1, str2)
