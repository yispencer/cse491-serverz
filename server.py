#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from StringIO import StringIO
from app import make_app

def main():

    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c);

def handle_connection(conn):
  
    # Break down the request into parts 
    recv = conn.recv(1)
    env = {}
    while recv[-4:] != '\r\n\r\n':
        recv += conn.recv(1)

    raw_request, raw_headers = recv.split('\r\n',1)
    raw_request = raw_request.split(' ')
 
    # Putting all of the request headers into a dictionary
    a_dict = {}
    for line in raw_headers.split('\r\n')[:-2]:
        k,v = line.split(":",1)
        a_dict[k.lower()] = v

    method = raw_request[0]
    url = urlparse(raw_request[1])
    parsed_path = url[2]

    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = url[2]
    env['QUERY_STRING'] = url[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = 0

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ": " + header + '\r\n')
        conn.send('\r\n')
    
    content = ''
    if method == 'POST':
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = a_dict['content-length']
        env['CONTENT_TYPE'] = a_dict['content-type']
        while len(content) < int(a_dict['content-length']):
            content += conn.recv(1)

    env['wsgi.input'] = StringIO(content)
    appl = make_app()
    result = appl(env, start_response)
    for data in result:
        conn.send(data)
    conn.close() 

if __name__ == '__main__':
   main()
