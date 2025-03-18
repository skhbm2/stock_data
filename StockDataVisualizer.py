##INFO TECH 4430 - Software Engineering
#Project 3 - Stock Data Visualization
#Scrum Team 2 - Sam Herrmann (Scrum Master), Zoey Benedict, Karson Null, Ken Kreidell

# Resources
# AlphaVantage API Key:   H1514RX61K8J6SFK
# https://www.alphavantage.co/documentation/    (API to get stock info)
# https://requests.readthedocs.io/en/latest/    (code to call API)
# https://www.pygal.org/en/stable/documentation/types/index.html    (graphing tool)
# https://lxml.de/  (tool to create HTML to wrap graph)
print(f"\nStock Data Visualizer")
print("------------------------")


keep_going = True
while keep_going:

# Collect graph parameters

    # Get symbol
    symbol = input(f"\nEnter the stock symbol you are looking for: ")

    # Validate symbol

    # Get chart type
    print(f"\nChart Types")
    print("-----------")
    print("1. Bar")
    print("2. Line")
    chartType = input("Enter the chart type you want (1, 2): ")

    # Validate chart type

    # Get time series
    print(f"\nSelect the time series of the chart you wish to generate")
    print("--------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    chartType = input("Enter the time series option (1, 2, 3, 4): ")

    # Validate chart type

    # Get start date
    startDate = input(f"\nEnter the start date (YYYY-MM-DD): ")

    # Validate start date

    # Get end date
    endDate = input(f"\nEnter the end date (YYYY-MM-DD): ")

    # Validate end date


# Call API to get data
# AlphaVantage API Key:   H1514RX61K8J6SFK

# Manipulate data

# Create graph

# Write HTML wrapper for graph

# Launch HTML in default browser.

# Ask to go again
    go = input(f"\nWould you like to view more stock data? Press 'y' to continue: ")
    if go.lower() != "y":
        keep_going = False

print(f"\nGoodbye")
exit()
