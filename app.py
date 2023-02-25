import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# define a simple endpoint that takes a GET request
@app.route('/hello', methods=['GET'])
def hello():
    df = pd.read_csv('dummy.csv')
    name = request.args.get('name', 'World')
    response = {'message': f'Hello, {name}!'}
    # return jsonify(response)
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
