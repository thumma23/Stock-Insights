import requests
import json
import locale
import re
import time

locale.setlocale( locale.LC_ALL, '' )

class TickerData():
    def __init__(self, ticker, token):
        self.ticker = ticker
        self.token = token
        self.counter = 0

    def getFinhubData(self, uri):
        url = f"https://finnhub.io/api/v1/{uri}"
        time.sleep(1)
        self.counter += 1
        return requests.get(url = url)
        

    def getTickerNews(self):
        URL = "company-news?symbol={}&from=2020-04-30&to=2020-05-01&token={}".format(self.ticker, self.token)
        try:
            stock_api = self.getFinhubData(URL)

            if stock_api.status_code != 200:
                raise Exception(f"Error occuredn Code: {stock_api.status_code}")
            elif stock_api.content is None:
                raise Exception("No Content within Data Request")
            else:
                stock_data = stock_api.json()
                for record in stock_data[:5]:
                    print(f"HEADLINE: {record['headline']}")
                    print(f"SUMMARY: {record['summary']}")
                    print(f"URL: {record['url']}")
                    print("")                              
        except requests.exceptions.ConnectionError as err:
            raise err
        except Exception as e:
            raise(e)
    
    def getTickerFinancials(self):
        URL = f"stock/financials-reported?symbol={self.ticker}&token={self.token}"
        try:
            stock_api = self.getFinhubData(URL)
            if stock_api.status_code != 200:
                raise Exception(f"Error occuredn Code: {stock_api.status_code}")
            elif stock_api.content is None:
                raise Exception("No Content within Data Request")
            else:
                stock_data = stock_api.json()
                stock_data = stock_data["data"]
                for record in stock_data[:4]:
                    print(f"YEAR: {record['year']}")
                    for type_finance in record['report']:
                        finance_dict = record['report'][type_finance]
                        for finance_data in finance_dict:
                            if(finance_dict[finance_data] == 'N/A'):
                                pass
                            else:
                                print(re.sub(r"(\w)([A-Z])", r"\1 \2", finance_data), ' -> ', locale.currency(float(finance_dict[finance_data]), grouping= True))                     
        except requests.exceptions.ConnectionError as err:
            raise err
        except Exception as e:
            raise(e)
    
    def getRecommendation(self):
        URL = f"stock/recommendation?symbol={self.ticker}&token={self.token}"
        try:
            stock_api = self.getFinhubData(URL)
            if stock_api.status_code != 200:
                raise Exception(f"Error occuredn Code: {stock_api.status_code}")
            elif stock_api.content is None:
                raise Exception("No Content within Data Request")
            else:
                stock_data = stock_api.json()
                stock_data = stock_data[0]
                print("")
                print(f"BUY: {stock_data['buy']}")
                print(f"HOLD: {stock_data['hold']}")
                print(f"SELL: {stock_data['sell']}")
                print(f"Period: {stock_data['period']}")
                print("")                              
        except requests.exceptions.ConnectionError as err:
            raise err
        except Exception as e:
            raise(e)

    def getFinData(self):
        URL = f"stock/financials-reported?symbol={self.ticker}&token={self.token}"
        try:
            fin_values = {}
            stock_api = self.getFinhubData(URL)
            if stock_api.status_code != 200:
                raise Exception(f"Error occuredn Code: {stock_api.status_code}")
            elif stock_api.content is None:
                raise Exception("No Content within Data Request")
            else:
                stock_data = stock_api.json()
                stock_data = stock_data["data"]
                for record in stock_data:
                    for type_finance in record['report']:
                        finance_dict = record['report'][type_finance]
                        for finance_data in finance_dict:
                            if(finance_dict[finance_data] == 'N/A'):
                                pass
                            elif(finance_data == 'Assets'):
                                fin_values['Assets'] = (finance_dict[finance_data])
                            elif(finance_data == 'Liabilities'):
                                fin_values['Liabilities'] = (finance_dict[finance_data])
                            elif(finance_data == 'NetIncomeLoss'):
                                fin_values['Net Income Loss'] = (finance_dict[finance_data])
                            elif('Depreciation' in finance_data):
                                fin_values['Depreciation'] = (finance_dict[finance_data])
                            elif(finance_data == 'StockholdersEquity'):
                                fin_values['Stock Holders Equity'] = (finance_dict[finance_data])
                            elif(finance_data == 'LiabilitiesCurrent'):
                                fin_values['Total Debt'] = (finance_dict[finance_data])
                            elif(finance_data == 'OperatingIncomeLoss'):
                                fin_values['Operating Income'] = (finance_dict[finance_data])
                            elif('Revenue' in finance_data):
                                fin_values['Revenue'] = (finance_dict[finance_data])

                    return fin_values
        except Exception as e:
            raise(e)

    def getEPSData(self):
        URL = f"stock/earnings?symbol={self.ticker}&token={self.token}"
        try:
            eps_values = {}
            stock_api = self.getFinhubData(URL)
            if stock_api.status_code != 200:
                raise Exception(f"Error occuredn Code: {stock_api.status_code}")
            elif stock_api.content is None:
                raise Exception("No Content within Data Request")
            else:
                stock_data = stock_api.json()
                for record in stock_data[0:2]:
                    eps_values[record['period']] = record['actual']
                return eps_values                          
        except requests.exceptions.ConnectionError as err:
            raise err
        except Exception as e:
            raise(e)

    
    def getCalcData(self):
        financial_Data = []
        financial_Data.append(self.getFinData())
        financial_Data.append(self.getEPSData())
        return financial_Data        
