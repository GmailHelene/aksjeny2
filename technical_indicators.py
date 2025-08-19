import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Try to import TA-Lib, fallback to pandas-ta
try:
    import talib
    HAS_TALIB = True
    logger.info("TA-Lib successfully imported")
except ImportError:
    HAS_TALIB = False
    try:
        import pandas_ta as ta
        HAS_PANDAS_TA = True
        logger.info("pandas-ta successfully imported as fallback")
    except ImportError:
        HAS_PANDAS_TA = False
        logger.warning("Neither TA-Lib nor pandas-ta is available. Technical indicators will not work.")

class TechnicalIndicatorsService:
    def __init__(self):
        if not HAS_TALIB and not HAS_PANDAS_TA:
            raise ImportError("Neither TA-Lib nor pandas-ta is available.")

    def sma(self, series: pd.Series, length: int = 14) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA).
        """
        if HAS_TALIB:
            return pd.Series(talib.SMA(series.values, timeperiod=length), index=series.index)
        elif HAS_PANDAS_TA:
            return ta.sma(series, length=length)
        else:
            raise RuntimeError("No technical analysis library available.")