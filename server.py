def main():
    #!/usr/bin/env python
    import random
    import socket
    import time

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
  
    # get the method type and the path
 
    recv = conn.recv(1000) 
    path = recv.splitlines()[0].split(' ',2)[1]
    method = recv.splitlines()[0].split(' ',2)[0]

    # send appropriate data

    if method == "POST":
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  'POST requested...\r\n' + \
                  'Hello, world.')
    elif path == "/": 
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Hello, world.</h1>' + \
                  'This is yispencer\'s Web server.<br><br>' + \
                  '<A HREF="/content">Content Page</A><br>' + \
                  '<A HREF="/file">File Page</A><br>' + \
                  '<A HREF="/image">Image Page</A>')
    elif path == "/content": 
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  'This is content page.')
    elif path == "/file":
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  'This is file page.')
    elif path == "/image":
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  'This is image page.')
    conn.close()

if __name__ == '__main__':
   main()
