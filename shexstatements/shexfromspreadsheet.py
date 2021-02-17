#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from openpyxl import load_workbook
from xlrd import open_workbook
from os.path import splitext
from odf.opendocument import OpenDocumentSpreadsheet,load
from odf.table import Table, TableCell, TableRow
from shexstatements.shexfromcsv import CSV

class Spreadsheet:
  """
    This class contains functions that can be used to generate ShEx from a data string or a Spreadsheet file
    (.xlsx,.xls,.ods)
  """
   
  @staticmethod
  def generate_shex_from_spreadsheet(filepath, skip_header=False):
    """
    This method can be used to generate ShEx from data string. However, the input data string must contain one or more lines. Each line contains '|' separated values. If filepath is a string, filename  should be set to false.

    Parameters
    ----------
      filepath : str
        This parameter contains path of a Spreadsheet file
      skip_header : bool
        if the first line is a header, set this value to True. By default, the value is False.

    Returns
    -------
      shex
        shape expression

    """
    shexstatement = ""
    try:
      pattern = '^\s*$'
      data = ""
      filename, file_extension = splitext(filepath)

      if(file_extension in {".xlsx",".xlsm",".xltx",".xltm"}):
         wb = load_workbook(filepath)
         for ws in wb.worksheets:
           for i in range(1,ws.max_row+1):
             line = list()
             for j in range(1,ws.max_column+1):
               cell = ws.cell(row=i,column=j).value
               if cell is not None:
                 line.append(cell)
             line = "|".join(line)
             data = data + line + "\n"

      elif(file_extension in {".xls"}):
         wb = open_workbook(filepath)
         for sheet in wb.sheets():
           for i in range(0,wb.sheets()[0].nrows):
             line = list()
             for j in range(0,wb.sheets()[0].ncols):
               cell = sheet.cell(i,j).value
               if len(str(cell)) > 0:
                 line.append(cell)
             data = data + "|".join(line) + "\n"

      elif(file_extension in {".ods"}):
         wb = load(filepath)
         wb = wb.spreadsheet
         rows = wb.getElementsByType(TableRow)
         for row in rows:
           cells = row.getElementsByType(TableCell)
           line = list()
           for cell in cells:
             if len(str(cell)) > 0:
               line.append(str(cell))
           data = data+"|".join(line) + "\n"

      shexstatement = CSV.generate_shex_from_data_string(data)
    except Exception as e:
      print("Unable to read file. Error: " + str(e))
    return shexstatement

