import logging

from levenshtein.utils.log import LoggerManager, setup_logging

class TestLoggerManager():
    logger = logging.getLogger("compression")

    def test_setup_logging_finds_default_log_file(self):
        """
        Minimal test to confirm that the log file is being found
        """
        try:
            setup_logging()
        except IOError:
            print("levenshtein.utils.log.setup_logging could not find logfile")
            #assert()
            raise

    def test_message_logging_to_log_file(self):
        TestLoggerManager.logger.info("hello, this is some info")
        TestLoggerManager.logger.debug("hello, found a bug")
        TestLoggerManager.logger.error("hello, found an error")


    @classmethod
    def setup(cls):
        # Reset logger
        #logging.shutdown()
        #reload(logging)
        pass

    @classmethod
    def teardown(cls):
        # Reset logger
        #logging.shutdown()
        #reload(logging)
        pass

    def test_logging_manager(self):
        log = LoggerManager.get_logger("compression")
        log.info("hello")
