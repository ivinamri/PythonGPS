# Python 3.6.1
import serial
import math

# Serial port settings
gps = serial.Serial()
gps.baudrate = 9600
gps.port = "COM4"

# Read GPS output from USB via COM4
gps.open()

a = gps.is_open
print("Port is open: " + str(a) + "\n")

while True:
	line = gps.readline().decode()
	dataraw = line.split("\r\n")	
	#data = dataraw[0].split(",")
	data = line.split(",")
  
  	# Find $GPRMC messages
	if data[0] == "$GPRMC":
		# Make sure GPS is active
		if data[2] == "A":
			# GPS Latitude
			latgps = float(data[3])
			if data[4] == "S":
				latgps = -latgps
			
			latdeg = int(latgps/100)
			latmin = latgps - latdeg*100
			lat = latdeg + (latmin/60)
			
			# GPS Longitude
			longps = float(data[5])
			if data[6] == "W":
				longps = -longps
			
			londeg = int(longps/100)
			lonmin = longps - londeg*100
			lon = londeg + (lonmin/60)
			
			# Display GPS coordinates
			print(str(lat) + ", " + str(lon))
			
			# Save current GPS position to KML file. View real-time GPS position updates from Google Earth application.
			with open("position.kml", "w") as pos:
				pos.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
	<Placemark>
		<name>My Current Position</name>
		<description>Real-time GPS</description>
		<Point>
			<coordinates>%s,%s,0</coordinates>
		</Point>
	</Placemark>
</kml>""" % (lon,lat))