from Levenshtein import distance as levenshtein_distance

from levenshtein.utils.process import *
from levenshtein.utils.computation import CalculationCache


class LDAlgorithm (Process):
    # Probably will want an approximation algorithm here. Those have to
    # be equipped with some error factor.

    def _execute(self, str1, str2):
        if type(str1) is not str or type(str2) is not str:
            warn = ("LDAlgorithm '%s' received non-strings to process" % (
                self.__class__.__name__))
            raise TypeError(warn)


class Absolute (LDAlgorithm):
    """Simple wrapper class for encapsulating the
    Levenshtein.StringMatcher.distance LD algorithm."""

    def _execute(self, str1, str2):
        LDAlgorithm._execute(self, str1, str2)
        return levenshtein_distance(str1, str2)


class LevenDistance (Calculation):

    def __init__(self, algorithm=Absolute(), **kwargs):
        super(LevenDistance, self).__init__(algorithm, kwargs)

    def __copy__(self):
        c = type(self)()
        c.__dict__.update(self.__dict__)
        return c

    def distance(self, str1, str2):
        return self.get_algorithm().__call__(str1, str2)
