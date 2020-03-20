import unittest

from tests.parsertest import *
from tests.shexgentest import *
from tests.shexfromcsvtest import *

if __name__ == '__main__':
  parsertests = ShExStatementParserTestSuite()
  shexgentests = ShExGeneratorTestSuite()
  shexfromcsvtests = ShExFromCSVTestSuite()
  tests = unittest.TestSuite([parsertests, shexgentests, shexfromcsvtests])
  unittest.main()
