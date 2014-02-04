import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True


def test_handle_index():
    
    # Test the main page.
   
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is yispencer\'s Web server.<br><br>' + \
                      '<A HREF="/content">Content Page</A><br>' + \
                      '<A HREF="/file">File Page</A><br>' + \
                      '<A HREF="/image">Image Page</A><br>' + \
                      '<A HREF="/form">Form Page</A>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_content():

    # Test the content page.

    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is content page.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_file():

    # Test the file page.

    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is file page.'

    server.handle_connection(conn)


    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_image():

    # Test the image page.
    
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'This is image page.'

    server.handle_connection(conn)


    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_post():

    # Test the POST request.

    conn = FakeConnection("POST / HTTP1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'POST requested...\r\n' + \
                      'Hello, world.'

    server.handle_connection(conn)


    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_error():

    # Test the handle error function.

    conn = FakeConnection("GET /notapage HTTP1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>ERROR</h>'

    server.handle_connection(conn)


    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_form():

    # Test the form page.

    conn = FakeConnection("GET /form HTTP1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<form action='/submit' method='GET'>\n" + \
                      "first name: <input type='text' name='firstname'>\n" + \
                      "last name: <input type='text' name='lastname'>\n" + \
                      "<input type='submit' value='Submitz'>\n\n" + \
                      "</form>"

    server.handle_connection(conn)


    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_submit():

    # Test the handle submit function.

    conn = FakeConnection('''GET /submit?firstname=Spencer&lastname=Yi
HTTP/1.0\r\n\r\n''')
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Hi Mr. Spencer Yi.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

    # Test POST submit request.

    conn = FakeConnection('''POST /submit HTTP/1.0\r\n\r\nfirstname=Cocoa&lastname=Milk''')

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Hi Mr. Cocoa Milk.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
