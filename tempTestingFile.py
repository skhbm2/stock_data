symbol = ""
symbolBool = True
while symbolBool:
    symbol = input(f"\nEnter the stock symbol you are looking for: ")
    symbol = symbol.upper()
    if symbol.isalpha() and len(symbol) <= 5:
        symbolBool = False
    else:
        print("\nYour Symbol doesn't exist")