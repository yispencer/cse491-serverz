#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from StringIO import StringIO
from app import make_app
from wsgiref.validate import validator
from sys import stderr
import argparse
import cookieapp

def main(socketmodule = None):

    if socketmodule is None:
        socketmodule = socket

    s = socketmodule.socket()         # Create a socket object
    host = socketmodule.getfqdn() # Get local machine name
    argParser = argparse.ArgumentParser(description = 'Set up WSGI server')
    argParser.add_argument('-A', metavar='App', type=str, nargs=1, \
                           default = 'myapp',   \
                           choices=['myapp',    \
                                    'imageapp', \
                                    'altdemo',  \
                                    'chat',     \
                                    'quotes',  \
                                    'cookie'],  \
                           help='Select which app to run', dest='app')
    argParser.add_argument('-p', metavar='Port', type=int, nargs=1, \
                           default = -1, help='Select a port to run on', \
                           dest='p')
    argValues = argParser.parse_args()

    port = argValues.p[0] if argValues.p != -1 else random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    app = argValues.app[0]
    
    # Quixote altdemo 
    if app == 'altdemo':
        import quixote
        from quixote.demo.altdemo import create_publisher
        try:
            p = create_publisher()
        except RuntimeError:
            pass
        wsgi_app = quixote.get_wsgi_app() 

    # Image app
    elif app == 'imageapp':
        import quixote
        import imageapp
        from imageapp import create_publisher
        import sqlite3
        p = create_publisher()
        imageapp.setup()
        wsgi_app = quixote.get_wsgi_app()
    # Chat app
    elif app == 'chat':
        from chat.apps import ChatApp as make_app 
        wsgi_app = make_app('chat/html')
 
    # quotes app
    elif app == 'quotes':
        from quotes.apps import QuotesApp as make_app 
        wsgi_app = make_app('quotes/quotes.txt', \
                                          'quotes/html')    
    # cookie app 
    elif app == 'cookie':
        wsgi_app = cookieapp.get_wsgi_app()

    # My app
    else:
        from app import make_app
        wsgi_app = make_app()
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, port, wsgi_app);

def handle_connection(conn, port, app):
  
    # Break down the request into parts 
    recv = conn.recv(1)

    env = {}
    while recv[-4:] != '\r\n\r\n':
        new = conn.recv(1)
        if new == '':
            return
        else:
            recv += new

    raw_request, raw_headers = recv.split('\r\n',1)
 
    # Putting all of the request headers into a dictionary
    header_dict = {}
    for line in raw_headers.split('\r\n')[:-2]:
        k,v = line.split(': ', 1)
        header_dict[k.lower()] = v
    
    url = urlparse(raw_request.split(' ', 3)[1])
   
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
    env['HTTP_COOKIE'] = header_dict['cookie'] \
                         if 'cookie' in header_dict.keys() else '' 

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ": " + header + '\r\n')
        conn.send('\r\n')
    
    content = ''
    if raw_request.startswith('POST '):
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = str(header_dict['content-length'])
        env['CONTENT_TYPE'] = header_dict['content-type']
        while len(content) < int(header_dict['content-length']):
            content += conn.recv(1)

    env['wsgi.input'] = StringIO(content)
    app = validator(app)
    result = app(env, start_response)
    for data in result:
        conn.send(data)
    result.close()
    conn.close() 

if __name__ == '__main__':
   main()
