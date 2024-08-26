"""
records_count_report module
--------------------------------
    a report for count of records in the dataset.

    Classes
        RecordsCountReport: a child of ETLReport A.B.C.
        
"""


from .etl_report import ETLReport
import pandas as pd
class RecordsCountReport(ETLReport):

    def __init__(self, description:str):
        self._description = description
        self._result=0

    @property
    def result_dataframe(self) -> pd.DataFrame:
        """A Getter for result property."""
        return pd.DataFrame({
            'Count': [self._result],
        })

    def accumelate_result(self,dataframe:pd.DataFrame) -> None:
        self._result += len(dataframe)

