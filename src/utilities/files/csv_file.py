'''
Class csv_file is a child class of etl_file,

must implement two functions:
    write_to_filesystem_core
    read_from_filesystem_core

    see etl_file for description of each.
'''


import pandas as pd
from .etl_file import etl_file



class csv_file(etl_file):

    def write_to_filesystem_core(self, data: pd.DataFrame):
        data.to_csv(self._path, sep=',', header=True, index=False) # index=True

    def read_from_filesystem_core(self) -> pd.DataFrame:
        return pd.read_csv(self._path, delimiter=',') # index_col='id'
    