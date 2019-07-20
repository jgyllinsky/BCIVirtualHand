#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Quadrant_Hand_Signs.py
#  
#  Copyright 2019 Joshua Gyllinsky  <jgyllinsky@my.uri.edu>
#  
#
# Copyright Joshua Gyllinsky. All rights reserved. Licensed under GPL (version 3.0).
#
# #########
#
# ~ 2019-07-20  Joshua Gyllinsky  <jgyllinsky@my.uri.edu>
# ~
# ~ * Forked from my BCI2000 code from last December.
#
# #########
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  



## Includes

import socket
import sys


## Global Variables

### Networking Variables
UDP_IP_ADDRESS = '' #> Address used by UDP protocol; The blank string allows for a non-specific IP to bind to. This is useful if there are more than one network interfaces that the local computer identifies as.
UDP_PORT_NO = 8888 #> Port to bind to. Given the {UDP_IP_ADDRESS = ''}, this binds as *:8888

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #> serverSocket to listen to for UDP messages
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO)) #> Bind to it

# https://stackoverflow.com/questions/38478913/delay-when-receiving-udp-packets-in-python-in-real-time
#serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1) #> Maybe be useful
serverSock.settimeout(0.1)

data = '' #> Blank data for incoming stream
addr = '' #> Blank data for incoming stream
d = [b'','']
     
counter = 0



### Location of Cursor Variables
myX = 0
myY = 0
hand_state = "state_01"

MAX_Y = 1
MAX_X = 0
MIN_Y = 1
MIN_X = 0

while True:
	print ('X,Y = ' + str(myX) + ' , ' + str(myY)+ ' (' + hand_state +') at loop #: ' +str(counter))
	try:
		d = serverSock.recvfrom(1024)
	except socket.timeout:
		print ('caught a timeout...')
	
		
	if(d):
		data = d[0]
		addr = d[1]
		counter = counter+1 
	 
		if not data: 
			# Something unhappy happened.
			break
	 
		reply = 'OK, Data was..' + str(data)
	 
		reply = reply.encode()
		serverSock.sendto(reply , addr)

		val_d =  data.strip()

		val = val_d


		if( 'CursorPosX'.encode() in val ):
			#print val
			#print val.lstrip().split()
			obj = val.decode().lstrip().split()
			myX = obj[1]
			#print 'X = ' + str(myX)
		if( 'CursorPosY'.encode() in val ):
			#print val
			#print val.lstrip().split()
			obj = val.decode().lstrip().split()
			myY = obj[1]
			#print 'Y = ' + str(obj[1])
	
		if(int(myX) >= 3200):
			ser.write("1\r\n".encode())
			#cc=str(ser.readline())
			#print (cc[2:][:-5])
			hand_state = "Open"

		if(int(myX) <= 900):
			ser.write("2\r\n".encode())
			hand_state = "Close"
			
			   
serverSock.close()    

    
    
    
# ~ def main(args):
    # ~ return 0

# ~ if __name__ == '__main__':
    # ~ import sys
    # ~ sys.exit(main(sys.argv))

