import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import geopandas as gpd
from shapely.geometry import Point

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
    lat = request.args.get('lat', 53.3463684)
    long= request.args.get('long', -6.244145158699778)
    road_segments = gpd.read_file('airview_dublincity_roaddata_shp')
    valid_roads = road_segments.dropna(subset="PM25_ugm3")

    color_dict = {'< 2': '#84B856',
              '2 - 4': '#B2DF8A',
              '4 - 8': '#CCD677',
              '8 - 12': '#FFC756',
              '12 - 16': '#FF8713',
              '16 - 20': '#F54E00',
              '20 - 24': '#D81730',
              '24 - 28': '#B50130',
              '28 - 32': '#8B1D69',
              '> 32': '#6A3D9A'}

    bins = [-float('inf'), 2, 4, 8, 12, 16, 20, 24, 28, 32, float('inf')]
    labels = ['< 2', '2 - 4', '4 - 8', '8 - 12', '12 - 16', '16 - 20', '20 - 24', '24 - 28', '28 - 32', '> 32']


    valid_roads['pm2_5_colors'] = pd.cut(road_segments['PM25_ugm3'], bins=bins, labels=labels).map(color_dict)
    first_five_rows = valid_roads.head(5).to_dict(orient='records')

    # Step 1. turn road data into distance calculable ITM
    itm_crs = 'EPSG:2157'
    valid_roads_pcs = valid_roads.to_crs(itm_crs)

    # Step 2. Take house and turn it into geo dataframe
    house_gcs = gpd.GeoDataFrame(geometry=[Point(long, lat)], crs='EPSG:4326')

    # Step 3. Convert house into distance calculable ITM
    house_pcs= house_gcs.to_crs(itm_crs)

    # Step 4. add buffer zone
    buffer_distance=200
    house_zone_pcs = gpd.GeoDataFrame(geometry=house_pcs['geometry'].buffer(buffer_distance), crs=itm_crs)

    # Step 5. Spatial join on intersection
    intersecting_roads = gpd.sjoin(valid_roads_pcs, house_zone_pcs, predicate='intersects')

    # Step 6. return simple mean
    simple_pm2_5_mean=intersecting_roads['PM25_ugm3'].mean()
    return jsonify(f"Your lat is {lat} and your long is {long}. Number of road segments {len(road_segments)} Mean pm2_5 in 200m radius: {simple_pm2_5_mean}")


if __name__ == '__main__':
    app.run(debug=True)
