# INFO TECH 4430 - Software Engineering
# Project 3 - Stock Data Visualization
# Scrum Team 2 - Sam Herrmann (Scrum Master), Zoey Benedict, Karson Null, Ken Kreidell

import requests
import pygal
import webbrowser
from datetime import datetime
import os

print(f"\nStock Data Visualizer")
print("------------------------")

def date_validation(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

keep_going = True
while keep_going:

    # Collect graph parameters
    symbol = input(f"\nEnter the stock symbol you are looking for: ").upper().strip()

    print(f"\nChart Types")
    print("-----------")
    print("1. Bar")
    print("2. Line")
    chartType = input("Enter the chart type you want (1, 2): ")
    while chartType not in ["1", "2"]:
        chartType = input("Please enter 1 or 2 for chart type.")

    print(f"\nSelect the time series of the chart you wish to generate")
    print("--------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    timeSeries = input("Enter the time series option (1, 2, 3, 4): ")
    while timeSeries not in ["1", "2", "3", "4"]:
        timeSeries = input("Please enter 1, 2, 3, or 4 for the type of chart you want to generate.")

    startDateStr = input(f"\nEnter the start date (YYYY-MM-DD): ")
    startDate = date_validation(startDateStr)
    while not startDate:
        startDateStr = input("Please enter the date in YYYY-MM-DD format.")
        startDate = date_validation(startDateStr)

    endDateStr = input(f"\nEnter the end date (YYYY-MM-DD): ")
    endDate = date_validation(endDateStr)
    while not endDate or endDate < startDate:
        if not endDate:
            endDateStr = input("Please enter the date in YYYY-MM-DD format.")
        else:
            print("End date cannot be before start date.")
            endDateStr = input("Enter the end date (YYYY-MM-DD): ")
        endDate = date_validation(endDateStr)

    if timeSeries == "1":
        alphaFunction = "TIME_SERIES_INTRADAY"
        paramaters = {"interval": "5min"}
        timeSeriesKey = "Time Series (5min)"
    elif timeSeries == "2":
        alphaFunction = "TIME_SERIES_DAILY"
        paramaters = {}
        timeSeriesKey = "Time Series (Daily)"
    elif timeSeries == "3":
        alphaFunction = "TIME_SERIES_WEEKLY"
        paramaters = {}
        timeSeriesKey = "Weekly Time Series"
    else:
        alphaFunction = "TIME_SERIES_MONTHLY"
        paramaters = {}
        timeSeriesKey = "Monthly Time Series"

    apiKey = "H1514RX61K8J6SFK"
    url = "https://www.alphavantage.co/query"
    parameters = {"function": alphaFunction, "symbol": symbol, "apikey": apiKey}
    paramaters.update(parameters)
    print("\nGetting data from Alpha Vantage....")
    response = requests.get(url, params=parameters)
    if response.status_code != 200:
        print("Having troubles fetching data. Please try again.")
        continue
    data = response.json()
    if "Error Message" in data or "Note" in data or timeSeriesKey not in data:
        print("API Key Error:", data.get("Error Message", data.get("Note", "Data not available.")))
        continue

    timeSeriesData = data[timeSeriesKey]
    filteredDates = []
    filteredPrices = []
    for dateStr, daily in timeSeriesData.items():
        try:
            currentDate = datetime.strptime(dateStr[:10], "%Y-%m-%d")
        except:
            continue
        if startDate <= currentDate <= endDate:
            filteredDates.append(currentDate)
            filteredPrices.append(float(daily["4. close"]))
