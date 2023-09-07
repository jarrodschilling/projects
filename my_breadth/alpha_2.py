from functions import alpha

symbol = "IWM"
period = 20
ma = "EMA"

twenty = alpha(symbol, period, ma)

ten = alpha(symbol, 50, "SMA")

forty = alpha(symbol, 200, "SMA")


print(twenty)
print(ten)
print(forty)

if twenty > ten and ten > forty:
    print("power trend")
else:
    print("loser")