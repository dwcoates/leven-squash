import pprint
import pickle
import time

from levenshtein.leven_squash import LevenSquash
from levenshtein.compression import *
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.utils.computation import *
from levenshtein.score import ScoreDistance


class ADescription(object):

    def __init__(self, data, name):
        self._data = data
        if type(name) is not str:
            raise TypeError("Result name must be a string.")
        self._name = name

    def __repr__(self):
        return str(self.get_dict())

    def __str__(self):
        return self._format_dict_repr(self.get_dict())

    def get_name(self):
        return self._name

    def get_result(self):
        raise NotImplemented

    def get_dict(self):
        raise NotImplemented

    @classmethod
    def _format_dict_repr(cls, d):
        pp = pprint.PrettyPrinter(indent=4)

        return pp.pformat(d)


class Terminal(ADescription):

    def __init__(self, result, name):
        ADescription.__init__(self, result, name)

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


class Description(ADescription):

    def __init__(self, results, name):
        data = dict()
        try:
            for demo in results:
                data[demo.get_name()] = demo
        except AttributeError:
            raise TypeError("Results provided must be a list of " +
                            "Descriptions and/or Terminals")
        ADescription.__init__(self, data, name)

    def get(self, demo_name):
        if demo_name in self._data:
            return self._data[demo_name]

        return None

    def get_result():
        return self.get_dict()[self._name]

    def get_dict(self):
        x = dict()
        for demo in self._data:
            x.update(self._data[demo].get_dict())

        d = dict()
        d[self._name] = x

        return d


class DemoDescriptionInterface(object):
    NAME = None

    pass


class IString(DemoDescriptionInterface):
    NAME = "STRING"
    TEXT = "TEXT"
    ENTROPY = "ENTROPY"
    LENGTH = "LENGTH"
    DESCRIPTION = "DESCRIPTION"

    def get_length(self):
        raise NotImplemented

    def get_text(self, limit=None):
        raise NotImplemented

    def get_entropy(self):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented


class ICompressor(DemoDescriptionInterface):
    NAME = "COMPRESSION"
    COMPRESSION = "COMPRESS"
    SOURCE_LENGTH = "SOURCE STRING LENGTH"
    SOURCE_ENTROPY = "SOURCE STRING ENTROPY"
    SIGNATURE_DESCRIPTION = "Temp"  # temp
    TIME = "TIME"
    ACCURACY = "ACCURACY"

    def get_source_length(self):
        raise NotImplemented

    def get_source_entropy(self):
        raise NotImplemented

    def get_compression(self):
        raise NotImplemented

    def get_sig_desc(self):
        raise NotImplemented

    def get_entropy(self):
        raise NotImplemented

    def get_length(self):
        raise NotImplemented

    def get_text(self):
        raise NotImplemented

    def get_time(self):
        raise NotImplemented

    def get_accuracy(self):
        raise NotImplemented


class IFile(DemoDescriptionInterface):
    NAME = "NAME"
    CONTENTS = "TEMP"  # temp
    FILENAME = "FILENAME"

    def get_contents(self):
        raise NotImplemented

    def get_filename(self):
        raise NotImplemented

    def get_length(self):
        raise NotImplemented

    def get_entropy(self):
        raise NotImplemented

    def get_text(self):
        raise NotImplemented


class IFileComp(DemoDescriptionInterface):
    NAME = "FILE COMPARISON"
    DIFFERENCE = "DIFFERENCE"

    def get_file_desc(self, fname):
        raise NotImplemented

    def get_contents(self, fname):
        raise NotImplemented

    def get_filename(self, fname):
        raise NotImplemented

    def get_length(self, fname):
        raise NotImplemented

    def get_entropy(self, fname):
        raise NotImplemented

    def get_text(self, fname):
        raise NotImplemented


class IMeasurement(DemoDescriptionInterface):
    NAME = "DISTANCE"
    VALUE = "VALUE"
    TIME = "TIME"
    DESCRIPTION = "ALGORITHM"

    def get_value(self):
        raise NotImplemented

    def get_time(self):
        raise NotImplemented


class IEstimate(IMeasurement):
    NAME = "SQUASH ESTIMATE"
    ERROR = "ERROR"

    def get_error(self):
        raise NotImplemented


class IDistance(IMeasurement):
    NAME = "ABSOLUTE DISTANCE"
    pass


class ISquash(DemoDescriptionInterface):
    NAME = "SQUASHING"
    LEVENSQUASH_MODULE = "LEVENSQUASH MODULE"
    ESTIMATE = "ESTIMATE"
    ESTIMATE_CORRECTED = "ESTIMATE CORRECTED"

    pass


class ILevenSquash(DemoDescriptionInterface):
    NAME = "LEVENSQUASH DESCRIPTION"
    COMPRESSION = "COMPRESSION ALGORITHM"
    DISTANCE = "DISTANCE ALGORITHM"

    pass


class IProcess(DemoDescriptionInterface):
    NAME = "PROCESS DEMO"
    PROCESS = "PROCESS"

    pass


def pdemo(demo_results):
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(demo_results)


class DemoDescription(Description, DemoDescriptionInterface):

    def __init__(self, descriptions, **labels):
        self.NAME = labels.pop('name', self.NAME)
        # calls self.set_labels
        if self.NAME is None:
            raise ValueError(
                "Name unset by concrete Demo class '" +
                self.__class__.__name__ + "'")

        Description.__init__(self, descriptions, self.NAME)

    def save_data(d, name):
        raise NotImplemented

    def load_data(name):
        raise NotImplemented


class SingularDescription(DemoDescription, DemoDescriptionInterface):

    def __init__(self, *args, **labels):
        data = self._RESULTS(*args)

        DemoDescription.__init__(self, data, **labels)

    def _RESULTS(self, *args):
        raise NotImplemented


class SingularStringDesc(SingularDescription, IString):

    def __init__(self, string, str_description, str_limit=1000,
                 **labels):
        SingularDescription.__init__(self, string, str_description, **labels)
        self._limit = str_limit

    def _RESULTS(self, string, str_description):
        results = list()
        results.append(Terminal(string, self.TEXT))
        results.append(Terminal(len(string), self.LENGTH))
        results.append(
            Terminal(ShannonBasic().calculate(string), self.ENTROPY))
        if str_description is not None:
            results.append(
                Terminal(str_description, self.DESCRIPTION))

        return results

    def __str__(self):
        d = self.get_dict()
        d[self.NAME][self.TEXT] = self.get_text()

        return self._format_dict_repr(d)

    def get_length(self):
        return self.get(self.LENGTH).get_result()

    def get_text(self, limit=None):
        if limit is None:
            limit = self._limit
        return self.get(self.TEXT).get_result()[0:limit]

    def get_entropy(self):
        return self.get(self.ENTROPY).get_result()

    def get_description(self):
        r = self.get(self.DESCRIPTION)
        if r is not None:
            return r.get_result()
        return r


class SingularCompressorDesc(SingularDescription, ICompressor):

    def __init__(self, compressor, string_demo, **labels):
        SingularDescription.__init__(self, compressor, string_demo, **labels)

    def _RESULTS(self, compressor, string_demo):
        diff = ScoreDistance.difference
        source_string = string_demo.get_text()
        signature = ComputationManager.CREATE_COMPUTATION(
            compressor.compress, source_string)
        sig_time = signature.time()
        sig_text = signature.value()

        results = list()
        results.append(Terminal(string_demo.get_length(),
                                self.SOURCE_LENGTH))
        results.append(Terminal(string_demo.get_entropy(),
                                self.SOURCE_ENTROPY))
        results.append(SingularStringDesc(sig_text,
                                          ("Signature for " +
                                           string_demo.NAME),
                                          name=self.SIGNATURE_DESCRIPTION
                                          ))
        results.append(Terminal(sig_time, self.TIME))
        signature_length = len(sig_text)
        expected_length = len(source_string) / float(compressor.getC())
        results.append(Terminal(diff(signature_length, expected_length),
                                self.ACCURACY))
        results.append(Terminal("N/A", self.COMPRESSION))

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


class SingularFileDesc(SingularDescription, IFile):

    def __init__(self, filename, **labels):
        SingularDescription.__init__(self, filename, **labels)

    def _RESULTS(self, fname):
        file_contents = self._parse_file(fname)
        description = file_contents[1]
        text = file_contents[0]

        results = list()
        results.append(Terminal(fname, self.FILENAME))
        results.append(SingularStringDesc(text, description,
                                          name=self.CONTENTS
                                          ))

        return results

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


class SingularFileComp(SingularDescription, IFileComp):

    def __init__(self, fname1, fname2, difference="Not Specified", **labels):
        SingularDescription.__init__(
            self, fname1, fname2, difference, **labels)

    def _RESULTS(self, fname1, fname2, difference):
        results = list()

        results.append(SingularFileDesc(fname1, name=fname1))
        results.append(SingularFileDesc(fname2, name=fname2))
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


class SingularMeasurementDesc(SingularDescription, IMeasurement):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """

    def __init__(self, sd, measure, **labels):
        SingularDescription__init__(self, sd, measure, **labels)

    def _RESULTS(self, sd, measure):
        results = list()
        c = sd.get(measure)

        results.append(Terminal(c.value(), self.VALUE))
        results.append(Terminal(c.time(), self.TIME))
        results.append(Terminal(measure.__name__,
                                self.DESCRIPTION))

        return results

    def get_value(self):
        return self.get(self.VALUE).get_result()

    def get_time(self):
        return self.get(self.TIME).get_result()


class SingularEstimateDesc(SingularMeasurementDesc, IEstimate):

    def __init__(self, sd, **labels):
        SingularDescription.__init__(
            self, sd, **labels)

    def _RESULTS(self, sd):
        results = SingularMeasurementDesc._RESULTS(
            self, sd, LevenSquash.estimate)

        results.append(Terminal(sd.diff(LevenSquash.estimate,
                                        LevenSquash.calculate).value(),
                                self.ERROR))

        return results

    def get_error(self):
        return self.get(self.ERROR).get_result()


class SingularDistanceDesc(SingularMeasurementDesc, IDistance):

    def __init__(self, sd, **labels):
        SingularDescription.__init__(self, sd, **labels)

    def _RESULTS(self, sd):
        return SingularMeasurementDesc._RESULTS(self, sd, LevenSquash.calculate)


class SingularSquashDesc(SingularDescription, ISquash):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    describe_levenshquash(ls) and assess_distance_measures(str1, str2, ls)
    under keys "LEVENSQUASH MODULE" and "DISTANCE"
    """

    def __init__(self, sd, **labels):
        SingularDescription.__init__(self, sd, **labels)

    def _RESULTS(self, sd):
        results = list()

        results.append(LSDescription(sd.get_leven_squash()))
        results.append(SingularEstimateDesc(sd))
        # results.append(Terminals(self.ESTIMATE_CORRECTED, "N/A"))

        return results


class SingularLSDesc(SingularDescription, ILevenSquash):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.
    """

    def __init__(self, ls, **labels):
        SingularDescription.__init__(self, ls, **labels)

    def _RESULTS(self, ls):
        results = list()

        results.append(ProcessDescription(
            ls.get_compressor().get_algorithm()).get_description())
        results.append(ProcessDescription(
            ls.get_ld_alg().get_algorithm()).get_description())

        return results


class SingularProcessDesc(SingularDescription, IProcess):

    def __init__(self, process, **labels):
        SingularDescription.__init__(self, process, **labels)

    def _RESULTS(self, process):
        results = list()

        results.append(Terminal(process.__class__.__name__,
                                SingularProcessDesc.PROCESS))

        return results


class Demo:
    """
    Class for constructing demo descriptions
    """
    pass


class DemoFiles(Description):

    def add(ls):
        """
        Add results for ls to demo
        """
        pass

    def __init__(self, f1, f2, ls):
        start = time.clock()
        print("DEMO: DEMO START...")

        print("DEMO: READING FILES '" + f1 + "' AND '" + f2 + "'...")
        self._file_comp = SingularFileComp.CREATE(f1, f2)
        text1 = self._file_comp.get_file_desc(f1).get_text()
        text2 = self._file_comp.get_file_desc(f2).get_text()

        self._score = ScoreDistance(text1, text2, ls)
        print("DEMO: CALCULATING ABSOLUTE LEVENSHTEIN DISTANCE...")
        self._distance = Description("absolute distance: ", self._score)

        print("DEMO: PRODUCING SQUASH DEMO...")
        self._squash_desc = SingularSquashDesc("squash desc", self._score)

        print("DEMO: FINISH.")
        print("DEMO: TIME TO PROCESS: " + str(time.clock() - start))

    def get(self):
        d = dict()

        d["FILES"] = self._file_comp.get()
        d["SQUASH"] = self._squash_desc.get()
        d["DISTANCE"] = self._distance.get()

        return d


class DemoDescriptionSet(DemoDescription, DemoDescriptionInterface):

    def __init__(self, descriptions, **labels):
        DemoDescription.__init__(self, descriptions, **labels)

    def add(self, demo):
        raise NotImplemented


class ListedDescription(DemoDescriptionSet, DemoDescriptionInterface):
    _DESCIPTION_TYPE = None

    def __init__(self, desc_type, descs, **labels):
        self._DESCIPTION_TYPE = desc_type.__name__

        for d in descs:
            if d.__class__.__name__ is not self._DESCIPTION_TYPE:
                raise TypeError("'" + self.__class__.__name__ +
                                "' ListedDescription only " +
                                "accepts Description type '" +
                                self._DESCIPTION_TYPE + "'. " +
                                "Got '" + d.__class__.__name__ + "'.")

        self.NAME = desc_type.__class__.__name__ + " objects"
        DemoDescriptionSet.__init__(self, descs, **labels)

    def get_dict(self):
        d = dict()

        d[self.get_name()] = map(lambda d: d.get_dict(), self._data.values())

        return d

    def get(item):
        try:
            item_results = map(lambda d: d.get(item), self._data)
            return ListedDescription(item_results, str(item) +
                                     "s in '" + self._name + "'")
        except:
            ValueError()


class DistributedDescription(DemoDescriptionSet, DemoDescriptionInterface):
    NAME = None

    _DESCRIPTION_TYPE = None

    def __init__(self, demolists):
        DemoDescriptionSet.__init__(self, demolists)

    def add(self, description):
        raise NotImplemented


class DistributedStringDesc(DistributedDescription, IString):
    NAME = "HELLO"

    def __init__(self, descriptions):
        results = list()

        text = map(lambda x: Terminal(
            x.get_text(), x.get_name()), descriptions)
        ent = map(lambda x: Terminal(
            x.get_entropy(), x.get_name()), descriptions)
        length = map(lambda x: Terminal(
            x.get_length(), x.get_name()), descriptions)
        desc = map(lambda x: Terminal(
            x.get_description(), x.get_name()), descriptions)
        results.append(ListedDescription(Terminal, text, name=self.TEXT))
        results.append(ListedDescription(Terminal, ent, name=self.ENTROPY))
        results.append(ListedDescription(Terminal, length, name=self.LENGTH))
        results.append(ListedDescription(
            Terminal, desc, name=self.DESCRIPTION))

        DistributedDescription.__init__(self, results)

        self._descriptions = ListedDescription(
            SingularStringDesc, descriptions, name=self.NAME)


class DistributedCompressorDesc(DistributedDescription, ICompressor):
    NAME = "Compressor Results"

    def __init__(self, descriptions):
        results = list()

        text = map(lambda x: Terminal(
            x.get_text(), x.get_name()), descriptions)
        source_length = map(lambda x: Terminal(
            x.get_source_length(), x.get_name()), descriptions)
        source_entropy = map(lambda x: Terminal(
            x.get_source_entropy(), x.get_name()), descriptions)
        time = map(lambda x: Terminal(
            x.get_time(), x.get_name()), descriptions)
        accuracy = map(lambda x: Terminal(
            x.get_accuracy(), x.get_name()), descriptions)

        results.append(ListedDescription(
            Terminal, text, name=self.COMPRESSION))
        results.append(ListedDescription(
            Terminal, source_length, name=self.SOURCE_LENGTH))
        results.append(ListedDescription(
            Terminal, source_entropy, name=self.SOURCE_ENTROPY))
        results.append(ListedDescription(Terminal, time, name=self.TIME))
        results.append(ListedDescription(
            Terminal, accuracy, name=self.ACCURACY))
        # results.append(DistributedStringDesc())

        DistributedDescription.__init__(self, results)

        self._descriptions = ListedDescription(
            SingularCompressorDesc, descriptions, name=self.NAME)


class DistributedEstimateDesc(DistributedDescription, IEstimate):
    NAME = "Estimates"

    def __init__(self, descriptions, **labels):
        results = list()

        value = map(lambda x: Terminal(
            x.get_value(), x.get_name()), descriptions)
        time = map(lambda x: Terminal(
            x.get_time(), x.get_name()), descriptions)
        error = map(lambda x: Terminal(
            x.get_error(), x.get_name()), descriptions)

        results.append(ListedDescription(Terminal, value, name=self.VALUE))
        results.append(ListedDescription(Terminal, time, name=self.TIME))
        results.append(ListedDescription(Terminal, error, name=self.ERROR))

        DistributedDescription.__init__(self, descriptions, **labels)

        self._descriptions = ListedDescription(SingularEstimateDesc,
                                               descriptions, name=self.NAME
                                               )

    def get_error(self):
        return self.get(self.ERROR).get_result()


class SingularDistanceDesc(SingularMeasurementDesc, IDistance):

    def __init__(self, sd, **labels):
        SingularDescription.__init__(self, sd, **labels)

    def _RESULTS(self, sd):
        return SingularMeasurementDesc._RESULTS(self, sd, LevenSquash.calculate)


class SingularSquashDesc(SingularDescription, ISquash):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    describe_levenshquash(ls) and assess_distance_measures(str1, str2, ls)
    under keys "LEVENSQUASH MODULE" and "DISTANCE"
    """

    def __init__(self, sd, **labels):
        SingularDescription.__init__(self, sd, **labels)

    def _RESULTS(self, sd):
        results = list()

        results.append(LSDescription(sd.get_leven_squash()))
        results.append(SingularEstimateDesc(sd))
        # results.append(Terminals(self.ESTIMATE_CORRECTED, "N/A"))

        return results


class SingularLSDesc(SingularDescription, ILevenSquash):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.
    """

    def __init__(self, ls, **labels):
        SingularDescription.__init__(self, ls, **labels)

    def _RESULTS(self, ls):
        results = list()

        results.append(ProcessDescription(
            ls.get_compressor().get_algorithm()).get_description())
        results.append(ProcessDescription(
            ls.get_ld_alg().get_algorithm()).get_description())

        return results


class SingularProcessDesc(SingularDescription, IProcess):

    def __init__(self, process, **labels):
        SingularDescription.__init__(self, process, **labels)

    def _RESULTS(self, process):
        results = list()

        results.append(Terminal(process.__class__.__name__,
                                SingularProcessDesc.PROCESS))

        return results
