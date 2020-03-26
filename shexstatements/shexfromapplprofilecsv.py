#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
import re
from shexstatements.shexstatementsparser import ShExStatementLexerParser
from shexstatements.shexfromcsv import CSV

class ApplicationProfile(CSV):
  def generate_shex_from_csv(filepath, delim=",", skip_header=False):
    pass
