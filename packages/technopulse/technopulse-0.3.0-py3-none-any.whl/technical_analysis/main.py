from .ta_calculation import calculation


class TA_Calculation(object):
    symbol = ""
    interval = ""

    def __init__(self, symbol="", interval="", data=None):
        """Create an instance of TA_Calculation class

        Args:
            symbol (str, required): Abbreviation of a stock or currency (see documentation and tradingview's site).
            interval (str, optional): See the interval class and the documentation. Defaults to 1 day.
        """
        self.symbol = symbol
        self.interval = interval
        self.data = data

    def technical_analysis(self):
        """Get technical analysis data

        Returns:
            dict: Technical analysis data
        """
        intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d"]
        if self.interval not in intervals:
            return {"error":"Interval {self.interval} is not supported. Supported intervals are {intervals}"}

        
        return calculation(self.symbol, self.interval, self.data)

       