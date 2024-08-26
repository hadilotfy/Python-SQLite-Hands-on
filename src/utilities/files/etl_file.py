'''
Class ETL_FILE , Abstract Base Class

properties:
    _path: str , the string containing path to file.

methods:
    @abstractmethod
    read_from_filesystem_core() -> pd.DataFrame

    @abstractmethod
    write_to_filesystem_core(self,data:pd.DataFrame)
    
    read_from_filesystem(self) -> pd.DataFrame
        
    write_to_filesystem(self,data: pd.DataFrame) -> Tuple[bool, str]

'''



from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple,List
from .pathes import check_file


class etl_file(ABC):
    def __init__(self, path:str):
        self._path = path

    @property
    def path(self) -> str:
        return self._path
        
    @path.setter
    def path(self,path):
        self._path = path
        
    @abstractmethod
    def read_from_filesystem_core(self) -> pd.DataFrame:
        '''        
        method containing core read functionality implemented by child classes.

        args:
            None
        returns:
            pandas.DataFrame object containing read data.
        '''
        pass

    def read_from_filesystem(self) -> pd.DataFrame:
        """
        Read data from the file
        Wrapper method for read operation on an etl_file.
        args:
            None
        returns:
            pandas.DataFrame object containing read data.
        """
        # print(f'Reading data from file: {self._path}')
        rbool,rmsg = check_file(self._path,check_read=True,check_write=False)
        if not rbool:
            raise RuntimeError(f'Cannot get data from file: {self._path} , msg: {rmsg}')
        return self.read_from_filesystem_core()


    @abstractmethod
    def write_to_filesystem_core(self,data:pd.DataFrame):
        '''
        method containing core write functionality implemented by child classes.
        args:
            data: pandas.DataFrame, the data to write to filesystem.
        returns:
            None
        '''
        pass

    def write_to_filesystem(self,data: pd.DataFrame) -> Tuple[bool, str]:
        """
        Write data to the file
        Wrapper for write operation on filesystem.

        args:
            data: pandas.DataFrame, the data to write.
        returns:
            Tuple[bool,str]
                [0]: bool, whether the operation was successfull.
                [1]: str , msg to explain the status.
        """
        # print(f'Writing to : {self.path}')
        
        try:
            self.write_to_filesystem_core(data)
            # print(f"Data successfully written to : {self.path}")
            return True , 'Data was written'
        except ValueError as e:
            print(f"ValueError: {e}")
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while writing to JSON: {e}")

        return False , 'Data Writting Error.'

    @staticmethod
    def write_to_files(data : pd.DataFrame ,files:List['etl_file'],ignore_errors:bool):
        """"
        Write a DataFrame to muliple etl_file instances.
        args:
            data: a Pandas DataFrame containing data to write.
            files: a list of etl_file instances.
        """
        for file in files :
            rbool,rmsg = file.write_to_filesystem(data=data)
            if not ignore_errors and not rbool:
                print(f'Error when writing to file:{file.path} , error: {rmsg} , exiting...')
                exit(1)
    
