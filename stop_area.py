from matplotlib.path import Path as mPath
import mysql.connector
from mysql.connector import Error
import sys

if len(sys.argv) is 1:
    sys.exit('please start this script with a geofence file as argument!')

#geofence
geofence = str(sys.argv[1]) 

def is_point_in_polygon_matplotlib(point, polygon):
    pointTuple = (point['lat'], point['lon'])
    polygonTupleList = []
    for c in polygon:
        coordinateTuple = (c['lat'], c['lon'])
        polygonTupleList.append(coordinateTuple)

    polygonTupleList.append(polygonTupleList[0])
    p = mPath(polygonTupleList)
    return p.contains_point(pointTuple)

def in_area(lat, lon, area):
    point = {'lat': lat, 'lon': lon}
    polygon = area['polygon']
    return is_point_in_polygon_matplotlib(point, polygon)

def parse_geofences_file(geofence_file):
    geofences = []
    # Read coordinates of areas from file.
    if geofence_file:
        with open(geofence_file) as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:  # Empty line.
                    continue
                elif line.startswith("["):  # Name line.
                    name = line.replace("[", "").replace("]", "")
                    geofences.append({
                        'name': name,
                        'polygon': []
                    })
                else:  # Coordinate line.
                    lat, lon = line.split(",")
                    LatLon = {'lat': float(lat), 'lon': float(lon)}
                    geofences[-1]['polygon'].append(LatLon)
    return geofences

try:
   mySQLconnection = mysql.connector.connect(
       host = 'localhost',
       user = '',
       passwd = '',
       database = '')
   sql_select_Query = "SELECT pokestop.latitude, pokestop.longitude FROM pokestop;" 
   cursor = mySQLconnection .cursor()
   cursor.execute(sql_select_Query)
   records = cursor.fetchall()
   cursor.close()

except Error as e :
    print("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(mySQLconnection .is_connected()):
        mySQLconnection.close()

for row in records:
    if in_area(float(row[0]),float(row[1]), parse_geofences_file(geofence)[0]):
        print(str(row[0]) + "," + str(row[1]))
