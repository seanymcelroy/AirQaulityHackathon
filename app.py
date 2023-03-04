import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# define a simple endpoint that takes a GET request


@app.route('/hello', methods=['GET'])
def hello():
    # df = pd.read_csv('dummy.csv')
    name = request.args.get('coords', 'World')
    return jsonify(f'Hello {name}')

@app.route('/airquality', methods=['GET'])
def getAirQuality():
    # df = pd.read_csv('dummy.csv')
    lat = request.args.get('lat', 'Not prvided')
    long= request.args.get('long', 'Not povided')
    return jsonify(f"Your lat is {lat} and your long is {long}")


if __name__ == '__main__':
    app.run(debug=True)
