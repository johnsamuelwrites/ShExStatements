#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexstatementsparser import ShExStatementLexerParser

class ShExStatementParserTestSuite(unittest.TestCase):
  def setUp(self):
    self.lexerparser = ShExStatementLexerParser()
    self.lexerparser.build()
    self.lexerparser.buildparser()
    

  def test_basic_shexstatements(self):
    data = '''paa|paa:pp|aa:aa
              ppaa|paa:pp|[aa:aa]
              ppaa|paa:pp|[aa:aa a:a]
           '''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    
  def test_shexstatements_with_constraints(self):
    data = '''
    painting|P31|Q3305213
    painting|P571|xsd:dateTime
    painting|P276|.|+
    painting|P1476|.|+ 
    painting|P195|.|+
    painting|P170|creator|+
    creator|P31|.|+
           '''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    
  def test_shexstatements_with_valueset(self):
    data = '''
    endangeredlanguage|P31|Q83365345,Q83365347,Q83365366,Q83365404,Q38058796
    endangeredlanguage|P1999|Q20672087,Q20672088,Q20672089,Q20672090,Q20672091
    endangeredlanguage|P17|.|*
    endangeredlanguage|P220|.|+
    endangeredlanguage|P12341|.|*
    endangeredlanguage|P220|LITERAL
           '''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
 
  def test_shexstatements(self):
    data = '''paa|paa:pp|aa:aa 
    paa|paa:pp|aa:aa,b1:cv 
    paa|paa:pp|aa:aa b1:cv 
    paa|paa:pp|[aa:aa] 
    ppaa|paa:pp|[aa:aa a:a] 
    paa|paa:pp|aa:aa,b1:cv 
    paa|paa:pp|aa:aa b1:cv 
    ''' 
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)

if __name__ == '__main__':
  unittest.main()

