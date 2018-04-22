# Python v3.6.5
# Read NMEA output from RTKlib software (using output option: TCP Server, with port 50006)
# using Socket programming
# 
# Developer: Dr. Ivin Amri Musliman
# Updated: 20 April 2018

import socket
import sys, os
import time

# Read from localhost IP. Do NOT use 127.0.0.1 or "locahost" as the host!
host = socket.gethostname() # or host = "192.168.1.2"

port = 50006
address = (host, port)
buffer_size = 4096

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
except socket.error as e:
	print("Error creating socket: %s \n" % e)
	time.sleep(2)
	sys.exit(1)

try:
	# Connect to the socket
	client.connect(address)

	while True:
		try:
			data = client.recv(buffer_size)
			if not data:
				print ("\nDisconnected from server")
				break

			else:
				lines = data.decode("utf-8").split("\r\n")
	
				# f = open("socks.txt","a+")
				# f.write(data.decode("utf-8"))
				try:
					# dataGPS = lines
					## If using RTKlib software to output the NMEA, enable the line below, else use the line above.
					dataGPS = [i.split(",") for i in lines]
					
					# Assign new variable name to NMEA message
					dataRMC = dataGPS[0]
					dataGGA = dataGPS[1]
					
					# Read $GPGGA message to get the altitude and northing easting (LatLong) accurately
					if dataGGA[0] == "$GPGGA":
						if dataGGA[6] != "0":
							if dataGGA[6] == "1":
								print("GPS fix (SPS)")
							elif dataGGA[6] == "2":
								print("DGPS fix")
							elif dataGGA[6] == "3":
								print("PPS fix")
							elif dataGGA[6] == "4":
								print("Real Time Kinematic")
							elif dataGGA[6] == "5":
								print("Float RTK")
							elif dataGGA[6] == "6":
								print("estimated (dead reckoning)")
							
							altitude = dataGGA[9]
					
					# Read $GPRMC message to get the minimum recommended position (LatLong)
					if dataRMC[0] == "$GPRMC":
						# If data is available/valid (code: A) else code: 0
						if dataRMC[2] == "A":
							latgps = float(dataRMC[3])
							if dataRMC[4] == "S":
								latgps = -latgps
							
							latdeg = int(latgps/100)
							latmin = latgps - latdeg*100
							lat = latdeg + (latmin/60)
							
							longps = float(dataRMC[5])
							if dataRMC[6] == "W":
								longps = -longps
							
							londeg = int(longps/100)
							lonmin = longps - londeg*100
							lon = londeg + (lonmin/60)
							
							# Output coordinates + altitude
							print(str(round(lat,6)) + ", " + str(round(lon,6)) + ", " + altitude)

						# Output / write to KML file. Code must aligned with (if dataRMC[2] == "A"). Create KML file if data is available/valid.
						with open("position.kml", "w") as pos:
							pos.write(
							"""<?xml version="1.0" encoding="UTF-8"?>
								<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
								<Document>
									<Style id="randomLabelColor">
										<LabelStyle>
											<color>ff0000cc</color>
											<colorMode>random</colorMode>
											<scale>1.5</scale>
										</LabelStyle>
								   </Style>
									<Placemark>
										<Style>
											<IconStyle>
												<Icon>
													<href>root://icons/palette-3.png</href>
													<x>64</x>
													<y>32</y>
													<w>32</w>
													<h>32</h>
												</Icon>
											</IconStyle>
										</Style>
										<name>%.6f, %.6f, %sm</name>
										<description>My Current Position via real-time GPS</description>
										<!--<styleUrl>#randomLabelColor</styleUrl>-->
										<Point>
											<coordinates>%s,%s,%s</coordinates>
											<altitudeMode>relativeToGround</altitudeMode>
											<extrude>1</extrude>
										</Point>
									</Placemark>
								</Document>
								</kml>""" % (round(lat,6),round(lon,6),altitude,lon,lat,altitude))

				except NameError as e:
					print("Name error: " + str(e))
				except AttributeError as e:
					print("Attribute error: " + str(e))
				except IOError as e:
					print("I/O error ({0}): {1}".format(e.errno, e.strerror))
				except ValueError:
					print("Could not convert data to an integer.")
				except:
					print("Unexpected error:", sys.exc_info()[0])
					raise
		
		# Handling error if connect to socket is False
		except TypeError as e:
			print("Type error: " + str(e))
		except socket.error as e:
			print("Error receiving data: %s" % e)
			time.sleep(3)
			sys.exit(1)

	# f.close()
	# Close socket connection if False, a.k.a "not connected"
	client.close()

except KeyboardInterrupt:
	print("\nProcess interrupted by user\nClosing...")
	time.sleep(3)
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)
	
except socket.gaierror as e:
	print("Address-related error connecting to server: %s \n" % e)
	time.sleep(3)
	sys.stdout.flush()
	sys.exit(0)

except socket.error as e:
	print("Connection Error: %s \n" % e)
	time.sleep(3)
	sys.stdout.flush()
	sys.exit(0)