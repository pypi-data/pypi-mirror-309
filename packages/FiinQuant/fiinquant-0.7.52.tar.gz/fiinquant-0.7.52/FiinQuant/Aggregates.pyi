import pandas as pd
from typing import Union
from datetime import datetime

class Bar:
    def __init__(self, 
                 access_token: str, 
                 tickers: Union [str, list],  
                 by: str,  
                 from_date: Union [str, datetime],  
                 to_date: Union [str, datetime],  
                 multiplier: int = 1,  
                 limit: int = -1,
                 adj: bool = True) -> None:...

    def get(self, data_type: str) -> BarData: ...

class BarData:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Open: pd.Series
        self.Low: pd.Series
        self.High: pd.Series
        self.Close: pd.Series
        self.Volume: pd.Series
        self.Timestamp: pd.Series
        self.BU: pd.Series
        self.SD: pd.Series

    def to_dataFrame(self) -> pd.DataFrame: ...

class BarDataUpdate:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Ticker: str
        self.Open: pd.Series
        self.Low: pd.Series
        self.High: pd.Series
        self.Close: pd.Series
        self.Volume: pd.Series
        self.Timestamp: pd.Series
        self.BU: pd.Series
        self.SD: pd.Series

    def to_dataFrame(self) -> pd.DataFrame: ...

class IndexBars(Bar) : 
    def get(self) -> BarData: ...

class TickerBars(Bar):
    def get(self) -> BarData: ...

class CoveredWarrantBars(Bar):
    def get(self) -> BarData: ...
    
class DerivativeBars(Bar):
    def get(self) -> BarData: ...



