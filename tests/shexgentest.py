#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexstatementsparser import ShExStatementLexerParser

class ShExGeneratorTestSuite(unittest.TestCase):
  def setUp(self):
    self.lexerparser = ShExStatementLexerParser()
    self.lexerparser.build()
    self.lexerparser.buildparser()
    

    
  def test_shexstatements_with_cardinality(self):
    data = '''@painting|P31|Q3305213
    @painting|P571|xsd:dateTime
    @painting|P572|xsd:dateTime
    @painting|P276|.|+
    @painting|P1476|.|+
    @painting|P195|.|+
    @painting|P170|@creator|+
    @creator|P31|.|+'''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    shexstatement = result.generate_shex()
    desired = '''start = @<painting>
<painting> {
  P31 [ Q3305213  ] ;
  P571 [ xsd:dateTime  ] ;
  P572 [ xsd:dateTime  ] ;
  P276 .+ ;
  P1476 .+ ;
  P195 .+ ;
  P170 @<creator>+ ;
}
<creator> {
  P31 .+ ;
}
'''
    self.assertEqual(shexstatement, desired)

  def test_shexstatements_with_prefixed_node(self):
    data = '''@painting|P31|Q3305213
    @painting|P571|xsd:dateTime
    @painting|P572|xsd:dateTime
    @painting|P276|.|+
    @painting|P1476|.|+
    @painting|P195|.|+
    @painting|P170|@painting:creator|+
    @painting:creator|P31|.|+'''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    shexstatement = result.generate_shex()
    desired = '''start = @<painting>
<painting> {
  P31 [ Q3305213  ] ;
  P571 [ xsd:dateTime  ] ;
  P572 [ xsd:dateTime  ] ;
  P276 .+ ;
  P1476 .+ ;
  P195 .+ ;
  P170 @<painting:creator>+ ;
}
<painting:creator> {
  P31 .+ ;
}
'''
    self.assertEqual(shexstatement, desired)
    
  def test_shexstatements_with_valueset(self):
    data = '''
    @endangeredlanguage|P31|Q83365345,Q83365347,Q83365366,Q83365404,Q38058796
    @endangeredlanguage|P1999|Q20672087,Q20672088,Q20672089,Q20672090,Q20672091
    @endangeredlanguage|P17|.|*
    @endangeredlanguage|P220|.|+
    @endangeredlanguage|P12341|.|*
    @endangeredlanguage|P220|LITERAL'''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    shexstatement = result.generate_shex()
    desired ='''start = @<endangeredlanguage>
<endangeredlanguage> {
  P31 [ Q83365345 Q83365347 Q83365366 Q83365404 Q38058796  ] ;
  P1999 [ Q20672087 Q20672088 Q20672089 Q20672090 Q20672091  ] ;
  P17 .* ;
  P220 .+ ;
  P12341 .* ;
  P220 LITERAL ;
}
'''
    self.assertEqual(shexstatement, desired)

  def test_shexstatements_with_multiple_nodes(self):
    data = '''@flag|P31|Q7242811
@flag|P18|.|+
@flag|P571|.|*
@flag|P1268|.|*
@flag|P3089|.|*
@flag|p:P462|@color|+
@color|ps:P462|@colorinstance
@color|pq:P465|.|*
@colorinstance|P31|Q1075'''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    shexstatement = result.generate_shex()
    desired='''start = @<flag>
<flag> {
  P31 [ Q7242811  ] ;
  P18 .+ ;
  P571 .* ;
  P1268 .* ;
  P3089 .* ;
  p:P462 @<color>+ ;
}
<color> {
  ps:P462 @<colorinstance> ;
  pq:P465 .* ;
}
<colorinstance> {
  P31 [ Q1075  ] ;
}
'''
    self.maxDiff = None
    self.assertEqual(shexstatement, desired)

  def test_shexstatements_with_prefixes(self):
    data = '''p|<http://www.wikidata.org/prop/>
ps|<http://www.wikidata.org/prop/statement/>
pq|<http://www.wikidata.org/prop/qualifier/>
@flag|P31|Q7242811
@flag|P18|.|+
@flag|P571|.|*
@flag|P1268|.|*
@flag|P3089|.|*
@flag|p:P462|@color|+
@color|ps:P462|@colorinstance
@color|pq:P465|.|*
@colorinstance|P31|Q1075'''
    tokens = self.lexerparser.input(data)
    result = self.lexerparser.parse(data)
    shexstatement = result.generate_shex()
    desired='''
start = @<flag>
<flag> {
  P31 [ Q7242811  ] ;
  P18 .+ ;
  P571 .* ;
  P1268 .* ;
  P3089 .* ;
  p:P462 @<color>+ ;
}
<color> {
  ps:P462 @<colorinstance> ;
  pq:P465 .* ;
}
<colorinstance> {
  P31 [ Q1075  ] ;
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX p: <http://www.wikidata.org/prop/>" in shexstatement, True)
    self.assertEqual("PREFIX ps: <http://www.wikidata.org/prop/statement/>" in shexstatement, True)
    self.assertEqual("PREFIX pq: <http://www.wikidata.org/prop/qualifier/>" in shexstatement, True)

if __name__ == '__main__':
  unittest.main()

