# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/api/xrp-usdt-price')
def get_xrp_usdt_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'XRP',
        'convert': 'USDT'
    }
    headers = {
        'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'
    }
    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()
    
    # Extract the XRP to USDT price from the response
    if 'XRP' in data['data']:
        xrp_price_usdt = data['data']['XRP']['quote']['USDT']['price']
        return jsonify({'xrp_usdt_price': xrp_price_usdt})
    else:
        return jsonify({'error': 'Unable to fetch XRP price'})

if __name__ == '__main__':
    app.run(debug=True)

