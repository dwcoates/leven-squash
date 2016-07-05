import pprint
import pickle
import time

from levenshtein.leven_squash import LevenSquash
from levenshtein.compression import *
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.utils.computation import *
from levenshtein.score import ScoreDistance


class ATest(object):

    def get_dict(self):
        raise NotImplemented

    def __repr__(self):
        return str(self.get_dict())

    def __str__(self):
        return self._format_dict_repr(self.get_dict())

    @classmethod
    def _format_dict_repr(cls, d):
        pp = pprint.PrettyPrinter(indent=4)

        return pp.pformat(d)


class AResult(ATest):

    def __init__(self, data, name):
        self._data = data
        if type(name) is not str:
            raise TypeError("Result name must be a string.")
        self._name = name

    def get_name(self):
        return self._name

    def get_result(self):
        raise NotImplemented


class Terminal(AResult):

    def __init__(self, result, name):
        super(type(self), self).__init__(result, name)

    def get_dict(self):
        d = dict()

        d[self.get_name()] = self._data

        return d

    def get_result(self):
        return self._data

    def save_data(d, name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def load_data(name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)


class Description(AResult):

    def __init__(self, results, name):
        data = dict()
        try:
            for demo in results:
                data[demo.get_name()] = demo
        except AttributeError:
            raise TypeError("results provided must be a list of " +
                            "Descriptions and/or Terminals")
        super(type(self), self).__init__(data, name)

    def get(self, demo_name):
        try:
            return self._data[demo_name]
        except:
            raise

        return None

    def get_result():
        return self._data()

    def get_dict(self):
        x = dict()
        for demo in self._data:
            x.update(self._data[demo].get_dict())

        d = dict()
        d[self._name] = x

        return d


class ADemo(ATest):
    NAME = None

    def __init__(self, *args, **labels):
        self.NAME = labels.pop('name', self.NAME)
        if self.NAME is None:
            raise ValueError(
                "Name unset by concrete Demo class '" +
                self.__class__.__name__ + "'")
        self._description = Description(self._CREATE_RESULTS(*args), self.NAME)

    def _CREATE_RESULTS(self, *args):
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

    def get(self, item):
        return self._description.get(item)

    def get_description(self):
        return self._description


class StringDemo(ADemo):
    TEXT = "TEXT"
    ENTROPY = "ENTROPY"
    LENGTH = "LENGTH"
    DESCRIPTION = "DESCRIPTION"
    NAME = "STRING"

    def __init__(self, string, str_description=None, str_limit=1000, **labels):
        super(type(self), self).__init__(string, str_description)
        self._limit = str_limit

    @classmethod
    def _CREATE_RESULTS(self, string, str_description):
        results = list()
        results.append(Terminal(string, self.TEXT))
        results.append(Terminal(len(string), self.LENGTH))
        results.append(
            Terminal(ShannonBasic().calculate(string), self.ENTROPY))
        if str_description is not None:
            results.append(Terminal(str_description, self.DESCRIPTION))

        return results

    def get_length(self):
        return self.get(self.LENGTH).get_result()

    def get_text(self, limit=None):
        if limit is None:
            limit = self._limit
        return self.get(self.TEXT).get_result()[0:limit]

    def get_entropy(self):
        return self.get(self.ENTROPY).get_result()

    def __str__(self):
        d = self.get_dict()
        print d[self.NAME].keys()
        # d[self.NAME][self.TEXT] = d[self.TEXT][0:self._limit]

        return self._format_dict_repr(d)


class CompressorDemo(ADemo):
    NAME = "COMPRESSION"
    COMPRESSION = "COMPRESSION"
    SOURCE_LENGTH = "SOURCE STRING LENGTH"
    SOURCE_ENTROPY = "SOURCE STRING ENTROPY"
    SIGNATURE_DESCRIPTION = StringDemo.NAME  # temp
    TIME = "TIME"
    ACCURACY = "ACCURACY"

    def __init__(self, compressor, string_demo, **labels):
        super(type(self), self).__init__(compressor, string_demo)

    @classmethod
    def _CREATE_RESULTS(self, compressor, string_demo):
        diff = ScoreDistance.difference
        source_string = string_demo.get_text()
        signature = ComputationManager.CREATE_COMPUTATION(
            compressor.compress, source_string)
        sig_time = signature.time()
        sig_text = signature.value()

        results = list()
        results.append(Terminal(string_demo.get_length(),
                                self.SOURCE_LENGTH))
        results.append(
            Terminal(string_demo.get_entropy(), self.SOURCE_ENTROPY))
        results.append(StringDemo(sig_text,
                                  ("Signature for " + string_demo.NAME)
                                  # name=self.SIGNATURE_DESCRIPTION
                                  ).get_description())
        results.append(Terminal(sig_time, self.TIME))
        signature_length = len(sig_text)
        expected_length = len(source_string) / float(compressor.getC())
        results.append(
            Terminal(diff(signature_length, expected_length), self.ACCURACY))

        return results

    def get_source_length(self):
        return self.get(self.SOURCE_LENGTH).get_result()

    def get_source_entropy(self):
        return self.get(self.SOURCE_ENTROPY).get_result()

    def get_compression(self):
        return self.get(self.COMPRESSION)

    def get_sig_desc(self):
        return self.get(self.SIGNATURE_DESCRIPTION)

    def get_entropy(self):
        return self.get_sig_desc().get_entropy()

    def get_length(self):
        return self.get_sig_desc().get_length()

    def get_text(self):
        return self.get_sig_desc().get_text()

    def get_time(self):
        return self.get(self.TIME).get_result()

    def get_accuracy(self):
        return self.get(self.ACCURACY).get_result()


class FileDemo(ADemo):
    CONTENTS = StringDemo.NAME  # temp
    FILENAME = "FILENAME"
    NAME = "NAME"

    @classmethod
    def _CREATE_RESULTS(self, fname):
        file_contents = self._parse_file(fname)
        description = file_contents[1]
        text = file_contents[0]

        results = list()
        results.append(Terminal(fname, self.FILENAME))
        results.append(StringDemo(text, None,
                                  # name=self.CONTENTS
                                  ).get_description())

        return results

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
        return self.get(self.FILENAME).get_result()

    def get_length(self):
        return self.get_contents().get_length()

    def get_entropy(self):
        return self.get_contents().get_entropy()

    def get_text(self):
        return self.get_contents().get_text()


class FileComparison(ADemo):
    DIFFERENCE = "DIFFERENCE"
    NAME = "FILE COMPARISON"

    def __init__(self, fname1, fname2, difference="NOT SPECIFIED", **labels):
        super(type(self), self).__init__(fname1, fname2, difference)

    @classmethod
    def _CREATE_RESULTS(self, fname1, fname2, difference):
        results = list()

        results.append(FileDemo(fname1).get_description())
        results.append(FileDemo(fname2).get_description())
        results.append(Terminal(difference, self.DIFFERENCE))

        return results

    def get_file_desc(self, fname):
        return self.get(fname)

    def get_contents(self, fname):
        return self.get_file_desc(fname).get_contents()

    def get_filename(self, fname):
        return self.get_file_desc(fname).get_filename()

    def get_length(self, fname):
        return self.get_file_desc(fname).get_length()

    def get_entropy(self, fname):
        return self.get_file_desc(fname).get_entropy()

    def get_text(self, fname):
        return self.get_file_desc(fname).get_text()


class MeasurementDescription(ADemo):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """
    VALUE = "VALUE"
    TIME = "TIME"
    DESCRIPTION = "ALGORITHM"
    NAME = "DISTANCE"

    def _CREATE_RESULTS(self, sd, measure, **labels):
        results = list()
        c = sd.get(measure)

        results.append(Terminal(c.value(), self.VALUE))
        results.append(Terminal(c.time(), self.TIME))
        results.append(Terminal(measure.__name__, self.DESCRIPTION))

        return results

    def get_value(self):
        return self.get(self.VALUE).get_result()

    def get_time(self):
        return self.get(self.TIME).get_result()


class EstimateDemo(MeasurementDescription):
    ERROR = "ERROR"
    NAME = "SQUASH ESTIMATE"

    def __init__(self, sd, **labels):
        super(type(self), self).__init__(sd, LevenSquash.estimate)

    def _CREATE_RESULTS(self, sd, estimate):
        results = super(type(self), self)._CREATE_RESULTS(sd, estimate)

        results.append(Terminal(sd.diff(
            LevenSquash.estimate, LevenSquash.calculate).value(), self.ERROR))

        return results

    def get_error(self):
        return self.get(self.ERROR).get_result()


class DistanceDemo(MeasurementDescription):

    def __init__(self, sd):
        super(type(self), self).__init__(self, sd, LevenSquash.calculate)


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
    NAME = "SQUASHING"

    def __init__(self, sd):
        super(type(self), self).__init__(sd)

    def _CREATE_RESULTS(self, sd):
        results = list()

        results.append(LSDemo(
            sd.get_leven_squash()).get_description())
        results.append(EstimateDemo(sd).get_description())
        # results.append(Terminals(self.ESTIMATE_CORRECTED, "N/A"))

        return results


class LSDemo(ADemo):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.
    """
    COMPRESSION = "COMPRESSION ALGORITHM"
    DISTANCE = "DISTANCE ALGORITHM"
    NAME = "LEVENSQUASH DESCRIPTION"

    @classmethod
    def _CREATE_RESULTS(self, ls):
        results = list()

        results.append(ProcessDemo(
            ls.get_compressor().get_algorithm()).get_description())
        results.append(ProcessDemo(
            ls.get_ld_alg().get_algorithm()).get_description())

        return results


class ProcessDemo(ADemo):
    PROCESS = "PROCESS"
    NAME = "PROCESS DEMO"

    def __init__(self, process, **labels):
        super(type(self), self).__init__(process)

        # self._desc = process.__doc__.replace('\n', '')

    def _CREATE_RESULTS(self, process):
        results = list()

        results.append(Terminal(process.__class__.__name__, self.PROCESS))

        return results


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
        self._distance = Description("absolute distance: ", self._score)

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
