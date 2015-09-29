#!/usr/bin/env python
import socket
import subprocess
import sys
import time
from datetime import datetime


# Ask for input
if len(sys.argv) == 1:
    remoteServer = raw_input("Enter a remote host to scan: ")
else:
    remoteServer = sys.argv[1]


remoteServerIP  = socket.gethostbyname(remoteServer)

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

try:
    ports_to_scan = [22,3306,5900]
    
    for port in ports_to_scan:  
        sys.stdout.write("Scanning Port: %s           \r" % (str(port)))
        sys.stdout.flush() # erases line
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print "Port %s: Open               "  % (str(port))
        sock.close()
        

except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit()

except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

except socket.error:
    print "Couldn't connect to server"
    sys.exit()

# Printing the information to screen
print 'Scanning Completed in: ', datetime.now() - t1
