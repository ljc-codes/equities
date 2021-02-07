import os 
from equities.api import Client as api
from equities import static as STATIC 

__version__ = STATIC.__version__
__author__  = STATIC.__author__

class Universe(object):
    """ programatic representation of a stock universe """

    def __init__(self,verbose=False):
        self.api = api(verbose=verbose)
        self.ciks = self.api.ciks
        self.names = self.api.names
        self.tickers = self.api.tickers

    def cik_to_name(self):
        """returns a  dict mapping ciks to company names"""
        return self.api.cik_to_name()

    def cik_to_ticker(self):
        """returns a dict mapping ciks to tickers"""
        return self.api.cik_to_ticker()

    def ticker_to_cik(self):
        """returns a dict mapping tickers to ciks"""
        return self.api.ticker_to_cik()

    def name_to_cik(self):
        """returns a dict mapping names to ciks"""
        return self.api.name_to_cik()

    def prices(self,cik_or_ticker,period='max'):
        """returns a price dataframe for the given cik or tickers and period.
           period must be a string contained in the following list:
           ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'].
        """
        return self.api.prices(cik_or_ticker,period)

    def actions(self,cik_or_ticker):
        """returns a corporate actions dataframe for the given cik or tickers"""
        return self.api.actions(cik_or_ticker)

    def dividends(self,cik_or_ticker):
        """returns a dividends dataframe for the given cik or tickers"""
        return self.api.dividends(cik_or_ticker)

    def splits(self,cik_or_ticker):
        """returns a splits dataframe for the given cik or tickers"""
        return self.api.splits(cik_or_ticker)

    def major_holders(self,cik_or_ticker):
        """returns a dataframe of major holders for the given cik or ticker"""
        return self.api.major_holders(cik_or_ticker)

    def institutional_holders(self,cik_or_ticker):
        """returns a dataframe of instiutional holders for the given cik or ticker"""
        return self.api.institutional_holders(cik_or_ticker)

    def events(self,cik_or_ticker):
        """returns a dataframe of earnings events for the given cik or ticker"""
        return self.api.events(cik_or_ticker)

    def recommendations(self,cik_or_ticker):
        """returns a dataframe buy/sell side recommendations for the given cik or ticker"""
        return self.api.recommendations(cik_or_ticker)

    def esg(self,cik_or_ticker):
        """returns a dataframe esg metrics for the given cik or ticker"""
        return self.api.esg(cik_or_ticker)

    def financial_statement(self,cik_or_ticker,kind):
        """returns a financial statement dataframe for the given cik or ticker
            and kind of statement. kind must be a string contained in the following 
            list: ['income','balance','cash','equity'].
        """
        return self.api.financial_statement(cik_or_ticker,kind)

    def interest(self,name):
        """returns a dataframe of google search interest for a particular name"""
        return self.api.interest(name)

    def search(self,query):
        """ returns a dict mapping ciks to names containing 
            matched companies to a given query.
        """
        return self.api.search(query)

    def company(self,query,search=False):
        """returns a dictionary of data for a given ticker/cik/search query"""
        return self.api.company(query,search=search)

    '''def download(self,queries=[],search=False,data_dir=None):

        def _to_json():
            for key, data in company_data.items():
                if type(data) == pd.DataFrame:
                    return data.to_json()

        # create dir
        os.makedirs(os.path.join('data'),exist_ok=True)

        download_path = 

        if queries == []:
            for cik in self.cik:
                company_data = self.company(query,search)
                
        else:
            for query in queries:
                company_data = self.company(query,search)'''
