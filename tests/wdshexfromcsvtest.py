#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexfromcsv import CSV

class WDShExFromCSVTestSuite(unittest.TestCase):
   def test_shex_from_csv_datastructure(self):
    shexstatement = CSV.generate_shex_from_csv("examples/wikidata/datastructure.csv", delim=";")
    desired = '''start = @<datastructure>
<datastructure> {
  wdt:P31 [ wd:Q175263  ] ;#instance of a data structure
  wdt:P138 .* ;#named after
  wdt:P61 .* ;#discoverer or inventor
  wdt:P3752 .+ ;#worst case time complexity
  wdt:P3753 .+ ;#best case time complexity
  wdt:P3754 .+ ;#average time complexity
  wdt:P3755 .+ ;#worst case space complexity
  wdt:P3756 .+ ;#best case space complexity 
  wdt:P3757 .+ ;#average space complexity 
  wdt:P575 .{1} ;#time of discovery or invention
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)


if __name__ == '__main__':
  unittest.main()

