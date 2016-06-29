from timeit import default_timer as timer
import copy


class Computation:
    """
    Class for encapsulating a calculation's result and the time to calculate.
    Prefer building Computations with ComputationManager.CREATE_COMPUTATION.
    """

    def __init__(self, value, time):
        self._value = value
        self._time = time

    def time(self):
        return self._time

    def value(self):
        return self._value

    def __repr__(self):
        return ("(" + str(self.value()) + ", " +
                str(self.time()) + "s)")


class ComputationManager:
    _TIME_REGISTER = 0

    def __init__(self):
        raise NotImplementedError(
            "ComputationManager cannot be instantiated or extended.")

    @staticmethod
    def CREATE_COMPUTATION(function, *args):
        """
        Return appropriate computation for method 'function' with arguments
        'args'. Will return correct time even if 'function' itself features
        calls to CREATE_COMPUTATION possibly replaced by a cache source, so
        long as the cache uses REGISTER_COMPUTATION appropriately.
        """
        r0 = ComputationManager._TIME_REGISTER

        start = timer()
        v = function(*args)
        t = timer() - start

        r = ComputationManager._TIME_REGISTER - r0

        return Computation(v, t + r)

    @staticmethod
    def REGISTER_COMPUTATION(computation):
        """
        Register computation 'computation' as recently computed. This means
        that if the call to this method occurs within a call in
        CREATE_COMPUTATION to 'function', CREATE_COMPUTATION will bel able to
        consider computation.time() in its return value.
        """
        if computation.__class__.__name__ != Computation.__name__:
            raise ValueError("ComputationManager.REGISTER_COMPUTATION only " +
                             "accepts instances of type" +
                             Computation.__name__)

        ComputationManager._TIME_REGISTER += computation.time()


class CalculationCache:
    """
    Caches computations. Times them and stores their results and times in a
    Calculation. Returns computation values. To return complete calculations,
    use ComputationManager.CREATE_COMPUTATION(cache_instance.produce) or
    something similiar. Note, this cache's default key creator uses the
    IDs of the cached function's arguments. Therefore, do not use this default
    method (create_key) to cache functions accepting mutable arguments.
    """

    def __init__(self):
        self._cache = dict()

    @classmethod
    def _yield(cls, computation):
        """
        Return a safe and appropriate representation of computation.value().
        """
        return computation.value()

    def check(self, key):
        """
        Check cached value corresponding to 'key'. This will not notify the
        CalculationManager, and so is not suitable if you want to source the
        cache publically.
        """
        if self.exists(key):
            return copy.deepcopy(self._cache[key])
        return None

    def exists(self, key):
        """
        Return True iff there exists a computation corresponding to 'key'.
        """
        if key in self._cache:
            return True
        else:
            return False

    def source(self, key):
        """
        Get value corresponding to 'key' if it exists. Prefer
        produce(function, args). Will register the calculation to
        CalculationManager so that it's being sourced is known to
        methods calling this one.
        """
        computation = self.check(key)
        if computation is not None:
            ComputationManager.REGISTER_COMPUTATION(computation)
            return self._yield(computation)
        return None

    def add(self, key, function, *args):
        """
        Add Calculation 'calculation' to cache under key 'key'. Prefer
        produce(function, args).
        """
        computation = ComputationManager.CREATE_COMPUTATION(
            function, *args)
        self._add(key, computation)

    def _add(self, key, computation):
        if self.exists(key):
            raise ValueError("Cache already has computation for key '" +
                             key + "': " + str(self.check(key)) +
                             ". Remove with clear(key) before adding if " +
                             "this is intended.")

        self._cache[key] = computation

    def produce(self, function, *args):
        """
        Wraps get(key) and add(key, calculation) to guarantee that a
        calculation corresponding to 'function' and 'args' will be returned,
        whether it already exists in the cache or not. Note, this uses
        CaclulationCache.create_key to create the key. This method is only
        well-defined for immutable 'args'.
        """
        key = self.create_key(function, *args)

        v = self.source(key)
        if v is None:
            self.add(key, function, *args)
            v = self._yield(self.check(key))

        return v

    def clear(self, key):
        """
        Remove element of cache corresponding to key 'key'.
        """
        if key not in self._cache:
            raise ValueError("Removal of key '" + key + "' failed. Cache " +
                             "does not contain it.")
        else:
            del self._cache[key]

    def reset_cache(self, *ignore):
        """
        Reset cache. 'ignore' is a list of keys to not be affected by the
        reset.
        """
        delete = list()
        for key in self._cache:
            if key not in ignore:
                delete.append(key)

        for i in delete:
            self.clear(i)

    @classmethod
    def create_key(cls, function, *args):
        """
        Return a key corresponding to function 'function' accepting 'args'.
        Recommended (but not necessary) input to add(key, calculation). This
        method roduces keys with id(arg), so is only useful for immutable
        'args'. Otherwise, manually create keys.
        """
        return ''.join(map(lambda x: str(id(x)), args) + [function.__name__])
