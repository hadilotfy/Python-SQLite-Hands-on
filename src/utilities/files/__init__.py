'''
files package
-------------

Handle Files and Pathes work for input and output data files

Modules:
    
    pathes          : filesystems inquiry and checking permissions
    etl_file        : ETLFile class
        csv_file    : CSVFile class
        json_file   : JSONFile class
    etl_file_map    : ETL_FILES_TYPE_MAPPING dict and get_etl_file_class func.

Classes:
    ETLFile: Abstract Base Class for file classes in this module.
    CSVFile: Child of ETLFile which handles 'csv' file operations.
    JSONFile: Child of ETLFile which handles 'json' files opertations.

Dictionary:
    ETL_FILES_TYPE_MAPPING:
        mapping from typecodes (eg. 'json') to file class names (eg. JSONFile).

Functions:
    get_etl_file_class(typename)-> Tuple[bool,type]:
        returns True and class name corresponding to some type code if the
        type code is valid. and (False, None ) if the type code is invalid.

'''
from .etl_file import ETLFile
from .etl_file_map import ETL_FILES_TYPE_MAPPING,get_etl_file_class
from .json_file import JSONFile
from .csv_file import CSVFile