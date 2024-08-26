'''
1. A dictionary which maps from an etl_file child class to a string representation
that is used for user input to dynamically select the appropriate class for file work.

2. A function to get class corresponding to some type.
    get_etl_file_class(typename)-> Tuple[bool,type]


each etl_file have a pair of key (the user-friendly name) and a value (the class name).

this module appears in two other files, 
    src/script.py       the main body for the script
    src/utilities/__init__.py

keys are shown in help menu so the user can know which types are acceptable.

'''


from .csv_file import csv_file
from .json_file import json_file

ETL_FILES_TYPE_MAPPING = {
    'json': json_file,
    'csv':csv_file
}

from typing import Tuple
def get_etl_file_class(typename)-> Tuple[bool,type] :
    '''
    Check if a file type is supported by this script
    args:
        typename: str , the type to use with --output option.
    returns:
        Tuple[bool,str]
            [0]: bool, whether the type is valid.
            [1]: type, the class if name is valid.

    '''
    cls = ETL_FILES_TYPE_MAPPING[typename]
    return (cls is not None) , cls 
 