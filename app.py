from flask import Flask, jsonify, request

app = Flask(__name__)

# define a simple endpoint that takes a GET request
@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name', 'World')
    response = {'message': f'Hello, {name}!'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
