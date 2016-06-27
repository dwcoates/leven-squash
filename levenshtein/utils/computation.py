from timeit import default_timer as timer


class Computation:

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


class ComputationCache:

    def __init__(self):
        self._cache = dict()

    def get(self, key):
        """
        Get Calculation corresponding to key 'key' if it exists. Prefer
        produce(function, args).
        """
        if key in self._cache:
            c = self._cache[key]
            ComputationManager.REGISTER_COMPUTATION(c)
            return c
        else:
            return None

    def add(self, key, calculation):
        """
        Add Calculation 'calculation' to cache under key 'key'. Prefer
        produce(function, args).
        """
        if key in self._cache:
            raise ValueError("Cache already has value and time for key '" +
                             key + "': (" + self.get_value[key] + ", " +
                             self.get_time[key] + ". Remove with clear(key) " +
                             "before adding.")
        else:
            self._cache[key] = calculation

    def produce(self, function, *args):
        """
        Wraps get(key) and add(key, calculation) to guarantee that a
        calculation corresponding to 'function' and 'args' will be returned,
        whether it already exists in the cache or not.
        """
        key = self.create_key(function, *args)
        computation = self.get(key)
        if computation is None:
            computation = ComputationManager.CREATE_COMPUTATION(
                function, *args)
            self.add(key, computation)

        return computation

    def clear(self, key):
        """
        Remove element of cache corresponding to key 'key'.
        """
        if key not in self._cache:
            raise ValueError("Removal of key '" + key + "' failed. Cache " +
                             "does not contain key.")
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

    def create_key(self, function, *args):
        """
        Return a consistent key correspoding to function 'function' accepting
        arguments 'arguments'. Recommended (but not necessary) input to
        add(key, calculation).
        """
        return ''.join(map(lambda x: str(id(x)), args) + [function.__name__])
