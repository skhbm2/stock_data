##INFO TECH 4430 - Software Engineering
#Project 3 - Stock Data Visualization
#Scrum Team 2 - Sam Herrmann (Scrum Master), Zoey Benedict, Karson Null, Ken Kreidell

# Resources
# AlphaVantage API Key:   H1514RX61K8J6SFK
# https://www.alphavantage.co/documentation/    (API to get stock info)
# https://requests.readthedocs.io/en/latest/    (code to call API)
# https://www.pygal.org/en/stable/documentation/types/index.html    (graphing tool)
# https://lxml.de/  (tool to create HTML to wrap graph)
import pygal  # First import pygal
import requests
import lxml
import json
import pandas

print(f"\nStock Data Visualizer")
print("------------------------")
api_key = "H1514RX61K8J6SFK"
symbol = "GOOGL"
function = "TIME_SERIES_DAILY"
#url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key}"
url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}"

response = requests.get(url)
data = response.json()

print(f"*** DEBUG ***\n{data}\n***END DEBUG ***")

# Convert the JSON data to a Pandas DataFrame
df = pandas.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
df.index = pandas.to_datetime(df.index)
df = df.sort_index()

# Filter data for a specific date range
start_date = "2025-03-20"
end_date = "2025-03-30"
filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]

# Print the filtered data
print("Filtered by date range:")
print(filtered_df)
#for key, value in filtered_df.items():
#    print(f"Key: {key}")
#    print(f"Values: {value}")

# Trying some stuff...
for key, inner_dict in filtered_df.items():
    print(f"Key: {key}")
    # Loop through the inner dictionary
    for inner_key, value in inner_dict.items():
        print(f"  {inner_key}: {value}")
    

#print(data)
line_chart = pygal.Line()
line_chart.title = 'Stock Data for SYMBOL: DATE to DATE'
line_chart.x_labels = map(str, range(2003, 2006))
line_chart.add('Open', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('High',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('Low',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Close',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
line_chart.render_to_file('chart.svg')                          # Save the svg to a file

from datetime import datetime, timedelta
date_chart = pygal.Line(x_label_rotation=20)
date_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), [
 "2025-03-20",
 datetime(2025, 3, 21),
 datetime(2025, 3, 24),
 datetime(2025, 3, 25),
 datetime(2025, 3, 26),
 datetime(2025, 3, 27),
 datetime(2025, 3, 28)])
date_chart.add("Open", [300, 412, 823, 672])
date_chart.add("High", [200, 312, 723, 572])
date_chart.add("Low", [100, 212, 623, 472])
date_chart.add("Close", [1, 112, 523, 472])
date_chart.render_to_file('chart2.svg')

exit() #Quit before we get into the main body.  This is just for debugging.


keep_going = True
while keep_going:

# Collect graph parameters

    # Get symbol
    #symbol = input(f"\nEnter the stock symbol you are looking for: ")

    # Validate symbol

    # Get chart type
    print(f"\nChart Types")
    print("-----------")
    print("1. Bar")
    print("2. Line")
    #chartType = input("Enter the chart type you want (1, 2): ")

    # Validate chart type

    # Get time series
    print(f"\nSelect the time series of the chart you wish to generate")
    print("--------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    #chartType = input("Enter the time series option (1, 2, 3, 4): ")

    # Validate chart type

    # Get start date
    #startDate = input(f"\nEnter the start date (YYYY-MM-DD): ")

    # Validate start date

    # Get end date
    #endDate = input(f"\nEnter the end date (YYYY-MM-DD): ")

    # Validate end date


    # Call API to get data
    # AlphaVantage API Key:   H1514RX61K8J6SFK
    # https://requests.readthedocs.io/en/latest/    (code to call API)
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=TSCO.LON&apikey=H1514RX61K8J6SFK'
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=H1514RX61K8J6SFK'
    #r = requests.get(url)
    #data = r.json()
    #print(data)
    
    # Transform json input to python objects
    #input_dict = json.loads(data)

    # Filter python objects with list comprehensions
    #output_dict = [x for x in input_dict if x['Monthly Time Series'] == '1']

    # Transform python object back into json
    #output_json = json.dumps(output_dict)

    # Show json
    #print(output_json)

    print(data)
    
    # Manipulate data

    # Create graph



    bar_chart = pygal.Bar()                                            # Then create a bar graph object
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file

    # Write HTML wrapper for graph

    # Launch HTML in default browser.

    # Ask to go again
    go = input(f"\nWould you like to view more stock data? Press 'y' to continue: ")
    if go.lower() != "y":
        keep_going = False

print(f"\nGoodbye")
exit()
