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

   def test_shex_from_csv_algorithm(self):
    shexstatement = CSV.generate_shex_from_csv("examples/wikidata/algorithm.csv", delim=";")
    desired = '''start = @<algorithm>
<algorithm> {
  wdt:P31 [ wd:Q8366  ] ;#instance of a algorithm
  wdt:P138 .* ;#named after
  wdt:P61 .* ;#discoverer or inventor
  wdt:P3752 .+ ;#worst-case time complexity
  wdt:P3753 .+ ;#best-case time complexity
  wdt:P3754 .+ ;#average time complexity
  wdt:P3755 .+ ;#worst-case space complexity
  wdt:P3756 .+ ;#best-case space complexity 
  wdt:P3757 .+ ;#average space complexity 
  wdt:P575 .{0,1} ;#time of discovery or invention
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_os(self):
    shexstatement = CSV.generate_shex_from_csv("examples/wikidata/operatingsystem.csv", delim=";")
    desired = '''start = @<operatingsystem>
<operatingsystem>  EXTRA wdt:P31  {
  wdt:P31 [ wd:Q9135  ] ;#instance of a operating system
  wdt:P138 .* ;#named after
  wdt:P178 .* ;#developer
  wdt:P277 .* ;# programming language
  wdt:P571 .{0,1} ;#inception
  wdt:P1448 .* ;#official name
  wdt:P737 .* ;#influenced by
  wdt:P856 .* ;#official website
}'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

if __name__ == '__main__':
  unittest.main()

