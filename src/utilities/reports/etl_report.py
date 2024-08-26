"""
etl_report module
-----------------

    one class:
        ETLReport Abstract Base Class
    
    and one static method:
        ETLReport.calculate_reports()

"""

from abc import abstractmethod
from abc import ABC
import pandas as pd
from ..dualstream import DualStream
import pandas as pd
from typing import Union # , Iterable
from collections.abc import Iterable
from tabulate import tabulate

class ETLReport(ABC):

    def __init__(self, description:str , initial_value):
        self._description = description
        self._result=initial_value

    @abstractmethod
    def accumelate_result(self,dataframe:pd.DataFrame) -> None:
        pass

    @property
    @abstractmethod
    def result_dataframe(self) -> pd.DataFrame:
        """Getter for result property."""
        pass
    
    @property
    def description(self):
        """Getter for description property."""
        return self._description

    
    def print_report(self) -> None:
        df = self.result_dataframe
        # Convert the DataFrame to a format compatible with tabulate
        # Convert DataFrame to a list of lists including headers
        data = [df.columns.tolist()] + df.values.tolist()

        # Print the DataFrame using tabulate
        print(f'Report Description: {self._description}')
        print(tabulate(data, headers='firstrow', tablefmt='grid'))
        
    @staticmethod
    def calculate_reports(data:Union[pd.DataFrame,Iterable[pd.DataFrame]],reports:list['ETLReport']):
        data_arr = data
        if isinstance(data,pd.DataFrame):
            data_arr = [data]

        for df in data_arr:
            if not df.empty:
                for report in reports:
                    try:
                        report.accumelate_result(df)
                    except Exception as e:
                        print(f'Error when calculating reports , error:{e}')
