from Levenshtein.StringMatcher import StringMatcher


class LDAlgorithm:
    def distance(self, str1, str2):
        raise NotImplemented()


class AbsoluteLD(LDAlgorithm):
    """Simple wrapper class for encapsulating the
    Levenshtein.StringMatcher.distance LD algorithm."""
    def distance(self, str1, str2):
        sm = StringMatcher(None, str1, str2)

        return sm.distance()
