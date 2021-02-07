import concurrent.futures
import pandas as pd 
from equities import static as STATIC 
from solaris.api import Client as SolarisClient
from pytrends.request import TrendReq as GoogleTrendClient
import yfinance as YahooFinanceClient

__version__ = STATIC.__version__
__author__  = STATIC.__author__

class Client(object):
    """ equities composed clients """

    def __init__(self,verbose=False):
        try:
            # sets verbosity level and prints begin init text
            self.verbose = verbose; STATIC.initialize(self.verbose)

            # connects clients 
            self._sol = SolarisClient(verbose=self.verbose)
            self._pytrends = GoogleTrendClient(hl='en-US', tz=360)

            # sets stock identification variables 
            self.tickers = list(set(self._sol.cik_to_ticker.values()))
            self.names = list(set(self._sol.cik_to_name.values()))
            self.ciks = list(set(self._sol.cik_to_name.keys()))

            # prints end init text
            messages = self._sol._fetch_equities_messages()
            STATIC.initialized(self.verbose,messages,len(self.ciks))

        except Exception as e:
            STATIC.failed(e)

    def __len__(self):
        return len(self.ciks)

    def __str__(self):
        return str(self._sol.name_to_cik)

    def _query_y_finance(self,cik_or_ticker):
        """ returns a yfinance Ticker object by quering YahooFinance
            for a given cik or ticker
        """
        try:
            cik = self._convert_to_cik(cik_or_ticker)
            ticker = self._sol.cik_to_ticker[cik]
        except:
            ticker = cik_or_ticker
        return YahooFinanceClient.Ticker(ticker)


    def _convert_to_cik(self,cik_or_ticker):
        """ returns a cik from a query/ticker into the corresponding 
            cik number with cleaning.
        """
        symbol = cik_or_ticker.lower().replace(' ','')
        try:
            if symbol in self.tickers:
                return self._sol.ticker_to_cik[symbol]
            elif str(int(cik_or_ticker)) in self.ciks:
                return str(int(cik_or_ticker))
            else: 
                print('Error Could not Convert: %s'%cik_or_ticker)
                return cik_or_ticker
        except: 
            return cik_or_ticker

    def _set_verbose(self,verbose):
        """sets universes' stdout level of verbosity"""
        self.verbose = verbose
        self._sol.verbose = verbose 

    def _invert_dict(self,to_invert):
        """inverts an arbitrary python dictionary"""
        return {v:k for k,v in to_invert.items()}

    def cik_to_name(self):
        """returns a  dict mapping ciks to company names"""
        return dict(zip(
            self._sol.cik_to_name.keys(),self._sol.cik_to_name.values()
            ))

    def cik_to_ticker(self):
        """returns a dict mapping ciks to tickers"""
        return dict(zip(
            self._sol.cik_to_ticker.keys(),self._sol.cik_to_ticker.values()
            ))

    def ticker_to_cik(self):
        """returns a dict mapping tickers to ciks"""
        return self._invert_dict(self.cik_to_name)

    def name_to_cik(self):
        """returns a dict mapping names to ciks"""
        return self._invert_dict(self.cik_to_name)

    def prices(self,cik_or_ticker,period='max'):
        """returns a price dataframe for the given cik or tickers and period.
           period must be a string contained in the following list:
           ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'].
        """
        try:
            return self._query_y_finance(cik_or_ticker).history(period=period)
        except Exception as e:
            return pd.DataFrame()

    def actions(self,cik_or_ticker):
        """returns a corporate actions dataframe for the given cik or tickers"""
        try:
            return self._query_y_finance(cik_or_ticker).actions
        except Exception as e:
            return pd.DataFrame()

    def dividends(self,cik_or_ticker):
        """returns a dividends dataframe for the given cik or tickers"""
        try:
            return self._query_y_finance(cik_or_ticker).dividends
        except Exception as e:
            return pd.DataFrame()

    def splits(self,cik_or_ticker):
        """returns a splits dataframe for the given cik or tickers"""
        try:
            return self._query_y_finance(cik_or_ticker).splits
        except Exception as e:
            return pd.DataFrame()

    def major_holders(self,cik_or_ticker):
        """returns a dataframe of major holders for the given cik or ticker"""
        try:
            return self._query_y_finance(cik_or_ticker).major_holders
        except Exception as e:
            return pd.DataFrame()
        
    def institutional_holders(self,cik_or_ticker):
        """returns a dataframe of instiutional holders for the given cik or ticker"""
        try:
            return self._query_y_finance(cik_or_ticker).institutional_holders
        except Exception as e:
            return pd.DataFrame()

    def events(self,cik_or_ticker):
        """returns a dataframe of earnings events for the given cik or ticker"""
        try:
            return self._query_y_finance(cik_or_ticker).calendar
        except Exception as e:
            return pd.DataFrame()

    def recommendations(self,cik_or_ticker):
        """returns a dataframe buy/sell side recommendations for the given cik or ticker"""
        try:
            return self._query_y_finance(cik_or_ticker).recommendations
        except Exception as e:
            return pd.DataFrame()

    def esg(self,cik_or_ticker):
        """returns a dataframe esg metrics for the given cik or ticker"""
        try:
            return self._query_y_finance(cik_or_ticker).sustainability
        except Exception as e:
            return pd.DataFrame()

    def financial_statement(self,cik_or_ticker,kind):
        """returns a financial statement dataframe for the given cik or ticker
            and kind of statement. kind must be a string contained in the following 
            list: ['income','balance','cash','equity'].
        """
        try:
            cik = self._convert_to_cik(cik_or_ticker)
            return self._sol.financial_statement(cik,kind,df=True)
        except Exception as e:
            #print(e)
            return pd.DataFrame()

    def interest(self,name):
        """returns a dataframe of google search interest for a particular name"""
        try:
            self._pytrends.build_payload(
                [name.replace('/','')],
                cat=0,
                timeframe='today 5-y',
                geo='',
                gprop='')
            return self._pytrends.interest_over_time()
        except Exception as e:
            print(e)
            return pd.DataFrame()

    def search(self,query):
        """ returns a dict mapping ciks to names containing 
            matched companies to a given query.
        """
        matches = []
        for name in self.names:
            if query.lower() in name.lower():
                matches.append(self._sol.name_to_cik[name])
        for ticker in self.tickers:
            if query.lower() in ticker.lower():
                matches.append(self._sol.ticker_to_cik[ticker])
        for cik in self.ciks:
            if query in cik:
                matches.append(cik)
        STATIC.search(self.verbose,query,str(len(matches)))
        return {self._sol.cik_to_name[match]:match for match in matches}

    def company(self,query,search=False):
        """returns a dictionary of data for a given ticker/cik/search query"""

        def execute_request(cik):
            """executes data request"""
            try:
                sol_data = self._sol.company(cik,df=True)
            except:
                sol_data = {'name' : cik }

            yfinance_data = {
                'prices' : self.prices(cik),
                'actions' : self.actions(cik),
                'dividends' : self.dividends(cik),
                'splits' : self.splits(cik),
                'major_holders' : self.major_holders(cik),
                'institutional_holders': self.institutional_holders(cik),
                'events': self.events(cik),
                'recommendations': self.recommendations(cik),
                'esg': self.esg(cik),
                'interest': self.interest(sol_data['name'])
            }
            sol_data.update(yfinance_data)
            return sol_data

        if type(query) == str:
            if search: # singleticker case (searches if specified)
                cik = list(self.search(query).values())[0]
            else:
                cik = self._convert_to_cik(query)
            return execute_request(query)
        elif type(query) == list:
            results = None # multiticker case (multithreaded,recursive)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                args = (ticker for ticker in query)
                saved_verbose = self.verbose; self._set_verbose(True)
                future = executor.map(self.company, args)
                results = dict(zip(query,future))
            self._set_verbose(saved_verbose)
            return results 
        else: 
            print('Error with arguments: %s'%str(query))
            quit()
            
