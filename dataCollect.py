import requests
import pygal
while True:
    symbol = input("Stock Data Visualizer\n---------------------\n\nEnter the Stock Symbol you are searching for or type EXIT to leave the program: ")
    if symbol == "EXIT":
        break
    while True:
        type = input("\nChart Types\n----------\n1. Bar\n 2. Line\n\nEnter the chart type you want (1, 2): ")
        if type == 1 or type == 2:
            break
        else:
            print("Please enter 1 or 2")
    while True:
        series = input("\nSelect the Time Series of the Chart you want\n--------------------------------------------\n1. Interday\n2. Daily\n3. Weekly\n4. Monthly\n\nEnter the time series you want (1, 2, 3, 4): ")
        if series == 1 or series == 2 or series == 3 or series == 4:
            break
        else:
            print("Please enter 1, 2, 3, or 4")
    start = input("\nEnter Start Date (YYYY-MM-DD):")
    end = input("\nEnter End Date (YYYY-MM-DD):")
    link = ""
    info = requests(link)
    info.json()