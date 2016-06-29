from Levenshtein.StringMatcher import StringMatcher

from levenshtein.utils.computation import CalculationCache


class LDAlgorithm:

    def distance(self, str1, str2):
        raise NotImplemented()


class CachedLDAlgorithm:

    def __init__(self, ld_algorithm):
        self._ld = ld_algorithm
        self._cache = CalculationCache()

    def distance(self, str1, str2):
        return self._cache.produce(self._ld.distance, str1, str2)


class AbsoluteLD(LDAlgorithm):
    """Simple wrapper class for encapsulating the
    Levenshtein.StringMatcher.distance LD algorithm."""

    def distance(self, str1, str2):
        sm = StringMatcher(None, str1, str2)

        return sm.distance()
