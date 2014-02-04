#!/usr/bin/env python
import random
import socket
import time
import urlparse

header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n' + \
         '\r\n'
 
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

def handle_index(conn,url):

    # handle the main page

    conn.send(header + \
              '<h1>Hello, world.</h1>' + \
              'This is yispencer\'s Web server.<br><br>' + \
              '<A HREF="/content">Content Page</A><br>' + \
              '<A HREF="/file">File Page</A><br>' + \
              '<A HREF="/image">Image Page</A><br>' + \
              '<A HREF="/form">Form Page</A>')

def handle_content(conn,url):

    # handle the content page

    conn.send(header + \
              'This is content page.')

def handle_file(conn,url):

    # handle the file page

    conn.send(header + \
              'This is file page.')
 
def handle_image(conn,url): 

    # handle the image page

    conn.send(header + \
              'This is image page.')

def handle_post(conn,url):

    # handle the post request

    conn.send(header + \
              'POST requested...\r\n' + \
              'Hello, world.')

def handle_error(conn,url):

    # handle pages not sepecified 

    conn.send(header + \
              '<h1>ERROR</h>')

def handle_form(conn,url):

    # handle the form page

    conn.send(header + \
              "<form action='/submit' method='GET'>\n" + \
              "first name: <input type='text' name='firstname'>\n" + \
              "last name: <input type='text' name='lastname'>\n" + \
              "<input type='submit' value='Submitz'>\n\n" + \
              "</form>")

def handle_submit(conn,url):

    # handle the submit page

    query = url.split("&")
    firstname = query[0].split("=")[1]
    lastname = query[1].split("=")[1] 
    conn.send(header + \
              "Hi Mr. %s %s." % (firstname, lastname))

def handle_connection(conn):
  
    # get the method type and the path
 
    recv = conn.recv(1000) 
    first_line = recv.splitlines()[0].split(' ')
    method = first_line[0]
    url = urlparse.urlparse(first_line[1])
    parsed_path = url[2]

    # send appropriate data

    if method == "POST":
         if parsed_path == "/":
              handle_post(conn,'')
         elif parsed_path == "/submit":
              handle_submit(conn,recv.split('\r\n')[-1]) 
    
    elif parsed_path == "/": 
         handle_index(conn,'')
   
    elif parsed_path == "/content": 
         handle_content(conn,'')
  
    elif parsed_path == "/file":
         handle_file(conn,'')
 
    elif parsed_path == "/image":
         handle_image(conn,'')

    elif parsed_path == "/form":
         handle_form(conn,'')
    
    elif parsed_path == "/submit":
         handle_submit(conn,url[4])

    else:
         handle_error(conn,'')


    conn.close()

if __name__ == '__main__':
   main()
