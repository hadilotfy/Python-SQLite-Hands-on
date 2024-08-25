    
import pandas as pd
import os
def write_to_csv (data , output_csv_file):
    """Write data to a CSV file"""
    # print('Writing data to CSV file with headers.')
    data.to_csv(output_csv_file, sep=',', header=True, index=False) # index=True
    return True , 'Data Written.'

def write_to_json(data: pd.DataFrame, output_json_file: str):
    """Write data to a JSON file"""
    # print('Writing data to JSON file.')
    data.to_json(output_json_file, orient='records', lines=True)
    return True , 'Data Written.'
    
def read_from_csv(input_csv_file: str):
    """Read data from a CSV file"""
    # print('Reading data from CSV file.')
    rbool,rmsg = check_file(input_csv_file,check_read=True,check_write=False)
    if not rbool:
        return rbool , rmsg ,None
    return True , 'Data returned.' ,  pd.read_csv(input_csv_file, delimiter=',') # index_col='id'


def read_from_json(input_json_file:str):
    """Read data from a JSON file"""
    # print('Reading data from JSON file.')
    rbool,rmsg = check_file(input_json_file,check_read=True,check_write=False)
    if not rbool:
        return rbool , rmsg ,None
    return True , 'Data returned.' ,  pd.read_json(input_json_file,lines=True) 


def check_path(path: str):
    if not isinstance(path, str):
        raise ValueError("The path should be a string.")
    
    try:
        if os.path.exists(path):
            return True , 'Valid path.'
        else:
            return False, f'Path {path} does not exist.'
    # except PermissionError:
    #     print(f"Permission denied: Unable to access '{path}'.")
    # except OSError as e:
    #     print(f"OS error occurred: {e}")
    except Exception as e:
        return False , f"Error reading path: {path}, the error: {e}"

def check_directory(path: str,check_read:bool,check_write:bool):
    rbool,rmsg = check_path(path)
    if not rbool:
        return rbool,rmsg

    if not os.path.isdir(path):
        return False , f'Not a directory: {path}.'
    
    if check_read and not (os.access(path, os.R_OK)):
        return False , f'No read permission on dir:{path}.'

    if check_write and not (os.access(path, os.W_OK)):
        return False , f'No write permission on dir:{path}.'

    return True , 'Valid dir.'


def check_file(path: str,check_read:bool,check_write:bool):
    rbool,rmsg = check_path(path)
    if not rbool:
        return rbool,rmsg

    if not os.path.isfile(path):
        return False , f'Not a file: {path}.'
    
    if check_read and not (os.access(path, os.R_OK)):
        return False , f'No read permission on file:{path}.'

    if check_write and not (os.access(path, os.W_OK)):
        return False , f'No write permission on file:{path}.'

    return True , 'Valid file.'
