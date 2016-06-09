from Levenshtein.StringMatcher import StringMatcher


class LDAlgorithm:
    def distance(self, str1, str2):
        raise NotImplemented()


class AbsoluteLD(LDAlgorithm):
    """Simple wrapper class for encapsulating the
    Levenshtein.StringMatcher.distance LD algorithm."""
    @staticmethod
    def distance(self, str1, str2):
        return StringMatcher.distance(str1, str2)

