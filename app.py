from flask import Flask, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

API_KEY='YDHNL5VEVABYDX1F'

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if "Note" in data:
        print("Rate limit reached! Waiting 60 seconds...")
        time.sleep(60)
        return get_stock_data(symbol)
        
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    return df.reset_index().to_dict('records')

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    try:
        data = get_stock_data(symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)