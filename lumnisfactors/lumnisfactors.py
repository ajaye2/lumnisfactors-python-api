import grequests
import os
import pandas as pd
import requests
import json
import numpy as np
import datetime




class LumnisFactors:
    def __init__(self, api_key):
        self.KEY = api_key #os.environ['LUMNIS']
        self.API_BASE = "https://api.lumnis.io/v1"
        self.HEADERS = {
            "x-api-key": self.KEY
        }

    @staticmethod
    def convert_from_unix_to_datetime(inp_date, unit='ns'):
        """
        Converts UNIX time to regular date time when forming Pandas returned DF.
        """
        return pd.to_datetime(inp_date, unit=unit, origin='unix', utc=True)

    def get_single_date_data(self, factor_name: str, exchange: str, asset: str, time_frame: str, date: str):
        """
        Gets data for defined parameters for only one date. Returns pd DF of data.
        See docs.lumnis.io (docs) for values each of the parameters can take.
        """
        PARAMS = "/historical?factorName=%s&exchange=%s&asset=%s&timeFrame=%s&date=%s" % (
            factor_name, exchange, asset, time_frame, date)
        url = self.API_BASE + PARAMS
        res = requests.get(url, headers=self.HEADERS)

        if res.status_code != 200:  
            raise Exception('Api call failed. Make sure you have passed in a valid API Key and the right parameters.', res.status_code, res.json() )


        data_api = pd.DataFrame(json.loads(res.json()['data']))
        # data_api.index = data_api.index.astype(np.int64)
        # data_api.index = self.convert_from_unix_to_datetime(data_api.index)
        data_api.drop_duplicates(inplace=True)

        return data_api

    def get_multi_date_data_sequential(self, factor_name: str, exchange: str, asset: str, time_frame: str,
                                       start_date: str, end_date: str):
        """
        Gets data for defined parameters over a date range sequentially with loops. Returns pd DF of data.
        See docs.lumnis.io (docs) for values each of the parameters can take.
        """
        curr_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        END_DATE = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        api_data_list = []
        while curr_date <= END_DATE:
            try:
                date = curr_date.strftime('%Y-%m-%d')
                PARAMS = "/historical?factorName=%s&exchange=%s&asset=%s&timeFrame=%s&date=%s" % (
                    factor_name, exchange, asset, time_frame, date)
                res = requests.get(self.API_BASE + PARAMS, headers=self.HEADERS)
                api_data_list.append(pd.DataFrame(json.loads(res.json()['data'])))
                curr_date += pd.Timedelta(days=1)
            except Exception as e:
                print(curr_date, " failed", e)
                curr_date += pd.Timedelta(days=1)

        data_api = pd.concat(api_data_list, axis=0)
        # data_api.index = data_api.index.astype(np.int64)
        # data_api.index = self.convert_from_unix_to_datetime(data_api.index)
        data_api.drop_duplicates(inplace=True)

        return data_api

    def get_historical_data(self, factor_name: str, exchange: str, asset: str, time_frame: str,
                                     start_date: str, end_date: str):
        """
        Gets data for defined parameters over a date range in paralle with grequests. Returns pd DF of data.
        Significantly faster than sequential version.
        See docs.lumnis.io (docs) for values each of the parameters can take.
        """
       

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        END_DATE = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        def get_lumnis_url(factor, exch, coinpair, timespan, date):
            date = date.strftime('%Y-%m-%d')
            PARAMS = "/historical?factorName=%s&exchange=%s&asset=%s&timeFrame=%s&date=%s" % (
                factor, exch, coinpair, timespan, date)
            return self.API_BASE + PARAMS

        def exception_handler(request, exception):
            print(exception)

        date_range_for_urls = pd.date_range(start_date, END_DATE)
        urls = [get_lumnis_url(factor_name, exchange, asset, time_frame, x) for x in date_range_for_urls]

        rs = (grequests.get(u, headers=self.HEADERS) for u in urls)
        res_items_ret = grequests.map(rs, exception_handler=exception_handler)
        res_items = []

        for i, res in enumerate( res_items_ret ):
            if res is not None and res.status_code != 200:
                print("One API call failed with status code", res.status_code, "url: ", urls[i], "response: ", res.json()) 
            elif res is None:
                print("One API call failed; no status code returned", "url: ", urls[i])
            else:
                res_items.append(res)
        
        if len(res_items) == 0:
            raise Exception('None of the api calls succeeded. Make sure you have passed in a valid API Key and the right parameters.')

        api_data_list = [pd.DataFrame(json.loads(x.json()['data'])) for x in res_items]
        data_api = pd.concat(api_data_list, axis=0)
        # data_api.index = data_api.index.astype(np.int64)
        # data_api.index = self.convert_from_unix_to_datetime(data_api.index)
        data_api.drop_duplicates(inplace=True)

        return data_api
    
    def get_live_data(self, factor_name: str, exchange: str, asset: str, time_frame: str, offset: int = 100):
        """
        Gets live data for defined parameters. Returns pd DF of data.
        See docs.lumnis.io (docs) for values each of the parameters can take.
        """

        PARAMS = "/live?factorName=%s&exchange=%s&asset=%s&timeFrame=%s&offset=%s" % (
        factor_name, exchange, asset, time_frame, offset)

        url = self.API_BASE + PARAMS
        res = requests.get(url, headers=self.HEADERS)

        if res.status_code != 200:  
            raise Exception('Api call failed. Make sure you have passed in a valid API Key and the right parameters.', res.status_code, res.json() )


        data_api = pd.DataFrame(json.loads(res.json()['data']))
        data_api.drop_duplicates(inplace=True)
        return data_api
        