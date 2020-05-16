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
  wdt:P31 [ wd:Q3305213  ] ;
  wdt:P571 xsd:dateTime  ;#date of creation
  wdt:P572 xsd:dateTime  ;
  wdt:P276 .+ ;
  wdt:P1476 .+ ;
  wdt:P195 .+ ;
  wdt:P170 @<creator>+ ;#creator of painting
}
<creator> {
  wdt:P2561 LITERAL ;#name
}
'''
    self.assertEqual(desired in shexstatement, True)

   def test_shex_from_csvstring(self):
    csvstring = '''@painting,P31,Q3305213
@painting,P571,xsd:dateTime,#date of creation
@painting,P572,xsd:dateTime
@painting,P276,.,+
@painting,P1476,.,+
@painting,P195,.,+
@painting,P170,@creator,+,#creator of painting
@creator,P2561,LITERAL,#name'''
    shexstatement = CSV.generate_shex_from_csv(csvstring, filename=False)
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
  wdt:P31 [ wd:Q3305213  ] ;
  wdt:P571 xsd:dateTime  ;#date of creation
  wdt:P572 xsd:dateTime  ;
  wdt:P276 .+ ;
  wdt:P1476 .+ ;
  wdt:P195 .+ ;
  wdt:P170 @<creator>+ ;#creator of painting
}
<creator> {
  wdt:P2561 LITERAL ;#name
}
'''
    self.assertEqual(desired in shexstatement, True)

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

   def test_shex_from_csv_foaf_person(self):
    shexstatement = CSV.generate_shex_from_csv("examples/foaf.csv")
    desired = '''start = @<person>
<person> {
  rdf:type foaf:Person  ;#should be a person
  foaf:name LIteral ;#name
  foaf:mbox IRi* ;#mail
  foaf:homepage IRI* ;#URL
  foaf:nick Literal* ;#Nickname
  foaf:depiction IRI* ;#photograph
  foaf:interest IRI* ;#topics of interest
  foaf:knows @<person>* ;#person knows another person 
}
'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" in shexstatement, True)
    self.assertEqual("PREFIX foaf: <http://xmlns.com/foaf/0.1/>" in shexstatement, True)

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
    shexstatement = CSV.generate_shex_from_csv("examples/tvseries.csv", delim="|")
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
    shexstatement = CSV.generate_shex_from_csv("examples/tests/tvseriesnegativeprop.csv", delim="|")
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

   def test_shex_from_csv_tvseries_cardinality(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tests/onevaluecardinality.csv", delim="|")
    desired = '''start = @<tvseries>
<tvseries> {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .{1,} ;#director
  wdt:P58 .{1,} ;#screenwriter
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
    shexstatement = CSV.generate_shex_from_csv("examples/tvseriesextra.csv", delim=";")
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

   def test_shex_from_csv_tvseriesplusplus(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tvseriesplusplus.csv", delim=";")
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

   def test_shex_from_csv_tvseriesclosed(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tvseriesclosed.csv", delim=";")
    desired = '''start = @<tvseries>
<tvseries>  EXTRA wdt:P31  {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .+ ;#director
  wdt:P58 .+ ;#screenwriter
}
<genre>  CLOSED {
  wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
}'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_tvseriesclosedsymbols(self):
    shexstatement = CSV.generate_shex_from_csv("examples/tvseriesclosedsymbols.csv", delim=";")
    desired = '''start = @<tvseries>
<tvseries>  EXTRA wdt:P31  {
  wdt:P31 [ wd:Q5398426  ] ;# instance of a tvseries
  wdt:P136 @<genre>* ;# genre
  wdt:P495 .+ ;#country of origin
  wdt:P57 .+ ;#director
  wdt:P58 .+ ;#screenwriter
}
<genre>  CLOSED {
  wdt:P31 [ wd:Q201658 wd:Q15961987  ] ;#instance of genre
}'''
    self.maxDiff = None
    self.assertEqual(desired in shexstatement, True)
    self.assertEqual("PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" in shexstatement, True)
    self.assertEqual("PREFIX wd: <http://www.wikidata.org/entity/>" in shexstatement, True)
    self.assertEqual("PREFIX wdt: <http://www.wikidata.org/prop/direct/>" in shexstatement, True)

   def test_shex_from_csv_languages_with_header(self):
    shexstatement = CSV.generate_shex_from_csv("examples/header/languageheader.csv", skip_header=True)
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

