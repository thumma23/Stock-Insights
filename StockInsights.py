from StockInsight_getData import TickerData
from StockInsight_Calculations import TickerCalc
import json
import datetime 
from datetime import date


today_date = date.today()
string_date = today_date.strftime('%Y-%m-%d')
past_Date = datetime.datetime.now() - datetime.timedelta(days=90)
finhub_token = input("Enter in your FinHub token: ")
ticker = input("Ticker of Company: ")
user_input = ""


while(user_input != 'exit'):

    print("")
    print("1. Company News")
    print("2. Financials")
    print("3. Recommendation Trends")
    print("4. My Recommendation")
    print("5. Change Ticker")
    print("6. Exit")


    user_input = input()

    Ticker_Data = TickerData(ticker, finhub_token)
    Ticker_Calc = TickerCalc(ticker, past_Date, today_date, string_date, finhub_token)

    if(user_input == "1"):
        Ticker_Data.getTickerNews()

    if(user_input == "2"):
        Ticker_Data.getTickerFinancials()

    if(user_input == "3"):
        Ticker_Data.getRecommendation()
    
    if(user_input == "4"):
        Ticker_Calc.myRecomendation()

    if(user_input == "5"):
        ticker = input("New Ticker: ")

    if(user_input == "6"):
        user_input = 'exit'




