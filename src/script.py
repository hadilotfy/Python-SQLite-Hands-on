#!/usr/bin/env python3

# Script Usage Description
#=============================
# usage: script.py [-h] [--input-db-file INPUT_DB_FILE] [--output-json OUTPUT_JSON]
#                  [--output-csv OUTPUT_CSV] [--out-report OUT_REPORT]
#                  [--report-visible]

# only last occurence of an options will be used if passed muliple times.

# optional arguments:
#   -h, --help            show this help message and exit
#   --input-db-file INPUT_DB_FILE
#                         input SQLite database file.
#   --output-json OUTPUT_JSON
#                         output JSON file.
#   --output-csv OUTPUT_CSV
#                         output CSV file.
#   --out-report OUT_REPORT
#                         report output file.
#   --report-visible      print dataset report on the screen.

#     if no input_db_file ?
#         then create and use 'sample.db'
#     if one output option is define ?
#         use the provided output option only.
#     if no output option ?
#         output to 'output.csv' and 'output.json' files.
#     if multiple output options ?
#         output to all files.

RESOURCES_PATH='resources'
DEFAULT_DB_PATH=RESOURCES_PATH+'/'+'sample.db'
DEFAULT_REPORT_PATH=RESOURCES_PATH+'/'+'report.txt'
DEFAULT_JSON_OUT_PATH=RESOURCES_PATH+'/'+'data.json'
DEFAULT_CSV_OUT_PATH=RESOURCES_PATH+'/'+'data.csv'
DEFAULT_REPORT_SCREEN_PRINTING=False

# x
import argparse
import os
def get_args():
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.description='only last occurence of an options will be used if passed muliple times.'
    # Add arguments
    parser.add_argument('--input-db-file' , type=str, default=DEFAULT_DB_PATH, help=f"input SQLite db file. If not defined then use default: {DEFAULT_DB_PATH}")
    parser.add_argument('--output-json'   , type=str, help="output JSON file.")
    parser.add_argument('--output-csv'    , type=str, help="output CSV file.")
    parser.add_argument('--out-report'    , type=str, default=DEFAULT_REPORT_PATH, help=f"report output file. If not defined then use default: {DEFAULT_REPORT_PATH}")
    parser.add_argument('--report-visible', action='store_true',default=DEFAULT_REPORT_SCREEN_PRINTING, help=f'print dataset report on the screen. If not defined then use default: DEFAULT_REPORT_SCREEN_PRINTING')

    # get passed arguments
    args = parser.parse_args()

    # if no data-output-file passed then output to default files.
    if not args.output_json and not args.output_csv:
        args.output_json = DEFAULT_JSON_OUT_PATH
        args.output_csv = DEFAULT_CSV_OUT_PATH
    
    # make default resources dirctory
    if not os.path.exists(RESOURCES_PATH):
        os.makedirs(RESOURCES_PATH)

    return args

def read_from_files(input_csv_file,input_json_file):
    jrbool,jrmsg,jdata = read_from_json(input_json_file)
    crbool,crmsg,cdata = read_from_csv(input_csv_file)
    if jrbool:
        return jdata
    elif crbool:
        return cdata
    else:
        print('Error: No data returned,')
        print(f'    csv error msg: {crmsg}.')
        print(f'    json error msg: {jrmsg}.')
        exit()

from utilities import *
def main():
    # get passed args.
    args = get_args()

    input_db_file  = args.input_db_file
    output_json_file = args.output_json
    output_csv_file = args.output_csv
    report_output_file=args.out_report
    is_print_report_to_screen = args.report_visible

    # create db if it does not exist.
    # if not os.path.exists(input_db_file) :
    create_sample_db(input_db_file)
    
    # read data from database.
    data = read_from_database(input_db_file)


    # export data to files.
    write_to_csv (data , output_csv_file)
    write_to_json(data , output_json_file)

    data = None #  make 'data' availble for garbage collector.

    # read data from files
    new_data = read_from_files(output_csv_file,output_json_file)
    
    # generate report
    # where to print report? to_screen, tofile or to both
    generate_report_wrapper(new_data,report_output_file,is_print_report_to_screen)


if __name__ == "__main__":
    main()