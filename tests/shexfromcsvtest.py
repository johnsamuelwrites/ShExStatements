#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexfromcsv import CSV

class ShExFromCSVTestSuite(unittest.TestCase):
   def test_shex_from_csv(self):
    shexstatement = CSV.generate_shex_from_csv("painting.csv")
    desired = '''start = @<painting>
<painting> {
  P31 [ Q3305213  ];
  P571 [ xsd:dateTime  ];
  P572 [ xsd:dateTime  ];
  P276 .+;
  P1476 .+;
  P195 .+;
  P170 @<creator>+;
}
<creator> {
  P31 .+;
}
'''
    self.assertEqual(shexstatement, desired)

if __name__ == '__main__':
  unittest.main()

