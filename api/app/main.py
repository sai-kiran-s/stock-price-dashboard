from flask import Flask, jsonify
import yfinance as yf
import os
import logging
from kafka import KafkaProducer
import json

app = Flask(__name__)

def convert_keys_to_str(obj):
    if isinstance(obj, dict):
        return {str(k): convert_keys_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_str(i) for i in obj]
    else:
        return obj

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)

        # Convert all keys to strings
        historical_data = convert_keys_to_str(ticker_obj.history(period="1y").to_dict())
        financials = convert_keys_to_str(ticker_obj.financials.to_dict())
        actions = convert_keys_to_str(ticker_obj.actions.to_dict())

        stock_info = {
            "ticker": ticker,
            "historical_data": historical_data,
            "financials": financials,
            "actions": actions
        }

        app.logger.info("Stock info: %s", json.dumps(stock_info, indent=2))

        # Kafka Configuration
        KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )

        producer.send('stock-prices', value=stock_info)
        producer.flush()

        return jsonify({
            "message": f"Stock data for {ticker} sent to Kafka",
            "data": stock_info
        }), 200
    except Exception as e:
        app.logger.error("Error: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
