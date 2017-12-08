from src.Engine.FreqFilters import BandFilters

class Factory:
    def __init__(self):
        self.butterFilter: BandFilters.ButterWorthFilter = None
        
    def getButterworthFilter(self):
        if self.butterFilter is not None:
            return self.butterFilter

        self.butterFilter = BandFilters.ButterWorthFilter(20, 1800, order=3)
        return self.butterFilter
