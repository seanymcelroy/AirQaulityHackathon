import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import geopandas as gpd
from shapely.geometry import Point

app = Flask(__name__)

# Allow cross origin
CORS(app)


road_segments = gpd.read_file('airview_dublincity_roaddata_shp')
valid_pm_roads = road_segments.dropna(subset="PM25_ugm3")


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(f'Hello World')

@app.route('/airquality/pm2_5', methods=['GET'])
def get_fine_particulate_matter():
    lat = request.args.get('lat')
    long= request.args.get('long')

    if not is_valid_lat_long(lat,long):
        response = {
            "error": "Invalid latitude and/or longitude",
            "message": "Please send a valid latitude and longitude.",
            "example": "airquality/pm2_5?lat=53.34372592082202&long=-6.307261762132252"
        }
        return jsonify(response)

    # Step 1. turn road data into distance calculable ITM
    valid_roads_pcs = valid_pm_roads.to_crs(get_irish_coordinate_system())

    # Step 2. Take house and turn it into geo dataframe
    house_gcs = gpd.GeoDataFrame(geometry=[Point(long, lat)], crs=get_wgs84_coordinate_system())

    # Step 3. Convert house into distance calculable ITM
    house_pcs= house_gcs.to_crs(get_irish_coordinate_system())

    # Step 4. add buffer zone
    BUFFER_DISTANCE=200
    house_zone_pcs = gpd.GeoDataFrame(geometry=house_pcs['geometry'].buffer(BUFFER_DISTANCE), crs=get_irish_coordinate_system())

    # Step 5. Spatial join on intersection
    intersecting_roads = gpd.sjoin(valid_roads_pcs, house_zone_pcs, predicate='intersects')

    # Step 6. return simple mean
    simple_pm2_5_mean=intersecting_roads['PM25_ugm3'].mean()

    response={
        'latitude': lat,
        'longitude': long,
        'buffer_distance_meters': BUFFER_DISTANCE,
        'mean_pm25_ugm3': simple_pm2_5_mean
    }
    return jsonify(response)


def is_valid_lat_long(lat, long):
    try:
        lat = float(lat)
        long = float(long)
    except (TypeError, ValueError):
        return False

    if -90 <= lat <= 90 and -180 <= long <= 180:
        return True
    else:
        return False

def get_irish_coordinate_system():
    IRISH_TRANVERSE_MERCATOR="EPSG:2157"
    return IRISH_TRANVERSE_MERCATOR

def get_wgs84_coordinate_system():
    WGS_84 = "EPSG:4326"
    return WGS_84

if __name__ == '__main__':
    app.run(debug=True)
