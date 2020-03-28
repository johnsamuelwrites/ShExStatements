#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import csv
import re
from shexstatements.shexstatementsparser import ShExStatementLexerParser
from shexstatements.shexfromcsv import CSV

"""
Following are the terms used by the Dublin Core Application Profile.
These terms are mapped to the ShExStatements in the following manner

DCAP term : ShExStatements
==========================
Entityname    : Node name
Property      : Property 
PropertyLabel :	
Mand          : Cardinality
Repeat        : Cardinality
Value         : Value
Valuetype     : Value
Annotation    :	Annotation

"""

class ApplicationProfile:
  def generate_shex_from_csv(filepath, delim=",", skip_header=False):
    shexstatement = ""
    try:
      data = ""
      with open(filepath, 'r') as csvfile:
       csvreader = csv.reader(csvfile, delimiter=delim)
       rowno = 0
       shapename = ""
       typelines = set()
       for row in csvreader:
         rowno = rowno + 1
         if skip_header and rowno == 1:
          continue 
         line = ""
         #Ignore lines with incorrect number of values
         if (len(row) != 8):
           continue 
         if row[0]:
           shapename = "@" + row[0]
         if row[6] and row[1]:
           typelines.add("@" + row[6]+"type" +"|rdf:type|"+ row[6]+ "\n")
           line = shapename + "|"+ row[1]+"|" + "@" + row[6]+"type" 
         else:
           line = shapename + "|" +row[1] + "|" + row[5]
         mand = row[3].lower()=="yes"
         repeat = row[4].lower() == "yes"
         if mand and repeat:
           line = line + "|+"
         elif mand and not repeat:
           line = line + "|1"
         elif not mand and repeat:
           line = line + "|*"
         elif not mand and not repeat:
           line = line + "|0,1"
         if row[7]:
           line = line + "|#" + row[7]
         data = data + line + "\n"
      if typelines: 
        data = data + "".join(typelines) + "\n"
      shexstatement = CSV.generate_shex_from_data_string(data)
    except Exception as e:
      print("Unable to parse. Error: " + str(e))
    return shexstatement
