#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import argparse
from shexstatements.shexfromcsv import CSV

parser = argparse.ArgumentParser(prog='shexstatements')
parser.add_argument('-o','--output', type=str, help='output file')
parser.add_argument('-','--delimiter', type=str, help='output file')
parser.add_argument('csvfile', type=str, help='path of CSV file')

args = parser.parse_args()
if args.delimiter:
  shexstatement = CSV.generate_shex_from_csv(args.csvfile, delim=args.delimiter)
else:
  shexstatement = CSV.generate_shex_from_csv(args.csvfile)
  
if args.output:
  with open(args.output, 'w') as shexfile:
    shexfile.write(shexstatement)
else:
  print(shexstatement)
