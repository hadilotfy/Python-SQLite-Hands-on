'''
Module: pathes

Module to deal with path checks which include existence of pathes, whether is a file
, whether is a directory and whether have read or write permissions or both. 


Methods:
    check_path(path:str) -> Tuple[bool,str]
    check_directory(path: str,check_read:bool,check_write:bool)-> Tuple[bool,str]
    check_file(path: str,check_read:bool,check_write:bool)-> Tuple[bool,str]
    
'''
import os
from typing import Tuple


def check_path(path:str) -> Tuple[bool,str]:
    """ 
        Check if path is a valid path.

        args:
            path : str , the path to a file or a directory

        retruns:
            Tuple[bool,str]
                [0]: bool, whether the path is valid.
                [1]: str , msg to explain the status.
    """
    try:
        if os.path.exists(path):
            return True , 'Valid path.'
        else:
            return False, f'Path {path} does not exist.'
    except Exception as e:
        return False , f"Error reading path: {path}, the error: {e}"

def check_directory(path: str,check_read:bool,check_write:bool)-> Tuple[bool,str]:
    '''
        Check dir path: if path exist, if is a dir, if can read and if can write

        args:
            path: str , the path to check.
            check_read: bool, whether to check for read permissions
            check_write: bool, whether to check for write permissions
        
        returns:
            Tuple[bool,str]
                [0]: bool, whether the path passed the checks.
                [1]: str , msg to explain the status.
    '''
    
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


def check_file(path: str,check_read:bool,check_write:bool)-> Tuple[bool,str]:
    '''
        Check file path: if path exist, if is a file, if can read and if can write

        args:
            path: str , the path to check.
            check_read: bool, whether to check for read permissions
            check_write: bool, whether to check for write permissions
        
        returns:
            Tuple[bool,str]
                [0]: bool, whether the path passed the checks.
                [1]: str , msg to explain the status.
    '''
    
    is_valid_path,rmsg = check_path(path)
    if not is_valid_path:
        return is_valid_path,rmsg

    if not os.path.isfile(path):
        return False , f'Not a file: {path}.'
    
    if check_read and not (os.access(path, os.R_OK)):
        return False , f'No read permission on file:{path}.'

    if check_write and not (os.access(path, os.W_OK)):
        return False , f'No write permission on file:{path}.'

    return True , 'Valid file.'
