'''
Class CSV_File is a child class of ETLFile,

implements two abstract functions:
    write_to_filesystem_core
    read_from_filesystem_core

    see ETLFile for description of each.
'''


import pandas as pd
from .etl_file import ETLFile
from typing import Optional,Iterable,Union

class JSONFile(ETLFile):

    def write_to_filesystem_core(self, data: pd.DataFrame , overwrite : bool):
        if overwrite:
            data.to_json(self._path, orient='records', lines=True)
        else :
            # Ensure the data is in JSON lines format
            json_lines = data.to_json(orient='records', lines=True)
            
            # Append the JSON lines to the file
            with open(self._path, 'a') as file:
                file.write(json_lines + '\n')

    def read_from_filesystem_core(self,chunksize:Optional[int]=None) -> Union[pd.DataFrame,Iterable[pd.DataFrame]]:
        return pd.read_json(self._path,lines=True,chunksize=chunksize)
    