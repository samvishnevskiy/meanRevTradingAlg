import yfinance as yf

#calculates the value of the portfolio at any given time
def value(cash, positions, prices, index) ->float:
    out = float(cash)
    for i in range(0, len(positions)):
        out+=prices.iloc[index]*10
    return out

spy = yf.Ticker("SPY")
spyPrices = spy.history(start = "2024-08-01", end = "2025-08-02", interval  = "1d")["Close"]

def ma2(tickerSymbol) ->int:
    ticker = yf.Ticker(tickerSymbol)
    print("\n" + str(ticker))
    historicalData = ticker.history(start = "2024-08-01", end = "2025-08-02", interval  = "1d")
    prices = historicalData["Close"]
    money = 100000 
    positions = []
    sma = 0     #short-term moving average
    lma = 0;    #long-term moving average

    #initializes the moving averages with data directly before the 1 year window starts
    averageData = ticker.history(start = "2024-07-05", end = "2024-08-02", interval  = "1d")["Close"]
    for i in range(0, len(averageData)):
        if(i > 14):
            sma += averageData.iloc[i]
        lma += averageData.iloc[i]
    lma /= len(averageData) 
    lma /= 5; 
    for i in range (0, len(prices)):
        #If 50% returns are achieved, or if 20% of the portfolio value is lost, the algorithm terminates
        if(value(money, positions, prices, i) > 150000 or value(money, positions, prices, i) < 80000):
            print("Stop-loss or success")
            for j in range(len(positions)):
                money += 10 * prices.iloc[i]
            break
        #updating the short and long term moving averages
        if(i >= 4):
            sma = (sma * 5 - prices.iloc[i-5] + prices.iloc[i])/5
        else:
            sma = (sma * 5 - averageData.iloc[i+15] + prices.iloc[i])/5
        if(i >= 19):
            lma = (lma * 20 - prices.iloc[i-20] + prices.iloc[i])/20
        else:
            lma = (lma * 20 - averageData.iloc[i] + prices.iloc[i])/20
        #closing all positions when the short-term moving average is lower than the long-term moving 
        # average, as this is a bearish signal indicating future downturn
        j = 0
        while(j < len(positions)):
            if(sma < lma):
                money += 10 * prices.iloc[i]
                positions.pop(j)
            else:
                j+=1
        #buys shares if there are sufficient funds and the short-term moving average is higher than the 
        #long term moving average, a bullish signal indicating future growth
        if(money >= 10 * prices.iloc[i] and sma > lma):
            positions.append(prices.iloc[i])
            money -= 10* prices.iloc[i]
        #close all remaining positions if the year-long window is over
        if(i == len(prices) -1):
            for j in range(len(positions)):
                money += 10 * prices.iloc[i]
    #print results of the algorithm profit, the results of buying and holding the same stock,
    #and SPY performance over the same time period as a benchmark
    print("\nAlgorithm profit: "+ str(money- 100000))
    print("Stock profit: " + str(100000/prices.iloc[0]* prices.iloc[-1]  - 100000))
    print("SPY profit: " + str((100000/spyPrices.iloc[0]* spyPrices.iloc[-1]) -100000))
    return money-100000

stocks = ["MMM", "AXP", "AMGN", "AMZN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "GS", "HD", "HON", "IBM", "JNJ", "JPM", "MCD", "MSFT", "TRV", "UNH", "VZ", "V", "WMT", "GOOGL", "TSLA", "META"]

returns = 0;
for i in range(0, len(stocks)):
    returns += ma2(stocks[i])

print("\nThe average return of the trading algorithm across selected stocks from 08/01/2024 to 08/01/2025 is: " + str(returns/len(stocks)))
print("In the same time period, the SPY return is: " + str((100000/spyPrices.iloc[0]* spyPrices.iloc[-1]) -100000))  
