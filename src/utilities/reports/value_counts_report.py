"""
sample_report module
--------------------------------
    a report for getting a sample from the dataset.

    Classes
        ValuesCountsReport: a child of ETLReport A.B.C.
            - takes additional initialization parameter:
                - column_name
                - preprocessing_func
                - top_counts
"""

from .etl_report import ETLReport
import pandas as pd
from collections import defaultdict

class ValuesCountsReport(ETLReport):

    def __init__(self, description:str,column_name:str,preprocessing_func: callable=None,top_count:int=0):
        # check if column name is a str.
        if not isinstance(column_name, str):
            raise ValueError('Bad value for column_name.')


        # Check if preprocessing_func is None or not a callable
        if preprocessing_func is None:
            preprocessing_func = lambda x: x
        elif not callable(preprocessing_func):
            raise ValueError("preprocessing_func must be a function or callable")

        if (top_count > 0):
            description = description + f' - Top {top_count} plus ties'

        self._description = description
        
        self._result=defaultdict(int)
        self._column_name = column_name
        self._top_n = top_count
        self._func = preprocessing_func



    @property
    def result_dataframe(self) -> pd.DataFrame:
        """Getter for result property."""
        # Convert to a pandas DataFrame
        return self.get_top_frequent_values(count=self._top_n)


    def accumelate_result(self,dataframe:pd.DataFrame) -> None:
        try:
            counts = dataframe[self._column_name].dropna().apply(func=self._func).value_counts(dropna=True)
        except KeyError as e:
            print(f"KeyError: value_counts_report , column_name:{self._column_name} error:{e}")
            return
        for value, count in counts.items():
            self._result [value] += count
    
    def get_top_frequent_values(self,count : int):
        # Convert the defaultdict to a DataFrame
        df = pd.DataFrame(list(self._result.items()), columns=['Key', 'Count'])

        if count > 0 and len(df) > 0 :
            # Get the top <count> most frequent keys, 
            # but print ties even if more than count
            top_n = df.nlargest(count, 'Count',keep='all')
            return top_n
        else:
            return df