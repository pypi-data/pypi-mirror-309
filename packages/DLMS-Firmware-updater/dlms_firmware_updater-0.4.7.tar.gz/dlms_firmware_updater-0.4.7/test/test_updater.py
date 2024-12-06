import sys
import unittest
from DLMSFirmwareUpdater import main


class TestType(unittest.TestCase):
    def test_Serial(self):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(('-t', "Serial", "-p", "COM5", "-T", "20", '-s', "0000000000000000", "-u"))
        main.main()

    def test_File(self):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(('-t', "File", "-p", "name.csv", "-d", "1", "-u"))
        main.main()

    def test_help(self):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(("--help",))
        main.main()
