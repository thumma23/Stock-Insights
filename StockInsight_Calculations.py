import numpy as np
from pandas_datareader import data as pdr
import pandas as pd
from StockInsight_getData import TickerData
import statistics


class TickerCalc():
    def __init__(self, ticker, past_Date, today_date, string_date, token):
        self.ticker = ticker
        self.token = token
        self.today_date = today_date
        self.string_date = string_date
        self.past_Date = past_Date 
        self.Ticker_Data = TickerData(ticker, token)
        self.financial_Data = self.Ticker_Data.getCalcData()

    def findVolatility(self):
        stocks = ['^GSPC', self.ticker]
        ticker_RollingData = pdr.DataReader(stocks, 'yahoo', self.past_Date, self.today_date)['Adj Close']

        ticker_RecentPrice = ticker_RollingData[self.ticker][-1]
        SPX_RecentPrice = ticker_RollingData['^GSPC'][-1]

        ticker_Perc = (statistics.stdev(ticker_RollingData['^GSPC'].to_numpy())/(SPX_RecentPrice))
        SPX_Perc = (statistics.stdev(ticker_RollingData[self.ticker].to_numpy())/(ticker_RecentPrice))

        correlation_in_stocks = np.corrcoef((ticker_RollingData[self.ticker], ticker_RollingData['^GSPC']))[0,1]
        beta_value = correlation_in_stocks * (ticker_Perc/SPX_Perc)
        return beta_value

    def findLiquidity(self):
        try:
            Company_Assets = self.financial_Data[0]['Assets']
            Company_Liabilities = self.financial_Data[0]['Liabilities']
            Company_Liquidity = Company_Assets/Company_Liabilities
            return Company_Liquidity
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            raise(e)

    def findProfitMargin(self):
        try:
            Company_OperatingIncome = self.financial_Data[0]['Operating Income']
            Company_Revenue = self.financial_Data[0]['Revenue']
            ProfitMargin = (Company_OperatingIncome/Company_Revenue) * 100
            return ProfitMargin
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            raise(e)
            

    def findSolvency(self):
        try:
            Company_NetIncome = self.financial_Data[0]['Net Income Loss']
            Company_Liabilities = self.financial_Data[0]['Liabilities']
            Company_Depreciation = self.financial_Data[0]['Depreciation']
            Company_Solvency = (Company_NetIncome + Company_Depreciation)/Company_Liabilities * 100
            return Company_Solvency
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            raise(e)

    def findDebtRatio(self):
        try:
            Company_Assets = self.financial_Data[0]['Assets']
            Company_Debt = self.financial_Data[0]['Total Debt']
            Company_DebtRatio = (Company_Debt/Company_Assets) * 100
            return Company_DebtRatio
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            raise(e)

    def findDebtToEquity(self):
        try:
            Company_Liabilities = self.financial_Data[0]['Liabilities']
            Company_Equity = self.financial_Data[0]['Stock Holders Equity'] 
            Company_DebtEquity = Company_Liabilities/Company_Equity
            return Company_DebtEquity
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            raise(e)

    def findPE(self):
        yahoo_data = pdr.get_data_yahoo(self.ticker, start = self.past_Date, end = self.today_date)['Adj Close']
        ticker_Price = pd.DataFrame(yahoo_data, columns = ['Adj Close'])
        ticker_Price = ticker_Price['Adj Close'][-1]  
        Company_EPS = self.financial_Data[1]
        for date in Company_EPS:
            if(self.string_date >= date):
                Company_EPS = self.financial_Data[1][date] 
        Company_PE = ticker_Price/Company_EPS
        return Company_PE
    
    def findPEGrowth(self):
        EPS2Recent = 0
        for date in self.financial_Data[1]:
            EPSRecent = EPS2Recent
            EPS2Recent = self.financial_Data[1][date]
        EPSGrowth = ((EPSRecent - EPS2Recent) / EPS2Recent) * 100
        Company_PE = self.findPE()
        PEGrowth = Company_PE/EPSGrowth
        return PEGrowth

    def getAllCalculations(self):
        Calc_Values = {}
        Calc_Values['Beta Value'] = self.findVolatility()
        Calc_Values['Liquidity'] = self.findLiquidity()
        Calc_Values['Solvency'] = self.findSolvency()
        Calc_Values['Profit Margin'] = self.findProfitMargin()
        Calc_Values['Debt Ratio'] = self.findDebtRatio()
        Calc_Values['Debt to Equity'] = self.findDebtToEquity()
        Calc_Values['PE Growth'] = self.findPEGrowth()
        return Calc_Values


    def myRecomendation(self):  
        Calc_Values = self.getAllCalculations()
        final_values = {}
        actual_values = {}
        for calc_type in Calc_Values:
            if(calc_type == 'Beta Value'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] < 1):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'Liquidity'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] >= 1):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'Solvency'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] >= 20):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'Profit Margin'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] >= 15):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'Debt Ratio'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] <= 50):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'Debt to Equity'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] <= 1.5):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
            if(calc_type == 'PE Growth'):
                if(Calc_Values[calc_type] != None):
                    actual_values[calc_type] = Calc_Values[calc_type]
                    if(Calc_Values[calc_type] <= 1 and Calc_Values[calc_type] > 0):
                        final_values[calc_type] = Calc_Values[calc_type]
                    else:
                        pass
                else:
                    pass
                
        len_of_actualvalues = len(actual_values)
        for i in final_values:
            print(i , " " , final_values[i])

        if(len(final_values) > (len_of_actualvalues * 0.75)):
            print("")
            print("Strong Buy")
        elif(len(final_values) > (len_of_actualvalues * 0.5) and len(final_values) <= (len_of_actualvalues * 0.75)):
            print("")
            print("Buy")
        elif(len(final_values) == (len_of_actualvalues * 0.5)):
            print("")
            print("Hold")
        elif(len(final_values) < (len_of_actualvalues * 0.5) and len(final_values) >= (len_of_actualvalues * 0.25)):
            print("")
            print("Sell")   
        elif(len(final_values) < (len_of_actualvalues * 0.25)):
            print("")
            print("Strong Sell")    



