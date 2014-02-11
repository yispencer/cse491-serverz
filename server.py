#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
import cgi
from StringIO import StringIO
import jinja2

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

    # Pages we know that exist
    response = {
                '/'        : 'index.html',   \
                '/content' : 'content.html', \
                '/file'    : 'file.html',    \
                '/image'   : 'image.html',   \
                '/form'    : 'form.html',    \
                '/submit'  : 'submit.html',  \
               }
    # Basic connection information and set up templates from brtaylor92's repo
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    retval = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    data = ''
    # send appropriate data
    args = parse_qs(url[4]) 
    if method == "POST":
         # Add the content portion of the request to the dictionary
         length = int(a_dict['content-length'])
         while len(data) < length:
             data += conn.recv(1)
    form = cgi.FieldStorage(fp=StringIO(data), headers=a_dict, \
                            environ={'REQUEST_METHOD' : 'POST'})
    args.update(dict([(x, [form[x].value]) for x in form.keys()]))
         
    if url[2] in response:
        template = env.get_template(response[url[2]])
    else:
        args['path'] = url[2]
        retval = 'HTTP/1.0 404 Not Found\r\n\r\n'
        template = env.get_template('404.html') 
    retval += template.render(args)
    conn.send(retval) 
    conn.close()

if __name__ == '__main__':
   main()
