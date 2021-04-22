import requests

# This will serve as a library for the input and output of money

# first we will check to see if we have enough money to make the trade. 
# Then we will lookup the price and either buy or sell at that price 
# amount should always be in USD
def buy(moneytype, amount):
    # check to see if we have enough money to make the trade
    if checkbal("USD") < amount:
        return False

    # get the price of the coin you want to buy
    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + str(moneytype).upper() + "USDT")
    price = float(r.json()["price"])
    
    # read the money file and store it in a list
    with open("money.txt", "r") as f:
        contents = f.readlines()
    
    # modify the list
    isnthere = True
    for line in range(len(contents)):
        if "USD" in contents[line]:
            contents[line + 1] = str(float(contents[line + 1]) - amount) + '\n'
        if moneytype in contents[line]:
            contents[line + 1] = str(float(contents[line + 1]) + amount/price) + '\n'
            isnthere = False
    
    if isnthere:
        contents.append(str(moneytype) + ":\n")
        contents.append("0.0\n")

    
    # write that list back into the file
    with open("money.txt", "w") as f:
        for line in contents:
            f.write(line)
    
    print("\nBought $" + str(amount) + " worth of " + str(moneytype) + "\n")

    return price

    
    #sell the type and the amount of that type
def sell(moneytype, amount):
    if checkbal(moneytype) < amount:
        return False
    
    # get the price of the coin you want to buy
    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + str(moneytype).upper() + "USDT")
    price = float(r.json()["price"])

    # read the money file and store it in a list
    with open("money.txt", "r") as f:
        contents = f.readlines()
    
    # modify the list
    for line in range(len(contents)):
        if "USD" in contents[line]:
            contents[line + 1] = str(float(contents[line + 1]) + amount*price) + '\n'
        if moneytype in contents[line]:
            contents[line + 1] = str(float(contents[line + 1]) - amount) + '\n'

    # write that list back into the file
    with open("money.txt", "w") as f:
        for line in contents:
            f.write(line)


    print("\nSold " + str(amount) + " " + str(moneytype) + "\n")

    return price


# Quick function to check the balance of a type of money
def checkbal(moneytype):
    with open("money.txt", 'r') as f:
        for line in f:
            if moneytype in line:
                return float(next(f))
    return 0.0


def sellall(moneytype):
    sell(moneytype, checkbal(moneytype))

def buyall(moneytype):
    buy(moneytype, checkbal("USD"))

# sellall("ETH")
# sellall("BTC")
# sellall("XRP")
# sellall("BNB")
# sellall("ADA")
