import pygal
import csv
import requests
from io import StringIO
import lxml
from datetime import datetime 
import webbrowser
import os
from dateutil import parser
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
        chartType = int(input("Enter the chart type you want (1, 2): "))
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
        try:
            dateType = int(input("Enter the time series option (1, 2, 3, 4): "))
        except ValueError:
            print("Please Enter 1, 2, 3, or 4")
        if int(dateType) == 1 or int(dateType) == 2 or int(dateType) == 3 or int(dateType) == 4:
            dateTypeBool = False
        else:
            print("Please Enter 1, 2, 3, or 4")

    # Validate chart type

    # Get start date
    tempDateBool = True
    startDate = ""
    while tempDateBool:
        if dateType == 1:
            tempDate = input(f"\nEarliest avalible date is 2000-01-01.\nEnter the start date (YYYY-MM-DD HH:MM:SS): ")
        else:
            tempDate = input(f"\nEarliest avalible date is 2000-01-01.\nEnter the start date (YYYY-MM-DD): ")
        # Splitting the dates into an array
        try:
            x = parser.parse(tempDate)
        except ValueError:
            continue
        # Checking to make sure the year and month in valid
        if x.year >= 2000 and x.year <= 2025 and x.month >= 1 and x.month <= 12:
            # Checking leap year Febuary
            if x.year % 4 == 0 and x.month == 2 and x.day >= 1 and x.day <= 29:
                startDate = tempDate
                tempDateBool = False
            # Checking Febuary
            elif x.month == 2 and x.day >= 1 and x.day <= 28:
                startDate = tempDate
                tempDateBool = False
            # Checking 30 Day months
            elif (x.month == 4 or x.month == 6 or x.month == 9 or x.month == 11) and x.day <= 30 and x.day >= 1:
                startDate = tempDate
                tempDateBool = False
            # Checking 31 Day Months
            elif (x.month == 1 or x.month == 2 or x.month == 3 or x.month == 5 or x.month == 7 or x.month == 8 or x.month == 10 or x.month == 12) and x.day <= 31 and x.day >= 1:
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
        if dateType == 1:
            tempDate = input(f"\nEnter the end date (YYYY-MM-DD HH:MM:SS): ")
        else:
            tempDate = input(f"\nEnter the end date (YYYY-MM-DD): ")
        # Splitting the dates into an array
        try:
            y = parser.parse(tempDate)
        except ValueError:
            continue
        # Checking to make sure the year and month in valid
        if y.year >= 2000 and y.year <= 2025 and y.month >= 1 and y.month <= 12:
            if y.year == x.year:
                if y.month == x.month:
                    if y.day >= x.day:
                        # Checking leap year Febuary
                        if y.year % 4 == 0 and y.month == 2 and y.day >= 1 and y.day <= 29:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking Febuary
                        elif y.month == 2 and y.day >= 1 and y.day <= 28:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking 30 Day months
                        elif (y.month == 4 or y.month == 6 or y.month == 9 or y.month == 11) and y.day <= 30 and y.day >= 1:
                            endDate = tempDate
                            tempDateBool = False
                        # Checking 31 Day Months
                        elif (y.month == 1 or y.month == 2 or y.month == 3 or y.month == 5 or y.month == 7 or y.month == 8 or y.month == 10 or y.month == 12) and y.day <= 31 and y.day >= 1:
                            endDate = tempDate
                            tempDateBool = False
                        else:
                            print("\nPlease Enter a Valid Date")
                    else:
                        print("\nPlease Enter a Valid Date")
                elif y.month > x.month:
                    endDate = tempDate
                    tempDateBool = False
                else:
                    print("\nPlease Enter a Valid Date")
            elif y.year > x.year:
                endDate = tempDate
                tempDateBool = False
            else:
                print("\nPlease Enter a Valid Date")
        else:
            print("\nPlease Enter a Valid Date")


    # Validate end date

    url = f""
    if dateType == 1:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&outputsize=full&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
    elif dateType == 2:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
    elif dateType == 3:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
    else:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey=NGQOGVZY1A9CYDLK&datatype=csv"

# Call API to get data
# AlphaVantage API Key:   H1514RX61K8J6SFK
    dates = []
    open_price = []
    high_price = []
    low_price = []
    close_price = []
    startFound = False
    noEndFound = True
    firstLineGone = 0
    aquireData = requests.get(url)
    stockData = csv.reader(aquireData.text.strip().split("\n"))
    #intraday requires a timestamp on the date format
    if dateType == 1:
        try:
            strippedStartDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
            strippedEndDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    else:
        strippedStartDate = datetime.strptime(startDate, "%Y-%m-%d")
        strippedEndDate = datetime.strptime(endDate, "%Y-%m-%d")
    next(stockData)
    for row in stockData:
        try:
            if dateType == 1:
                current_dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                if strippedStartDate.date() <= current_dt.date() <= strippedEndDate.date():
                    dates.append(row[0])  
                    open_price.append(float(row[1]))
                    high_price.append(float(row[2]))
                    low_price.append(float(row[3]))
                    close_price.append(float(row[4]))
            else:  
                current_dt = datetime.strptime(row[0], "%Y-%m-%d")
                if strippedStartDate <= current_dt <= strippedEndDate:
                    dates.append(row[0])  
                    open_price.append(float(row[1]))
                    high_price.append(float(row[2]))
                    low_price.append(float(row[3]))
                    close_price.append(float(row[4]))
        except ValueError:
                continue


    dates.reverse()
    open_price.reverse()
    high_price.reverse()
    low_price.reverse()
    close_price.reverse()
    for date in dates:
        print(f"[{date}]")
# Manipulate data

# Create graph
    if chartType == 2:
        line_chart = pygal.Line(x_label_rotation=20)
        line_chart.title = f'{symbol} Stock Data'
        line_chart.x_labels = dates
        line_chart.add('Open', open_price)
        line_chart.add('High', high_price)
        line_chart.add('Low', low_price)
        line_chart.add('Close', close_price)
        svg = line_chart.render()
    elif chartType == 1:
        bar_chart = pygal.Bar(x_label_rotation = 20)
        bar_chart.title = f'{symbol} Stock Data'
        bar_chart.x_labels = dates
        bar_chart.add('Open', open_price)
        bar_chart.add('High', high_price)
        bar_chart.add('Low', low_price)
        bar_chart.add('Close', close_price)
        svg = bar_chart.render()

# Write HTML wrapper for graph
    f = open("graph.html", "w")
    filePath = 'graph.html'

    content = f"""
    {svg}
    """

    with open(filePath,'w') as outFile:
        outFile.write(content)

# Launch HTML in default browser.
    webbrowser.open('file://' + os.path.realpath(filePath))
    f.close()

# Ask to go again
    go = input(f"\nWould you like to view more stock data? Press 'y' to continue: ")
    if go.lower() != "y":
        keep_going = False

print(f"\nGoodbye")
exit()
