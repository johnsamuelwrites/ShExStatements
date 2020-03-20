#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
from shexstatements.shexstatementsparser import ShExStatementLexerParser

class CSV:
  def generate_shex_from_csv(filepath, delim=","):
    data = ""
    with open(filepath, 'r') as csvfile:
     csvreader = csv.reader(csvfile, delimiter=delim)
     for row in csvreader:
         data = data + "|".join(row)
    lexerparser = ShExStatementLexerParser()
    lexerparser.build()
    lexerparser.buildparser()
    tokens = lexerparser.input(data)
    result = lexerparser.parse(data)
    shexstatement = result.generate_shex()
    return shexstatement

