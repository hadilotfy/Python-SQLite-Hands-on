"""
sample_report module
--------------------------------
    a report for getting a sample from the dataset.

    Classes
        DatasetSampleReport: a child of ETLReport A.B.C.
            - takes additional sample_count initialization parameter.
        
"""

from .etl_report import ETLReport
import pandas as pd
class DatasetSampleReport(ETLReport):

    def __init__(self, description:str,sample_count:int):
        if not isinstance(sample_count, int):
            raise ValueError('Bad value for sample_count.')
        self._description = description
        self._result=pd.DataFrame()
        self._sample_count = sample_count

    @property
    def result_dataframe(self) -> pd.DataFrame:
        """Getter for result property."""
        in_pocket = len(self._result)
        total_need = self._sample_count
        if in_pocket == 0 :
            return pd.DataFrame()
        return self._result.sample(n=total_need,replace=(in_pocket < total_need),random_state=4)

    def accumelate_result(self,dataframe:pd.DataFrame) -> None:
        in_pocket = len(self._result)
        total_need = self._sample_count

        # return if you have what you need
        if in_pocket >= total_need:
            return

        # get current needed count
        current_need = total_need - in_pocket
        
        # get as much as you can
        sample = dataframe.sample(n=min(current_need,len(dataframe)),replace=False)

        # concat with interal result dataframe
        self._result = pd.concat([self._result,sample],ignore_index=True)