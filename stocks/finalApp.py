from flask import Flask, request
import pygal
import csv
import requests
from datetime import datetime
from dateutil import parser

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def stock_visualizer():
    stocks = ""
    with open('stocks.csv', 'r') as read_obj: 
        csv_reader = csv.reader(read_obj) 
        stock_list = list(csv_reader) 
        for sublist in stock_list:
            stocks += f"<option value=\"{sublist[0]}\">{sublist[0]} - {sublist[1]} ({sublist[2]})</option>\r\n"
            
            
    chart_svg = ""
    error = ""
    form_html = f'''
        <h1>Stock Data Visualizer</h1>
        <form method="POST">
            <label>Stock Symbol:</label>
            <select name="symbol">
            {stocks}
            </select><br><br>

            <label>Chart Type:</label>
            <select name="chartType">
                <option value="1">Bar</option>
                <option value="2">Line</option>
            </select><br><br>

            <label>Time Series:</label>
            <select name="timeSeries">
                <option value="1">Intraday</option>
                <option value="2">Daily</option>
                <option value="3">Weekly</option>
                <option value="4">Monthly</option>
            </select><br><br>

            <label>Start Date:</label>
            <input type="date" name="startDate" placeholder="YYYY-MM-DD" required><br><br>
            
            <label>Start Time(for intraday only):</label>
            <input type="time" name="startTime" placeholder="If not intraday, leave blank" ><br><br>

            <label>End Date:</label>
            <input type="date" name="endDate" placeholder="YYYY-MM-DD" required><br><br>
            
            <label>End Time(for intraday only):</label>
            <input type="time" name="endTime" placeholder="If not intraday, leave blank" ><br><br>

            <button type="submit">Generate Chart</button>
        </form>
    '''

    if request.method == "POST":
        try:
            symbol = request.form["symbol"].upper()
            chartType = int(request.form["chartType"])
            dateType = int(request.form["timeSeries"])
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]

            if dateType == 1:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&outputsize=full&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
            elif dateType == 2:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
            elif dateType == 3:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey=NGQOGVZY1A9CYDLK&datatype=csv"
            else:
                url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey=NGQOGVZY1A9CYDLK&datatype=csv"

            dates = []
            open_price = []
            high_price = []
            low_price = []
            close_price = []

            if dateType == 1:
                startTime = request.form.get("startTime", "00:00")
                endTime = request.form.get("endTime", "23:59")
                
                startDate = f"{startDate} {startTime}:00"
                endDate = f"{endDate} {endTime}:00"
                
                strippedStartDate = datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
                strippedEndDate = datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
            else:
                strippedStartDate = datetime.strptime(startDate, "%Y-%m-%d")
                strippedEndDate = datetime.strptime(endDate, "%Y-%m-%d")

            aquireData = requests.get(url)
            stockData = csv.reader(aquireData.text.strip().split("\n"))
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

            if chartType == 2:
                chart = pygal.Line(x_label_rotation=20)
            else:
                chart = pygal.Bar(x_label_rotation=20)

            chart.title = f'{symbol} Stock Data'
            chart.x_labels = dates
            chart.add('Open', open_price)
            chart.add('High', high_price)
            chart.add('Low', low_price)
            chart.add('Close', close_price)

            chart_svg = chart.render().decode('utf-8')

        except Exception as e:
            error = f"<p style='color:red;'>Error: {str(e)}</p>"

    return f"""
        <html>
            <head><title>Stock Visualizer</title></head>
            <body>
                {form_html}
                {error}
                {chart_svg}
            </body>
        </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
