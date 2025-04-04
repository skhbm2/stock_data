# Resources
# AlphaVantage API Key:   H1514RX61K8J6SFK
# https://www.alphavantage.co/documentation/    (API to get stock info)
# https://requests.readthedocs.io/en/latest/    (code to call API)
# https://www.pygal.org/en/stable/documentation/types/index.html    (graphing tool)
# https://lxml.de/  (tool to create HTML to wrap graph)
import requests
import pygal
import lxml
import webbrowser
import xml.etree.ElementTree as etree

print("Stock Data Visualizer\n\n")
symbol = input("Enter Stock Symbol: \n")
while True:
    chartType = input("\nChart Types\n----------\n1. Bar\n 2. Line\n\nEnter the chart type you want (1, 2): ")
    if chartType == 1 or chartType == 2:
        break
    else:
        print("Please enter 1 or 2")
while True:
    timeSeries = input("Select Time Series: \n1. Interday\n2. Daily\n3. Weekly\n4. Monthly\n")
    if timeSeries == 1 or timeSeries == 2 or timeSeries == 3 or timeSeries == 4:
        break
    else:
        print("Please enter 1, 2, 3, or 4")
start = input("Enter Start Date (YYYY-MM-DD):")
end = input("Enter End Date (YYYY-MM-DD):")
link = ""
info = requests(link)
info.json()



line_chart = pygal.Line()
line_chart.title = 'Browser usage evolution (in %)'
line_chart.x_labels = map(str, range(2002, 2013))
line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
svg = line_chart.render()

# Write HTML wrapper for graph

f = open("graph.html", "w")
filePath = 'graph.html'

content = f"""
{svg}
"""

with open(filePath,'w') as outFile:
    outFile.write(content)


# Launch HTML in default browser.

webbrowser.open(f'{filePath}')
f.close()
