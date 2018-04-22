# PythonGPS
1. Connect USB/Serial GPS device via COM port and display current position (latitude & longitude in WGS84).
2. File gpsrmc.py - Utilizes $GPRMC NMEA message and output position to KML file. View the KML file via Google Earth application.
3. File gpsgga.py - Uses $GPGGA NMEA message and output to a text file.
4. File rtklib_socket_read.py - Read NMEA output from RTKLIB application via socket programming. Output the coordinate as KML file. View the KML file via Google Earth application (Add > Network Link)
