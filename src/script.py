#!/usr/bin/env python3

"""
script.py

Description:
    This is the main script for a simple ETL utility.
    It creates a SQLite DB and put some data in, reads the data and dump them in CSV/JSON files, then reads one 
    of the files and generate a report based on its data.

Features:
    SQLite DB
    Moduler Structure and OOP features utilization
    Memory Efficient (Read and process data in chunks)
    Reports Customization
    Packaging Ready (setup.py)

Dependencies:
    - pandas  : library used to hold data with its metadata and interaction with many sources and destinations.
    - tabulate: library for tidy console printing.

Python Internal Dependencies:
    - os.path       : enqire filesystems and read file permissions.
    - argparse      : handle command line options parsing and help menu construction.
    - sqlite3       : connecting to SQLite DB files and performing DB operations on them.
    - typing        : support for type hints and type checking.
    - ABC           : for abstract classes and abstract methods.
    - collections   : use some data structures

Usage:
    python script.py [options] [--help]             # use in powershell
    script.py [options] [--help]                    
    hadi-etl-script.exe [options] [--help]          # this one after installation.

Options:
    run `script.py --help` for details
    and see get_args() docs.

Examples:
   >python script.py --input-db-file 'samble.db' --output json data.json --output csv data.csv --out-report report.out 
   >python script.py --report-visible
"""

#################################################################################


from utilities import *
from utilities import reports
from utilities import files as fs
from utilities.reports import ETLReport

import pandas as pd
import argparse
import os
from typing import List

#################################################################################
CHUNK_SIZE = 5
# Defualt files to read from and write to
RESOURCES_PATH='resources'                            # default resources directory
DEFAULT_DB_PATH=RESOURCES_PATH+'/'+'sample.db'        # default DB file path
DEFAULT_REPORT_PATH=RESOURCES_PATH+'/'+'report.txt'   # defualt output report path
DEFAULT_REPORT_SCREEN_PRINTING=False                  # default behviour for report visibiliy on screen
DEFAULT_JSON_OUT_PATH=RESOURCES_PATH+'/'+'data.json'  # defualt json data output path
DEFAULT_CSV_OUT_PATH=RESOURCES_PATH+'/'+'data.csv'    # defualt json data output path
# DEFAULT_OUT_PATH=RESOURCES_PATH+'/'+'data.out'        # defualt json data output path
# DEFAULT_OUT_TYPE='json'                               # defualt json data output type


#################################################################################
def get_args():    
    """
    Parses command-line arguments for the script.

    This function uses the `argparse` module to handle command-line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.

    Arguments:
        --input-db-file (str)
            Path to the input SQLite database file.
            Defaults to `DEFAULT_DB_PATH` if not specified.
        --output (list of tuples)
            Output type and path. 
            Example: --output csv output.csv. 
            Defaults to [['json', DEFAULT_JSON_OUT_PATH]] if not specified.
        --out-report (str)
            Path to the report output file. 
            Defaults to `DEFAULT_REPORT_PATH` if not specified.
        --report-visible (bool)
            If true, prints the dataset report on the screen. 
            Defaults to `DEFAULT_REPORT_SCREEN_PRINTING`.

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
                         help=f"Specify output type and path. Availabe types are {list(fs.ETL_FILES_TYPE_MAPPING.keys())}. Example: --output csv out.csv")
    parser.add_argument('--out-report'    , type=str, default=DEFAULT_REPORT_PATH, help=f"Report output file. If not defined then use default: {DEFAULT_REPORT_PATH}")
    parser.add_argument('--report-visible', action='store_true',default=DEFAULT_REPORT_SCREEN_PRINTING, help=f'Print dataset report on the screen. If not defined then use default: {DEFAULT_REPORT_SCREEN_PRINTING}')

    # get passed arguments
    args = parser.parse_args()

    # Defualt Output Files (data.csv , data.json)
    # If no --output was provided
    if args.output is None:
        args.output = [
            ['csv' ,DEFAULT_CSV_OUT_PATH],
            ['json' ,DEFAULT_JSON_OUT_PATH],
            # [DEFAULT_OUT_TYPE,DEFAULT_OUT_PATH]
        ]
        
    # make default resources dirctory
    if not os.path.exists(RESOURCES_PATH):
        os.makedirs(RESOURCES_PATH)

    return args

def get_files_objects(args_output) -> List[fs.ETLFile]:
    ''' 
    Process output argument inputs to get corresponding file objects.
    args:
        arg_output: List[(str,str),...] : a list of tuple each with two
            values, TYPE and PATH. those values are passed
            as arguments to --output options.
    returns:
        a list of ETLFile objects.
    erros:
        this function stops the script if one type is invailde.
    '''
    files = []  # result list
    # loop on input list
    for output_type, output_path in args_output: 
        is_valid , cls = fs.get_etl_file_class(typename=output_type)
        if is_valid:
            files.append(cls(output_path)) # initialize an ETLFile instance and add to list.
            continue
        else:
            print(f"Unknown TYPE passed to --output TYPE PATH : {output_type}, exiting...")
            exit()
    return files

#################################################################################    
def main():
    """
    Main function and entry point for this script.
    """
    # get passed args.
    args = get_args()

    # Initialize variables
    input_db_file = args.input_db_file              # db file path
    output_files = get_files_objects(args.output)   # ETLFile instances
    report_output_file=args.out_report              # report file path
    is_print_report_to_screen = args.report_visible # print report to screen ?

    # create and initialize db if it does not exist.
    if not os.path.isfile(input_db_file):
        create_sample_db(input_db_file)

    # first pipeline: read from db and put in files.
    with etl_db_conn(input_db_file) as db_conn:
    
        # read data from database.
        data_chunks = read_from_database(db_conn,chunksize=CHUNK_SIZE)

        
        # export data to files.
        ### this will loop the chunks to write to files simultinously.      # Done not tested
        if(CHUNK_SIZE is None):
            fs.ETLFile.write_single_dataframe_to_files(data_chunks,output_files,ignore_errors=True,overwrite=True)
        else:
            fs.ETLFile.write_muliple_dataframes_to_files(data_chunks,output_files,ignore_errors=True,overwrite=True)

        #  make 'data' availble for garbage collector.
        del(data_chunks)
        

    # second pipeline: read from files and generate a report.
    # read data from first file (from first (--output TYPE PATH) argument.)
    # or from the defualt file when no (--output TYPE PATH) argument is passed.)
    data_chunks = output_files[0].read_from_filesystem(chunksize=CHUNK_SIZE)
    

    # generate report
    # get reports instances
    reports_arr = reports.define_reports()
    # calculate reports data
    ETLReport.calculate_reports(reports=reports_arr,data=data_chunks)
    # print reports
    reports.print_reports_wrapper(   reports=reports_arr,
                            report_output_file=report_output_file,
                            is_print_report_to_screen=is_print_report_to_screen
                        )


if __name__ == "__main__":
    main()