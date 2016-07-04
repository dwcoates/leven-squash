import pprint
import pickle
import time

from levenshtein.leven_squash import LevenSquash
from levenshtein.compression import *
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.utils.computation import *
from levenshtein.score import ScoreDistance


class AResult(object):

    def __init__(self, data, name):
        self._data = data
        self._name = name

    def get_name(self):
        return self._name

    def get_dict(self):
        raise NotImplemented

    def __repr__(self):
        return str(self.get_dict())

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)

        return pp.pformat(self.get_dict())


class Terminal(AResult):

    def __init__(self, result, name):
        super(type(self), self).__init__(result, name)

    def get_result(self):
        return self._data

    def get_dict(self):
        d = dict()

        d[self.get_name()] = self._data

        return d

    def save_data(d, name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def load_data(name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)


class Results(AResult):

    def __init__(self, results, name):
        data = dict()
        for demo in results:
            data[demo] = demo
        super(type(self), self).__init__(data, name)

    def get(self, demo_name):
        try:
            return self._data[demo_name].get_result()
        except:
            raise

        return None

    def get_dict(self):
        x = dict()
        # print self._data
        for demo in self._data:
            x.update(self._data[demo].get_dict())

        d = dict()
        d[self._name] = x

        return d


class ADemo(AResult):
    NAME = None

    def __init__(self, *args, **labels):
        self.NAME = labels.pop('name', self.NAME)
        self._description = self.CREATE_DESCRIPTION(*args)

    def CREATE_DESCRIPTION(self, *args):
        raise NotImplemented

    def save_data(d, name):
            # TODO: Implement
        with open('records/' + name + '.pkl', 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def load_data(name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def get_dict(self):
        return self._description.get_dict()

    def get_name(self):
        return self._description.get_name()

    def get(self, item):
        return self._description.get(item)


class StringDemo(ADemo):
    TEXT = "TEXT"
    ENTROPY = "ENTROPY"
    LENGTH = "LENGTH"
    DESCRIPTION = "DESCRIPTION"
    NAME = "STRING"

    def __init__(self, string, str_description, str_limit=1000, **labels):
        super(type(self), self).__init__(string, str_description)
        self._limit = str_limit

    @classmethod
    def CREATE_DESCRIPTION(self, string, str_description):
        results = list()
        results.append(Terminal(string, self.TEXT))
        results.append(Terminal(len(string), self.LENGTH))
        results.append(
            Terminal(ShannonBasic().calculate(string), self.ENTROPY))
        results.append(Terminal(str_description, self.DESCRIPTION))

        return Results(results, self.NAME)

    def get_length(self):
        return self.get(self.LENGTH)

    def get_text(self):
        return self.get(self.TEXT)

    def get_entropy(self):
        return self.get(self.ENTROPY)


class CompressorDemo(ADemo):
    NAME = "COMPRESSIOn"
    COMPRESSION = "COMPRESSION"
    SOURCE_LENGTH = "SOURCE STRING LENGTH"
    SOURCE_ENTROPY = "SOURCE STRING ENTROPY"
    SIGNATURE_DESCRIPTION = "SIGNATURE DESCRIPTION"
    TIME = "TIME"
    ACCURACY = "ACCURACY"

    @classmethod
    def CREATE_DESCRIPTION(self, compressor, string_demo):
        diff = ScoreDistance.difference
        source_string = string_demo.get_text()
        print "HELO: " + str(type(source_string))
        print source_string
        signature = ComputationManager.CREATE_COMPUTATION(
            compressor.compress, source_string)
        sig_time = signature.time()
        sig_text = signature.value()

        results = list()
        results.append(Terminal(self.SOURCE_LENGTH,
                                string_demo.get_length()))
        results.append(Terminal(self.SOURCE_ENTROPY,
                                string_demo.get_entropy()))
        results.append(StringDemo("Signature: " +
                                  string_demo.get_name(),
                                  sig_text,
                                  description=self.SIGNATURE_DESCRIPTION))
        results.append(Terminal(self.TIME, sig_time))
        print sig_text
        signature_length = len(sig_text)
        expected_length = len(source_string) / float(compressor.getC())
        results.append(Terminal(self.ACCURACY, diff(signature_length,
                                                    expected_length)))

        return Results(self.NAME, results)

    def get_compression(self):
        return get(self.COMPRESSION)

    def get_source_length(self):
        return get(self.SOURCE_LENGTH)

    def get_source_entropy(self):
        return get(self.SOURCE_ENTROPY)

    def get_sig_desc(self):
        return get(self.SIGNATURE_DESCRIPTION)

    def get_time(self):
        return get(self.TIME)

    def get_accuracy(self):
        return get(self.ACCURACY)


class FileDemo(ADemo):
    CONTENTS = "CONTENT"
    FILENAME = "FILENAME"

    @classmethod
    def CREATE_DESCRIPTION(self, fname):
        file_contents = self._parse_file(fname)
        description = file_contents[1]

        results = list()
        results.append(StringDemo(self.CONTENTS, "Contents of file '" +
                                  fname + "'", file_contents[0]))

        return Results(description, results)

    @staticmethod
    def _parse_file(fname):
        """
        Read file, and parse for description and text. Returns tuple with
        elements (text, description)
        """
        with open(fname) as f:
            text = f.read().replace('\n', '')

        # Currently just returns file text
        description = ""

        return (text, description)

    def get_contents(self):
        return self.get(self.CONTENTS)

    def get_filename(self):
        return self.get(self.FILENAME)

    def get_compression(self):
        return self.get_contents().get_compression()

    def get_source_length(self):
        return self.get_contents().get_source_length()

    def get_source_entropy(self):
        return self.get_contents().get_source_entropy()

    def get_sig_desc(self):
        return self.get_contents().get_sig_desc()

    def get_time(self):
        return self.get_contents().get_time()

    def get_accuracy(self):
        return self.get_contents().get_accuracy()


class FileComparison(ADemo):
    DIFFERENCE = "DIFFERENCE"

    def __init__(self, fname1, fname2, difference="NOT SPECIFIED"):
        pass

    @classmethod
    def CREATE_DESCRIPTION(self, fname1, fname2, difference):
        files = list()

        files.append(FileDemo(fname1))
        files.append(FileDemo(fname2))

        diff = Terminal(self.DIFFERENCE, difference)

        return Results(files, diff)

    def get_file_desc(self, fname):
        return self._files[fname]


class MeasurementDescription(ADemo):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """
    VALUE = "VALUE"
    TIME = "TIME"

    @classmethod
    def CREATE(cls, description, sd, measure):
        results = list()

        c = sd.get(measure)
        results.append(Terminal(cls.VALUE, c.value()))
        results.append(Terminal(cls.TIME, c.time()))

        return cls(description, results)


class EstimateDemo(MeasurementDescription):
    ERROR = "ERROR"

    @classmethod
    def CREATE(cls, description, sd):
        results = list()

        c = sd.get(measure)
        results.append(Terminal(cls.VALUE, c.value()))
        results.append(Terminal(cls.TIME, c.time()))
        results.append(Terminal(cls.ERROR, ScoreDistance.difference(
            LevenSquash.estimate, LevenSquash.calculate)))

        return cls(description, results)


class DistanceDemo(MeasurementDescription):

    @classmethod
    def CREATE(cls, note, sd):
        return super(type(self), self).CREATE(note, sd, LevenSquash.calculate)


class SquashDemo(ADemo):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    describe_levenshquash(ls) and assess_distance_measures(str1, str2, ls)
    under keys "LEVENSQUASH MODULE" and "DISTANCE"
    """
    LEVENSQUASH_MODULE = "LEVENSQUASH MODULE"
    ESTIMATE = "ESTIMATE"
    ESTIMATE_CORRECTED = "ESTIMATE_CORRECTED"

    def __init__(self, note, sd):
        pass

    def CREATE(cls, note, sd):
        results = list()

        results.append(LevenSquashDemo.CREATE(
            "ls module desc", sd.get_leven_squash()))
        results.append(EstimateDemo.CREATE("a super cool estimate", sd))
        results.append(Terminals(cls.ESTIMATE_CORRECTED, "N/A"))

        return cls(note, results)


class LSDemo(ADemo):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.
    """

    @classmethod
    def CREATE(cls, note, ls):
        results = list()
        results.append(ProcessDemo.CREATE(ls.get_compressor().get_algorithm()))
        results.append(ProcessDemo.CREATE(ls.get_ld_alg().get_algorithm()))
        return cls("LevenSquash description", results)


class ProcessDemo(ADemo):

    def __init__(self, process):
        self._type = process.__class__.__name__
        # self._desc = process.__doc__.replace('\n', '')


class DemoFiles(ADemo):

    def add(ls):
        """
        Add results for ls to demo
        """
        pass

    def __init__(self, f1, f2, ls):
        start = time.clock()
        print("DEMO: DEMO START...")

        print("DEMO: READING FILES '" + f1 + "' AND '" + f2 + "'...")
        self._file_comp = FileComparison.CREATE(f1, f2)
        text1 = self._file_comp.get_file_desc(f1).get_text()
        text2 = self._file_comp.get_file_desc(f2).get_text()

        self._score = ScoreDistance(text1, text2, ls)
        print("DEMO: CALCULATING ABSOLUTE LEVENSHTEIN DISTANCE...")
        self._distance = Results("absolute distance: ", self._score)

        print("DEMO: PRODUCING SQUASH DEMO...")
        self._squash_desc = SquashDescription("squash desc", self._score)

        print("DEMO: FINISH.")
        print("DEMO: TIME TO PROCESS: " + str(time.clock() - start))

    def get(self):
        d = dict()

        d["FILES"] = self._file_comp.get()
        d["SQUASH"] = self._squash_desc.get()
        d["DISTANCE"] = self._distance.get()

        return d


class DemoSet(AResult):

    def __init__(self, name, demos=[]):
        super(type(self), self).__init__(name)
        self._demos = demos

    def get_demo(demo):
        try:
            return self._demos[demo]
        except:
            raise ValueError()

    def add(self, name, description):
        raise NotImplemented


class ListedDemo(DemoSet):

    def add(demo):
        """
        Add demo to list of demos
        """
        self._demos.append(demos)

    def get_dict():
        d = dict()

        d[self.get_name()] = map(lambda d: d.get_dict(), self._demos)

        return d

    def get(item):
        try:
            item_results = map(lambda d: d.get(item), self._demos)
            return ListedDemo(item_results, str(item) +
                              "s in '" + self._name + "'")
        except:
            ValueError()


class DistributedDemo(DemoSet):

    def __init__(self, name, demos=[]):
        super(type(self), self).__init__(name)

    def add(self, description):
        raise NotImplemented
