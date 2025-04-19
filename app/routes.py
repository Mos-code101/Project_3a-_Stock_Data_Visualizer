from flask import Blueprint, render_template, request
import pandas as pd
import io
import base64
from datetime import datetime
from .api_connection import get_stock_data

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

main = Blueprint('main', __name__)

chart_types = ["Bar", "Line"]
time_series_options = ["Daily", "Weekly", "Monthly"]

def get_stock_symbols():
    try:
        df = pd.read_csv('app/stocks.csv')
        return df['Symbol'].tolist()
    except Exception:
        print("Error reading stock symbols..")
        return ['AAPL', 'MSFT', 'GOOGL']  

@main.route('/', methods=['GET', 'POST'])
def index():
    
    symbols = get_stock_symbols()
    chart = None
    error = None
    selected_symbol = None
    selected_chart_type = None
    selected_time_series = None
    start_date = None
    end_date = None

    if request.method == 'POST':
        
        selected_symbol = request.form.get('symbol')
        selected_chart_type = request.form.get('chart_type')
        selected_time_series = request.form.get('time_series')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not selected_symbol:
            error = "Please select a stock symbol."
        elif not start_date or not end_date:
            error = "Please provide both start and end dates."
        elif selected_chart_type not in chart_types:
            error = "Invalid chart type. Choose Bar or Line."
        elif selected_time_series not in time_series_options:
            error = "Invalid time series. Choose Daily, Weekly, or Monthly."

        if not error:
            stock_data = get_stock_data(selected_symbol, selected_time_series)

            if stock_data:
                try:
                    time_series_key = next((key for key in stock_data if "Time Series" in key), None)
                    
                    if not time_series_key:
                        error = f"No time series data found for {selected_symbol}."
                        return render_template(
                            "index.html", symbols=symbols, chart=chart, error=error,
                            chart_types=chart_types, time_series_options=time_series_options,
                            start_date=start_date, end_date=end_date, 
                            selected_symbol=selected_symbol,
                            selected_chart_type=selected_chart_type,
                            selected_time_series=selected_time_series
                        )
                    
                    df = pd.DataFrame.from_dict(stock_data[time_series_key], orient='index')
                    df.index = pd.to_datetime(df.index)
                    df = df.sort_index()
                    df["Close"] = df["4. close"].astype(float)
                    
                    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                    
                    filtered_df = df.loc[start_dt:end_dt]

                    if not filtered_df.empty:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        if selected_chart_type == "Bar":
                            ax.bar(filtered_df.index, filtered_df["Close"])
                        else:
                            ax.plot(filtered_df.index, filtered_df["Close"])

                        ax.set_title(f"{selected_symbol} Stock Prices ({selected_time_series})")
                        ax.set_ylabel("Price ($)")
                        ax.grid(True, linestyle='--', alpha=0.7)
                        fig.autofmt_xdate()
                        
                        img = io.BytesIO()
                        plt.savefig(img, format='png', dpi=100)
                        img.seek(0)
                        chart = base64.b64encode(img.read()).decode()
                        plt.close()
                    else:
                        error = "No data available for the selected range."
                except ValueError as e:
                    error = f"Invalid date format or range: {e}"
                except Exception as e:
                    error = f"Error processing data: {e}"
            else:
                error = f"No stock data found for {selected_symbol}."

    return render_template(
        "index.html", symbols=symbols, chart=chart, error=error,
        chart_types=chart_types, time_series_options=time_series_options,
        start_date=start_date, end_date=end_date, 
        selected_symbol=selected_symbol,
        selected_chart_type=selected_chart_type,
        selected_time_series=selected_time_series
    )