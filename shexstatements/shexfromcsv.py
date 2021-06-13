#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
import re
from shexstatements.shexstatementsparser import ShExStatementLexerParser
from io import StringIO


class CSV:
    """
      This class contains functions that can be used to generate ShEx from a data string or a CSV file.
    """
    @staticmethod
    def generate_shex_from_data_string(data):
        """
        This method can be used to generate ShEx from data string. However, the input data string must contain one or more lines. Each line contains '|' separated values.

        Parameters
        ----------
          data : str
            shexstatements in CSV format, using "|" as a delimiter.

        Returns
        -------
          shex
            shape expression

        """
        shexstatement = ""
        try:
            lexerparser = ShExStatementLexerParser()
            lexerparser.build()
            lexerparser.buildparser()
            tokens = lexerparser.input(data)
            result = lexerparser.parse(data)
            shexstatement = result.generate_shex()
        except Exception as e:
            print("Unable to parse. Error: " + str(e))
        return shexstatement

    @staticmethod
    def generate_shex_from_csv(filepath, delim=",", skip_header=False, filename=True):
        """
        This method can be used to generate ShEx from data string. However, the input data string must contain one or more lines. Each line contains '|' separated values. If filepath is a string, filename  should be set to false.

        Parameters
        ----------
          filepath : str
            This parameter can contain either a file path of a CSV file or shexstatements in CSV format.
          delim : str
            a delimiter. Allowed values include ',', '|' and ';' 
          skip_header : bool
            if the first line is a header, set this value to True. By default, the value is False.
          filename : bool
            if 'filepath' is a string, then this filename must be set to False

        Returns
        -------
          shex
            shape expression

        """
        shexstatement = ""
        try:
            pattern = '^\s*$'
            data = ""
            if filename:
                csvfile = open(filepath, 'r')
                csvreader = csv.reader(csvfile, delimiter=delim)
            else:
                # It's a multi-line string
                csvstring = StringIO(filepath)
                csvreader = csv.reader(csvstring, delimiter=delim)
            rowno = 0
            for row in csvreader:
                rowno = rowno + 1
                if skip_header and rowno == 1:
                    continue
                line = ""
                for value in row:
                    if value and not re.match(pattern, value):
                        if not line:
                            line = value
                        else:
                            line = line + "|" + value
                data = data + line + "\n"
            shexstatement = CSV.generate_shex_from_data_string(data)
            if filename:
                csvfile.close()
        except Exception as e:
            print("Unable to read file. Error: " + str(e))
        return shexstatement
