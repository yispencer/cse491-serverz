#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from StringIO import StringIO
from app import make_app
from wsgiref.validate import validator
from sys import stderr

def main(socketmodule = None):

    if socketmodule is None:
        socketmodule = socket

    s = socketmodule.socket()         # Create a socket object
    host = socketmodule.getfqdn() # Get local machine name
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
        handle_connection(c, client_port);

def handle_connection(conn,port):
  
    # Break down the request into parts 
    recv = conn.recv(1)
    if not recv:
        print 'Error'
        return

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
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
    env['SERVER_PORT'] = str(port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread'] = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once'] = False
    env['wsgi.url_scheme'] = 'http'

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
    validator_app = validator(appl)
    result = appl(env, start_response)
    for data in result:
        conn.send(data)
    conn.close() 

if __name__ == '__main__':
   main()
