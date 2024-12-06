from .FiinIndicator import FiinIndicator
from .Aggregates import IndexBars, TickerBars, CoveredWarrantBars, DerivativeBars
from .SubscribeCoveredWarrantEvents import SubscribeCoveredWarrantEvents
from .SubscribeIndexEvents import SubscribeIndexEvents
from .SubscribeTickerEvents import SubscribeTickerEvents
from .SubscribeTickerUpdate import SubscribeTickerUpdate
from .SubscribeDerivativeEvents import SubscribeDerivativeEvents
from datetime import datetime, timedelta
from typing import Union

class FiinSession:
    def __init__(self, username: str, password: str):...

    def login(self) -> FiinSession: ...
        
    def _is_valid_token(self) -> bool: ...
   
    def FiinIndicator(self) -> FiinIndicator: ...
    
    def IndexBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() + timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  limit: int = -1,
                  adj: bool = True) -> IndexBars:...
    
    def TickerBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() + timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  limit: int = -1,
                  adj: bool = True) -> TickerBars:...
    
    def DerivativeBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() + timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  limit: int = -1,
                  adj: bool = True) -> DerivativeBars:...
    
    def CoveredWarrantBars(self, tickers: str, by: str, 
                  from_date: Union [str, datetime] = datetime.now() + timedelta(days=30), 
                  to_date: Union [str, datetime] = datetime.now(), 
                  limit: int = -1,
                  adj: bool = True) -> CoveredWarrantBars:...
    
    def SubscribeDerivativeEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeDerivativeEvents: ...
    def SubscribeCoveredWarrantEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeCoveredWarrantEvents: ...
    def SubscribeTickerEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeTickerEvents: ...
    def SubscribeIndexEvents(self,
                            tickers: list, 
                            callback: callable) -> SubscribeIndexEvents: ...
    def SubscribeTickerUpdate(self,
                            access_token: str,
                            tickers: list, 
                            callback: callable,
                            by: str,
                            from_date: str,
                            wait_for_full_timeFrame: bool) -> SubscribeTickerUpdate: ...
    
    
