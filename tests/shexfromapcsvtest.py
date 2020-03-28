#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexfromapplprofilecsv import ApplicationProfile

class ShExFromAPCSVTestSuite(unittest.TestCase):
   def test_shex_from_ap_csv(self):
    shexstatement = ApplicationProfile.generate_shex_from_csv("examples/languageap.csv", skip_header=True)
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ]{1} ;#instance of a language
  wdt:P1705 @<LITERALtype>{1} ;#native name of language
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases of language
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# number of speakers
  wdt:P1999 .{1} ;# UNESCO language status
  wdt:P2341 .+ ;# languages indigenous to
}
<LITERALtype> {
  rdf:type LITERAL ;
}
'''
    self.maxDiff = None
    self.assertEqual(desired,shexstatement)

if __name__ == '__main__':
  unittest.main()

