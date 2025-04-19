import requests

def get_stock_data(stock_symbol, time_series):
    
    base_url = "https://www.alphavantage.co/query"

    time_series_options = {
        "Daily": "TIME_SERIES_DAILY",
        "Weekly": "TIME_SERIES_WEEKLY",
        "Monthly": "TIME_SERIES_MONTHLY"
    }

    if time_series not in time_series_options:
        print("Invalid time series.")
        return None

    params = {
        "function": time_series_options[time_series],
        "symbol": stock_symbol,
        "apikey": "HJAWPZECXKX9XKXA",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if "Error Message" in data:
            print(f"Error from API: {data['Error Message']}")
            return None
            
        time_series_key = next((key for key in data if "Time Series" in key), None)
        
        if not time_series_key:
            print("No time series data found.")
            return None

        return data
    else:
        print(f"API request failed. Status code: {response.status_code}")
        return None