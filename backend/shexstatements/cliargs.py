#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import argparse
from shexstatements.shexfromcsv import CSV
from shexstatements.shexjfromcsv import ShExJCSV
from shexstatements.shexfromspreadsheet import Spreadsheet
from shexstatements.shexfromapplprofilecsv import ApplicationProfile
import shexstatements.application
from os.path import splitext
import setuptools
import runpy


def handle_cli_arguments(arguments):
    parser = argparse.ArgumentParser(prog='shexstatements')
    parser.add_argument('-o', '--output', type=str, help='output file')
    parser.add_argument('-ap', '--applicationprofile',
                        action='store_true', help='input is application profile')
    parser.add_argument('-d', '--delimiter', type=str, help='output file')
    parser.add_argument('-s', '--skipheader',
                        action='store_true', help='Skip CSV header')
    parser.add_argument('-j', '--shexj', action='store_true',
                        help='Generate ShExJ')
    parser.add_argument('-r', '--run', action='store_true',
                        help='run web application')
    parser.add_argument('-v', '--version', action='store_true',
                        help='get version of shexstatements')
    parser.add_argument('csvfile', nargs="*", type=str,
                        help='path of CSV file')
    skipheader = False
    delimiter = ","

    args = parser.parse_args(args=arguments[1:])
    if args.version:
        version_meta = runpy.run_path("./shexstatements/version.py")
        version = version_meta["__version__"]
        print("shexstatements " + version)
        return
    if args.run:
        shexstatements.application.run()
    else:
        if len(args.csvfile) < 1:
            print("CSV file missing")
            parser.print_usage()
            return
        for csvfile in args.csvfile:
            if args.skipheader:
                skipheader = args.skipheader
            if args.delimiter:
                delimiter = args.delimiter

            if args.applicationprofile:
                shexstatement = ApplicationProfile.generate_shex_from_csv(
                    csvfile, delim=delimiter, skip_header=skipheader)
                if args.shexj:
                    shexstatement = ShExJCSV.generate_shexj_from_shexstament(
                        shexstatement)
            else:
                filename, file_extension = splitext(csvfile)
                if ".csv" == file_extension.lower():
                    if args.shexj:
                        shexstatement = ShExJCSV.generate_shexj_from_csv(
                            csvfile, delim=delimiter, skip_header=skipheader)
                    else:
                        shexstatement = CSV.generate_shex_from_csv(
                            csvfile, delim=delimiter, skip_header=skipheader)
                else:
                    shexstatement = Spreadsheet.generate_shex_from_spreadsheet(
                        filepath=csvfile)

            if args.output:
                with open(args.output, 'w') as shexfile:
                    shexfile.write(shexstatement)
            else:
                print(shexstatement)
