#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from tests.parsertest import *
from tests.shexgentest import *
from tests.shexfromcsvtest import *
from tests.shexfromapcsvtest import *
from tests.shexjfromcsvtest import *

if __name__ == '__main__':
  parsertests = ShExStatementParserTestSuite()
  shexgentests = ShExGeneratorTestSuite()
  shexfromcsvtests = ShExFromCSVTestSuite()
  shexfromapcsvtests = ShExFromAPCSVTestSuite()
  shexjfromcsvtests = ShExJFromCSVTestSuite()
  tests = unittest.TestSuite([parsertests, shexgentests, shexfromcsvtests, shexfromapcsvtests, shexjfromcsvtests])
  unittest.main()
