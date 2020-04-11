#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import unittest
from shexstatements.shexfromcsv import CSV

class ShExFromCSVTestSuite(unittest.TestCase):
   def test_shex_from_csv(self):
    shexstatement = CSV.generate_shex_from_csv("examples/example.csv")
    desired = '''start = @<painting>
<painting> {
  P31 [ Q3305213  ] ;
  P571 [ xsd:dateTime  ] ;#date of creation
  P572 [ xsd:dateTime  ] ;
  P276 .+ ;
  P1476 .+ ;
  P195 .+ ;
  P170 @<creator>+ ;#creator of painting
}
<creator> {
  P2561 LITERAL ;#name
}
'''
    self.assertEqual(shexstatement, desired)

   def test_shex_from_csv_empty_values(self):
    shexstatement = CSV.generate_shex_from_csv("examples/emptyvalues.csv")
    desired = '''start = @<painting>
<painting> {
  P31 [ Q3305213  ] ;
  P571 [ xsd:dateTime  ] ;#date of creation
  P572 [ xsd:dateTime  ] ;
  P276 .+ ;
  P1476 .+ ;
  P195 .+ ;
  P170 @<creator>+ ;#creator of painting
}
<creator> {
  P2561 LITERAL ;#name
}
'''
    self.assertEqual(shexstatement, desired)

   def test_shex_from_csv_languages(self):
    shexstatement = CSV.generate_shex_from_csv("examples/language.csv")
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .* ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_languages_delim_bar(self):
    shexstatement = CSV.generate_shex_from_csv("examples/languagedelimbar.csv", delim="|")
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .* ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)


   def test_shex_from_csv_languages_delim_semicolon(self):
    shexstatement = CSV.generate_shex_from_csv("examples/languagedelimsemicolon.csv", delim=";")
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .* ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_tvseries(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tvseries.csv")
    desired = '''start = @<tvseries>
<tvseries> {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .+ ;#director
  wdt:P58 .+ ;#screenwriter
}
<genre> {
  wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_tvseries_negative_prop(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tests/tvseriesnegativeprop.csv")
    desired = '''start = @<tvseries>
<tvseries> {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .+ ;#director
  wdt:P58 .+ ;#screenwriter
  wdt:P279 .{0} ;#no subclass values
  ^wdt:P279 .{0} ;#no such statements
}
<genre> {
  wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)


   def test_shex_from_csv_tvseriesextra(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tvseriesextra.csv")
    desired = '''start = @<tvseries>
<tvseries>  EXTRA wdt:P31  {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .+ ;#director
  wdt:P58 .+ ;#screenwriter
}
<genre>  EXTRA wdt:P31  {
  wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_languages_with_header(self):
    shexstatement = CSV.generate_shex_from_csv("examples/languageheader.csv", skip_header=True)
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .* ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_languages_with_numeric_cardinality(self):
    shexstatement = CSV.generate_shex_from_csv("examples/languagenumcardinality.csv")
    desired = '''start = @<language>
<language> {
  wdt:P31 [ wd:Q34770  ] ;# instance of a language
  wdt:P1705 LITERAL ;# native name
  wdt:P17 .+ ;# spoken in country
  wdt:P2989 .+ ;# grammatical cases
  wdt:P282 .+ ;# writing system
  wdt:P1098 .+ ;# speakers
  wdt:P1999 .{1} ;# UNESCO language status
  wdt:P2341 .+ ;# indigenous to
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

if __name__ == '__main__':
  unittest.main()

