#!/usr/bin/env python3

"""
script.py

Description:
    This is my main script for the simple ETL utility.
    It creates a SQLite DB and put some data in, reads the data and dump them in CSV/JSON files, then reads one 
    of the files and generate a report based on its data.

Dependencies:
    - pandas  : library used to hold data with its metadata and interaction with many sources and destinations.

Python Internal Dependencies:
    - os.path   : library used to interact with filesystems and read file permissions.
    - argparse  : library used to handly command line options parsing and help menu construction.
    - sqlite3   : library for connecting to SQLite DB files and performing DB operations on them.

Usage:
    python script.py [options]
    script.py [options]

Options:
    run  `script.py --help` for details
    and see get_args() docs.

Examples:
    script.py --input-db-file 'samble.db' --output json data.json --output csv data.csv --out-report report.out 
    script.py --report-visible
"""





from utilities import *
from utilities import ETL_FILES_TYPE_MAPPING
import pandas as pd
import argparse
import os
from typing import List


# Defualt files to read from and write to
RESOURCES_PATH='resources'                            # default resources directory
DEFAULT_DB_PATH=RESOURCES_PATH+'/'+'sample.db'        # default DB file path
DEFAULT_REPORT_PATH=RESOURCES_PATH+'/'+'report.txt'   # defualt output report path
DEFAULT_REPORT_SCREEN_PRINTING=True                   # default behviour for report visibiliy on screen
DEFAULT_OUT_PATH=RESOURCES_PATH+'/'+'data.out'        # defualt data output path
DEFAULT_OUT_TYPE='json'                               # defualt data output type

def get_args():    
    """
    Parses command-line arguments for the script.

    This function uses the `argparse` module to handle command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.

    Arguments:
        --input-db-file (str): Path to the input SQLite database file. Defaults to `DEFAULT_DB_PATH` if not specified.
        --output (list of tuples): Output type and path. Example: --output csv output.csv. Defaults to [['json', DEFAULT_JSON_OUT_PATH]] if not specified.
        --out-report (str): Path to the report output file. Defaults to `DEFAULT_REPORT_PATH` if not specified.
        --report-visible (bool): If true, prints the dataset report on the screen. Defaults to `DEFAULT_REPORT_SCREEN_PRINTING`.

    Notes:
        - Only the last occurrence of an option will be used if passed multiple times.
        - Creates the resources directory if it does not exist.
    """

    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.description='only last occurence of an options will be used if passed muliple times.'
    # Add arguments
    parser.add_argument('--input-db-file' , type=str, default=DEFAULT_DB_PATH, help=f"Input SQLite DB file. If not defined then use default: {DEFAULT_DB_PATH}")
    parser.add_argument('--output',nargs=2,
                         action='append',
                         type=str,
                         metavar=('TYPE', 'PATH'),
                         help=f"Specify output type and path. Availabe types are {list(ETL_FILES_TYPE_MAPPING.keys())}. Example: --output csv out.csv")
    parser.add_argument('--out-report'    , type=str, default=DEFAULT_REPORT_PATH, help=f"Report output file. If not defined then use default: {DEFAULT_REPORT_PATH}")
    parser.add_argument('--report-visible', action='store_true',default=DEFAULT_REPORT_SCREEN_PRINTING, help=f'Print dataset report on the screen. If not defined then use default: DEFAULT_REPORT_SCREEN_PRINTING')

    # get passed arguments
    args = parser.parse_args()

    # If no --output was provided, use default value
    if args.output is None:
        args.output = [[DEFAULT_OUT_TYPE, DEFAULT_OUT_PATH]]
        
    # make default resources dirctory
    if not os.path.exists(RESOURCES_PATH):
        os.makedirs(RESOURCES_PATH)

    return args

 

def get_files_objects(args_output) -> List[etl_file]:
    ''' 
    Process output argument inputs to get corresponding file objects.
    args:
        arg_output: List[(str,str),...] : a list of tuple each with two
            values, output_type and output_path. those values are passed
            as arguments to --output options.
    returns:
        a list of etl_file objects.
    erros:
        this function stops the script if one type is invailde.
    '''
    files = []  # result list
    # loop on input list
    for output_type, output_path in args_output: 
        is_valid , cls = get_etl_file_class(typename=output_type)
        if is_valid:
            files.append(cls(output_path)) # initialize an etl_file instance and add to list.
            continue
        else:
            print(f"Unknown TYPE passed to --output TYPE PATH : {output_type}, exiting...")
            exit()
    return files
            
def main():
    """
    Main function and entry point for this script.
    """
    # get passed args.
    args = get_args()

    # Initialize variables
    input_db_file = args.input_db_file              # db file path
    output_files = get_files_objects(args.output)   # etl_file instances
    report_output_file=args.out_report              # report file path
    is_print_report_to_screen = args.report_visible # print report to screen ?

    # create and initialize db if it does not exist.
    if not os.path.isfile(input_db_file):
        create_sample_db(input_db_file)
    
    # read data from database.
    data = read_from_database(input_db_file)

    # export data to files.
    etl_file.write_to_files(data,output_files,ignore_errors=True)
    
    data = None #  make 'data' availble for garbage collector.

    # read data from first file (from first --output option.
    # or from the defualt file when no --output option was passed.)
    new_data = output_files[0].read_from_filesystem()
    
    # generate report
    generate_report_wrapper(new_data,report_output_file,is_print_report_to_screen)


if __name__ == "__main__":
    main()