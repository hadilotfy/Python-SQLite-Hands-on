'''
Class CSV_File is a child class of ETLFile,

implements two abstract functions:
    write_to_filesystem_core
    read_from_filesystem_core

    see ETLFile for description of each.
'''


import pandas as pd
from .etl_file import ETLFile
from typing import Optional,Union,Iterable


class CSVFile(ETLFile):

    def write_to_filesystem_core(self, data: pd.DataFrame, overwrite: bool):
        if overwrite:
            # print headers and data
            data.to_csv(self._path, sep=',', header=True, index=False)
        else:
            # append data only.
            data.to_csv(self._path, sep=',', mode='a', header=False, index=False)

    def read_from_filesystem_core(self,chunksize:Optional[int]=None) -> Union[pd.DataFrame,Iterable[pd.DataFrame]]:
        # if chunksize is None/0 ----> returns a DataFrame
        # and if chunksize > 0   ----> returns Iterable[pd.DataFrame]
        if not (chunksize > 0):
            chunksize = None
        return pd.read_csv(self._path, delimiter=',',chunksize=chunksize)
    
