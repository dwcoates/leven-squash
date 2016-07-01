from levenshtein.utils.computation import CalculationCache, ComputationManager


class Process (object):

    def __call__(self, *args):
        try:
            self._execute(self, *args)
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
        if uncached_process.__class__.__name__ != CachedProcess.__name__:
            return CachedProcess(uncached_process)
        elif uncached_process.__class__.__name__ == CachedProcess.__name__:
            return uncached_process
        else:
            raise ValueError("'MAKE_CACHED_VERSION' only accepts a " +
                             "parameter of type 'Process'")

    @staticmethod
    def MAKE_UNCACHED_PROCESS(cached_process):
        if cached_process.__class__.__name__ == CachedProcess.__name__:
            return cached_process._process
        elif cached_process.__class__.__name__ != CachedProcess.__name__:
            return cached_process
        else:
            raise ValueError("'MAKE_CACHED_VERSION' only accepts a " +
                             "parameter of type 'Process'")


class Calculation (object):

    def __init__(self, process, *args, **kwargs):
        self._process = process
        self.set_cache(kwargs.pop('cached', None))

    def set_cache(self, cached):
        if cached is True:
            self.set_algorithm(
                CachedProcess.MAKE_CACHED_PROCESS(self._process))
        else:
            self.set_algorithm(
                CachedProcess.MAKE_UNCACHED_PROCESS(self._process))

    def set_algorithm(self, alg):
        self._process = alg

    def get_algorithm(self):
        return self._process
