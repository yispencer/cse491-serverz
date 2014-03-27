import jinja2
from urlparse import parse_qs
import cgi
from os import listdir
from random import choice
from StringIO import StringIO

def fileData(fname):
    fp = open(fname, 'rb')
    data = [fp.read()]
    fp.close()
    return data

def index(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('index.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def content(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('content.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def serveImage(env, **kwargs):
    response_headers = [('Content-type', 'image/jpeg')]
    data = fileData(kwargs['path'][1:]) 
    return (response_headers, data)

def serveFile(env, **kwargs):
    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]
    data = fileData(kwargs['path'][1:]) 
    return (response_headers, data)

def Image(env, **kwargs):
    kwargs['path'] = '/images/'+choice(listdir('images'))
    return serveFile(env, **kwargs)

def ImageList(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset"UTF-8"')]
    kwargs['images'] = listdir('images')
    template = env.get_template('imagelist.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def File(env, **kwargs):
    kwargs['path'] = '/files/'+choice(listdir('files'))
    return serveFile(env, **kwargs)

def Form(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('form.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def submit(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('submit.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)

def fail(env, **kwargs):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    template = env.get_template('404.html')
    data = [template.render(kwargs).encode('utf-8')]
    return (response_headers, data)
  
def app(environ, start_response):
    # pages we know that exist
    response = {
                '/'          : index,     \
                '/content'   : content,   \
                '/file'      : File,      \
                '/image'     : Image,     \
                '/imagelist' : ImageList, \
                '/form'      : Form,      \
                '/submit'    : submit,    \
                '404'        : fail,      \
               }

    for page in listdir('images'):
        response['/images/' + page] = serveImage
    for page in listdir('files'):
        response['/files/' + page] = serveFile

    # Basic connection information and set up templates from brtaylor92's repo
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
   
    x = parse_qs(environ['QUERY_STRING']).iteritems()
    args = {k : v[0] for k,v in x}
    args['path'] = environ['PATH_INFO']

    if environ['REQUEST_METHOD'] == 'POST': # if requested method is POST
        headers = {k[5:].lower().replace('_','-') : v \
                   for k,v in environ.iteritems() if(k.startswith('HTTP'))}
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']

        # Hack from brtaylor92's repo in order to bypass validator problem
        if "multipart/form-data" in environ['CONTENT_TYPE']:
            cLen = int(environ['CONTENT_LENGTH'])
            data = environ['wsgi.input'].read(cLen)
            environ['wsgi.input'] = StringIO(data)

        form = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, \
                                environ=environ)
        args.update({x : form[x].value for x in form.keys()})

    args = {k.decode('utf-8') : v.decode('utf-8') \
            for k, v in args.iteritems()
           }

    if environ['PATH_INFO'] in response:
        status = '200 OK'
        path = environ['PATH_INFO']
    else:
        status = '404 Not Found'
        path = '404'

    args['path'] = path
    response_headers, data = response[path](env, **args)

    start_response(status, response_headers)
    return data
           
def make_app():
    return app
