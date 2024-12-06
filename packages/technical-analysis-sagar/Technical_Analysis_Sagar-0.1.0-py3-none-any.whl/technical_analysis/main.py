from .ta_calculation import calculation


class TA_Calculation(object):
    symbol = ""
    interval = ""

    def __init__(self, symbol="", interval=""):
        """Create an instance of TA_Calculation class

        Args:
            symbol (str, required): Abbreviation of a stock or currency (see documentation and tradingview's site).
            interval (str, optional): See the interval class and the documentation. Defaults to 1 day.
        """
        self.symbol = symbol
        self.interval = interval

    def technical_analysis(self):
        """Get technical analysis data

        Returns:
            dict: Technical analysis data
        """
        return calculation(self.symbol, self.interval)

       