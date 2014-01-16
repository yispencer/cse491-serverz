#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000,9000)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print 'Got connection from', client_host, client_port

    init = "HTTP/1.0 200 OK\r\n"
    header = "Content-Type:  text/html\r\n\r\n"
    body = "<h1>Hello, world</h1> this is msweet18's web server."
    message = init + header + body
    c.send(message)
    c.close()

    # @comment this code looks good, and it runs well on Firefox.
    # I checked if it works on other browsers, and it doesn't work
    # on Chrome or Internet Explorer. I can't seem to fix it..
    # You used spaces instead of tabs so that's good and you spelled
    # the variable names properly. 
