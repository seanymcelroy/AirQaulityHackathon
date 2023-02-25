from flask import Flask, jsonify
# from shapely.geometry import Point
# from geopandas.tools import geodesic_buffer


app = Flask(__name__)


@app.route('/hello')
def hello():
    response = {'message': 'Hello, World!'}
    # point_of_interest = Point(-73.9869, 40.7484)
    # buffer_radius = 100  # in meters

    # buffer = geodesic_buffer(point_of_interest, buffer_radius)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
