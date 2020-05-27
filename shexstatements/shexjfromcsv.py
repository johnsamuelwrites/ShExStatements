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
  """
    This class contains functions that can be used to generate ShExJ from a ShEx.
  """
  @staticmethod
  def generate_shexj_from_shexstament(shexstatement):
    """
    This method can be used to generate ShEx from data string. However, the input data string must contain one or more lines. Each line contains '|' separated values.

    Parameters
    ----------
      shexstatement : str
        shex

    Returns
    -------
      shexj
        shape expression in JSON (ShExJ)

    """
    shexj = ""
    try:
      shexjson=parse(shexstatement)._as_json
      parsed = json.loads(shexjson)
      shexj = json.dumps(parsed, indent=4, sort_keys=False)
    except Exception as e:
      print("Unable to parse. Error: " + str(e))
    return shexj

  @staticmethod
  def generate_shexj_from_csv(filepath, delim=",", skip_header=False):
    """
    This method can be used to generate ShExJ from ShExStatements CSV file

    Parameters
    ----------
      filepath : str
        This parameter can contain either a file path of a CSV file or shexstatements in CSV format.
      delim : str
        a delimiter. Allowed values include ',', '|' and ';' 
      skip_header : bool
        if the first line is a header, set this value to True. By default, the value is False.

    Returns
    -------
      shexj
        shape expression in JSON format (ShExJ)

    """
    shexj = ""

    try:
      shexstatement = CSV.generate_shex_from_csv(filepath, delim=delim, skip_header=skip_header)
      shexj = ShExJCSV.generate_shexj_from_shexstament(shexstatement) 
    except Exception as e:
      print("Unable to parse. Error: " + str(e))
    return shexj

