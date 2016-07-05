from levenshtein.utils.computation import CalculationCache, ComputationManager
import inspect


class Process (object):
    """
    Callable algorithm.
    """

    def __call__(self, *args):
        try:
            return self._execute(*args)
        except:
            TypeError()

    def _execute(self, *args):
        raise NotImplementedError(
            "Process is an algorithm template. Not implemented.")


class CachedProcess (Process):

    # Is it bad practice to have a constructor have variable arguments like
    # this? Feels hackish.
    def __init__(self, process):
        self._cache = CalculationCache()
        self._process = CachedProcess.MAKE_UNCACHED_PROCESS(process)

    def __call__(self, *args):
        try:
            return self._cache.produce(self._process._execute, *args)
        except:
            TypeError()
            # CacheError

    @staticmethod
    def MAKE_CACHED_PROCESS(uncached_process):
        if CachedProcess in inspect.getmro(uncached_process.__class__):
            return uncached_process
        elif Process in inspect.getmro(uncached_process.__class__):
            return CachedProcess(uncached_process)
        else:
            raise ValueError("'MAKE_CACHED_VERSION' only accepts a " +
                             "parameter of type 'Process'")

    @staticmethod
    def MAKE_UNCACHED_PROCESS(cached_process):
        if CachedProcess in inspect.getmro(cached_process.__class__):
            return cached_process._process
        elif Process in inspect.getmro(cached_process.__class__):
            return cached_process
        else:
            raise ValueError("'MAKE_CACHED_VERSION' only accepts a " +
                             "parameter of type 'Process'")


class Calculation (object):

    def __init__(self, process, *args, **kwargs):
        self._process = process
        self.set_cache(kwargs.pop('cached', False))

    def set_cache(self, cached):
        if cached is True:
            self.set_algorithm(
                CachedProcess.MAKE_CACHED_PROCESS(self._process))
        else:
            self.set_algorithm(
                CachedProcess.MAKE_UNCACHED_PROCESS(self._process))
            print "algorithm set: " + self._process.__class__.__name__

    def set_algorithm(self, alg):
        self._process = alg

    def get_algorithm(self):
        return self._process
