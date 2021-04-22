import money, json, requests, talib, pprint, numpy, ast, time, sys


# change this number depending on how conservative you want the bot to be
buythreshold = 50

# This is the list of coins to trade, to add a coin, simply add it's symbol to the list
coinlist = ["ETH", "BTC", "XRP", "BNB", "ADA"]

# use a value of trust. The more trust there is in a trade, the bigger amount that you should put in.
# make sure to end trades if they go below around 2-6% 

def handler(moneylist):

    # get the trust value for each currency and then sell if it goes under the sell threshold, and buy the percentage that it goes above the buy threshold 
    for moneytype in moneylist:

        trust = analyse(moneytype)

        print("trust of " + moneytype + ":")
        print(trust)

        if trust > buythreshold:

            percentage = ((trust / buythreshold) - 1)
            money.sellall(moneytype)
            money.buy(moneytype, (money.checkbal("USD") * percentage))

        else:

            money.sellall(moneytype)







def analyse(moneytype):
    trust = 0.00

    # RSI
    # for rsi, we need to convert the closes to a numpy array and then pass the array to the function as doubles for some reason
    numpy_closes = numpy.array(data[moneytype]['close'], dtype="f8")
    rsi = talib.RSI(numpy_closes)
    # this will return a list of values for the rsi at different time periods

    # now we just add the most recent value to our trust
    rsilast = rsi[len(rsi) - 1]

    trust += 100 - float(rsilast)


    # MACD
    # for the MACD indicator, we are just going to add a hard number to the trust depending on if the MACD line is above the signal line or not
    macd, macdsignal, macdhist = talib.MACD(numpy_closes)
    macdlast = macd[len(macd) - 1]
    lastsignal = macdsignal[len(macd) - 1]
    if macdlast > lastsignal:
        trust += 20
    else:
        trust -= 20
    
    # SMA
    # for SMA, we will use a 30 minute SMA. I don't know how accurate this is going to be.
    # pretty straight forward, if the price is above the sma thats good, if its below, thats bad
    real = talib.SMA(numpy_closes)
    lastreal = float(real[len(real) - 1])

    if float(data[moneytype]['close'][len(data[moneytype]['close']) - 1]) > lastreal:
        trust += 20
    else:
        trust -= 20
    


    return trust
    

data = {}

for coin in coinlist:
    data[coin] = {
    "open": [],
    "high": [],
    "low": [],
    "close": [],
    "volume": []
    }


while True:
    for coin in coinlist:
        print("Getting market data for " + str(coin) + "...")
        try:
            call = requests.get(f"https://api.binance.com/api/v3/klines?symbol={coin}USDT&interval=1m")
        except:
            print("Failure to get market data for " + str(coin))
            print("Shutting down...")
            sys.exit(1)
        print("Success!")

        # decode the request information into readable data
        calldata = ast.literal_eval(call.content.decode("utf-8"))

        for entry in calldata:
            data[coin]['open'].append(entry[1])
            data[coin]['high'].append(entry[2])
            data[coin]['low'].append(entry[3])
            data[coin]['close'].append(entry[4])
            data[coin]['volume'].append(entry[5])

    
    handler(coinlist)
    # we are going to run everything once every minute
    # because running everything constantly would just waste resources
    time.sleep(60)