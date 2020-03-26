#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
import json
import re
from shexstatements.shexstatementsparser import ShExStatementLexerParser
from shexstatements.shexfromcsv import CSV
from pyshexc.parser_impl.generate_shexj import parse

class ShExJCSV:
  def generate_shexj_from_csv(filepath, delim=",", skip_header=False):
    shexj = ""

    try:
      shexstatement = CSV.generate_shex_from_csv(filepath, delim=delim, skip_header=skip_header)
      shexjson=parse(shexstatement)._as_json
      parsed = json.loads(shexjson)
      shexj = json.dumps(parsed, indent=4, sort_keys=False)
    except Exception as e:
      print("Unable to parse. Error: " + str(e))
    return shexj

