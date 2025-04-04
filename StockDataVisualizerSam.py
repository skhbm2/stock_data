import pygal
import csv
import requests
from io import StringIO
import lxml
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
    symbol = ""
    symbolBool = True
    while symbolBool:
        symbol = input(f"\nEnter the stock symbol you are looking for: ")
        symbol = symbol.upper()
        if symbol.isalpha() and len(symbol) <= 5:
            symbolBool = False
        else:
            print("\nYour Symbol doesn't exist")


    # Validate symbol

    # Get chart type
    chartBool = True
    chartType = 0
    while chartBool:
        print(f"\nChart Types")
        print("-----------")
        print("1. Bar")
        print("2. Line")
        chartType = input("Enter the chart type you want (1, 2): ")
        if int(chartType) == 1 or int(chartType) == 2:
            chartBool = False
        else:
            print("Please enter 1 or 2")

    # Validate chart type

    # Get time series
    dateTypeBool = True
    dateType = 0
    while dateTypeBool:
        print(f"\nSelect the time series of the chart you wish to generate")
        print("--------------------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")
        dateType = input("Enter the time series option (1, 2, 3, 4): ")
        if int(dateType) == 1 or int(dateType) == 2 or int(dateType) == 3 or int(dateType) == 4:
            dateTypeBool = False
        else:
            print("Please Enter 1, 2, 3, or 4")

    # Validate chart type

    # Get start date
    tempDateBool = True
    startDate = ""
    while tempDateBool:
        tempDate = input(f"\nEarliest avalible date is 2000-01-01.\nEnter the start date (YYYY-MM-DD): ")
        # Splitting the dates into an array
        x = tempDate.split("-")
        # Checking to make sure the year and month in valid
        if int(x[0]) >= 2000 and int(x[0]) <= 2025 and int(x[1]) >= 1 and int(x[1]) <= 12:
            # Checking leap year Febuary
            if int(x[0]) % 4 == 0 and int(x[1]) == 2 and int(x[2]) >= 1 and int(x[1]) <= 29:
                startDate = tempDate
                tempDateBool = False
            # Checking Febuary
            elif int(x[1]) == 2 and int(x[2]) >= 1 and int(x[2]) <= 28:
                startDate = tempDate
                tempDateBool = False
            # Checking 30 Day months
            elif (int(x[1]) == 4 or int(x[1]) == 6 or int(x[1]) == 9 or int(x[1]) == 11) and int(x[2]) <= 30 and int(x[2]) >= 1:
                startDate = tempDate
                tempDateBool = False
            # Checking 31 Day Months
            elif (int(x[1]) == 1 or int(x[1]) == 2 or int(x[1]) == 3 or int(x[1]) == 5 or int(x[1]) == 7 or int(x[1]) == 8 or int(x[1]) == 10 or int(x[1]) == 12) and int(x[2]) <= 31 and int(x[2]) >= 1:
                startDate = tempDate
                tempDateBool = False
            else:
                print("\nPlease Enter a Valid Date")
        else:
            print("\nPlease Enter a Valid Date")


    # Validate start date

    # Get end date
    tempDateBool = True
    endDate = ""
    while tempDateBool:
        tempDate = input(f"\nEnter the end date (YYYY-MM-DD): ")
        # Splitting the dates into an array
        y = tempDate.split("-")
        # Checking to make sure the year and month in valid
        if int(y[0]) >= 2000 and int(y[0]) <= 2025 and int(y[1]) >= 1 and int(y[1]) <= 12:
            if int(y[0]) == int(x[0]):
                if int(y[1]) == int(x[1]):
                    if int(y[2]) >= int(x[2]):
                        # Checking leap year Febuary
                        if int(y[0]) % 4 == 0 and int(y[1]) == 2 and int(y[2]) >= 1 and int(y[1]) <= 29:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking Febuary
                        elif int(y[1]) == 2 and int(y[2]) >= 1 and int(y[2]) <= 28:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking 30 Day months
                        elif (int(y[1]) == 4 or int(y[1]) == 6 or int(y[1]) == 9 or int(y[1]) == 11) and int(y[2]) <= 30 and int(y[2]) >= 1:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking 31 Day Months
                        elif (int(y[1]) == 1 or int(y[1]) == 2 or int(y[1]) == 3 or int(y[1]) == 5 or int(y[1]) == 7 or int(y[1]) == 8 or int(y[1]) == 10 or int(y[1]) == 12) and int(y[2]) <= 31 and int(y[2]) >= 1:
                            endDate = tempDate
                            tempDateBool = False
                        else:
                            print("\nPlease Enter a Valid Date")
                    else:
                        print("\nPlease Enter a Valid Date")
                elif int(y[1]) > int(x[1]):
                    endDate = tempDate
                    tempDateBool = False
                else:
                    print("\nPlease Enter a Valid Date")
            elif int(y[0]) > int(x[0]):
                endDate = tempDate
                tempDateBool = False
            else:
                print("\nPlease Enter a Valid Date")
        else:
            print("\nPlease Enter a Valid Date")


    # Validate end date

    url = f""
    if dateType == 1:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&outputsize=full&apikey=H1514RX61K8J6SFK&datatype=csv"
    elif dateType == 2:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey=H1514RX61K8J6SFK&datatype=csv"
    elif dateType == 3:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey=H1514RX61K8J6SFK&datatype=csv"
    else:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey=H1514RX61K8J6SFK&datatype=csv"

# Call API to get data
# AlphaVantage API Key:   H1514RX61K8J6SFK
    dates = []
    open = []
    high = []
    low = []
    close = []
    startFound = False
    noEndFound = True
    firstLineGone = 0
    aquireData = requests.get(url)
    stockData = csv.reader(aquireData.text.strip().split("\n"))
    for row in stockData:
        print(row)
        if firstLineGone > 0:    
            temp = str(row[0]).split('-')
            print(temp)
            if not startFound:
                if int(temp[0]) == int(x[0]) and int(temp[1]) == int(x[1]) and int(temp[2]) <= int(x[2]):
                    startFound = True
                    dates.append(float(row[0]))
                    open.append(float(row[1]))
                    high.append(float(row[2]))
                    low.append(float(row[3]))
                    close.append(float(row[4]))
            elif startFound and noEndFound:
                if int(temp[0]) == int(y[0]) and int(temp[1]) == int(y[1]) and int(temp[2]) == int(y[2]):
                    noEndFound = False
                    dates.append(float(row[0]))
                    open.append(float(row[1]))
                    high.append(float(row[2]))
                    low.append(float(row[3]))
                    close.append(float(row[4]))
                elif int(temp[0]) == int(y[0]) and int(temp[1]) == int(y[1]) and int(temp[2]) < int(y[2]):
                    noEndFound = False
                elif int(temp[0]) == int(y[0]) and int(temp[1]) == int(y[1])-1:
                    noEndFound = False
                elif int(temp[0]) == int(y[0])-1:
                    noEndFound = False
                else:
                    dates.append(float(row[0]))
                    open.append(float(row[1]))
                    high.append(float(row[2]))
                    low.append(float(row[3]))
                    close.append(float(row[4]))
        firstLineGone = firstLineGone + 1


    dates.reverse()
    open.reverse()
    high.reverse()
    low.reverse()
    close.reverse()
    for date in dates:
        print(f"[{date}]")
# Manipulate data

# Create graph
    if chartType == 1:
        line_chart = pygal.Line()
        line_chart.title = f'{symbol} Stock Data'
        line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.add('Open', )
        line_chart.add('High', )
        line_chart.add('Low', )
        line_chart.add('Close', )
    elif chartType == 2:
        bar_chart = pygal.Bar()

# Write HTML wrapper for graph

# Launch HTML in default browser.

# Ask to go again
    go = input(f"\nWould you like to view more stock data? Press 'y' to continue: ")
    if go.lower() != "y":
        keep_going = False

print(f"\nGoodbye")
exit()
