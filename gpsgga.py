# Python 3.6.1
import serial
import math

# Serial port settings
gps = serial.Serial()
gps.baudrate = 9600
gps.port = "COM2"

# Read GPS output from USB via COM2
gps.open()

a = gps.is_open
print("Port is open: " + str(a) + "\n")

while True:
	line = gps.readline().decode()
	dataraw = line.split("\r\n")	
	#data = dataraw[0].split(",")
	data = line.split(",")
  
  	# Find GGA messages
	if data[0] == "$GPGGA":
		if data[6] > "0":
			# GPS Latitude
      			latgps = float(data[2])
			if data[3] == "S":
				latgps = -latgps
			
			latdeg = int(latgps/100)
			latmin = latgps - latdeg*100
			lat = latdeg + (latmin/60)
			
      			# GPS Longitude
			longps = float(data[4])
			if data[5] == "W":
				longps = -longps
			
			londeg = int(longps/100)
			lonmin = longps - londeg*100
			lon = londeg + (lonmin/60)
			
      			# GPS Altitude
			altitude = data[9]
			altitude_unit = data[10]
			
			# GPS Time
			timeUTC = data[1][0:2] + ":" + data[1][2:4] + ":" + data[1][4:6]
			
	# Display GPS coordinates (GGA)
	print(timeUTC + ", " + str(lat) + ", " + str(lon) + ", " + str(altitude))
			
	# Save GGA messages to a text file
	with open("position.txt", "a") as pos:
		pos.write(timeUTC + ", " + str(lat) + ", " + str(lon) + ", " + str(altitude) + "\n")
		#pos.close()