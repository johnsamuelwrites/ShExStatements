#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexjfromcsv import ShExJCSV

class ShExJFromCSVTestSuite(unittest.TestCase):
   def test_shex_from_csv(self):
    shexj = ShExJCSV.generate_shexj_from_csv("examples/language.csv")
    desired = ""
    with open("examples/language.shexj") as shexjfile:
      desired = shexjfile.read()

    self.maxDiff = None
    # read adds extra character, hence omit the last one
    self.assertEqual(shexj, desired[0:len(shexj)])


if __name__ == '__main__':
  unittest.main()

