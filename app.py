import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# define a simple endpoint that takes a GET request


@app.route('/pollution', methods=['GET'])
def hello():
    df = pd.read_csv('dummy.csv')
    lat = request.args.get('lat', 'N/a')
    long = request.args.get('long', 'N/a')
    response = {
        'message': f'Here is your lat: {lat}, Here is your long: {long}!'}
    return jsonify(response)
    # data = df.to_dict(orient='records')
    # return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
