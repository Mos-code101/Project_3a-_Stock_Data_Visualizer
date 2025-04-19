import pygal
from datetime import datetime

def filter_stock_data(stock_data, start_date, end_date):
   
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    time_series_key = next((key for key in stock_data if "Time Series" in key), None)

    if not time_series_key:
        print("Invalid stock data format.")
        return None, None

    filtered_data = {
        date: float(data['4. close'])
        for date, data in stock_data[time_series_key].items()
        if start_date <= datetime.strptime(date, "%Y-%m-%d") <= end_date
    }

    sorted_dates = sorted(filtered_data.keys())
    sorted_prices = [filtered_data[date] for date in sorted_dates]

    return sorted_dates, sorted_prices


def graph_generator(chart_type, dates, prices):
    chart_types = {
        "Line": pygal.Line,
        "Bar": pygal.Bar
    }

    if chart_type not in chart_types:
        print("Invalid chart type.")
        return None

    chart = chart_types[chart_type]()  

    chart.title = "Stock Prices Over Time"
    chart.x_labels = dates
    chart.add("Stock Price", prices)

    chart.render_in_browser()
