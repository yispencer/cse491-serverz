import jinja2
from urlparse import parse_qs
from urllib import unquote
import cgi

def app(environ, start_response):
    # pages we know that exist
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
    response_headers = [('Content-type', 'text/html')]

    if environ['PATH_INFO'] in response: 
        status = '200 OK'
        template = env.get_template(response[environ['PATH_INFO']])
    else:  
        status = '404 Not Found'
        template = env.get_template('404.html')
    
    x = parse_qs(environ['QUERY_STRING']).iteritems()
    args = {k : v[0] for k,v in x}
    args['path'] = environ['PATH_INFO']

    if environ['REQUEST_METHOD'] == 'POST': # if requested method is POST
        headers = {k[5:].lower().replace('_','-') : v \
                   for k,v in environ.iteritems() if(k.startswith('HTTP'))}
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, \
                                environ=environ)
        args.update({x : form[x].value for x in form.keys()})

    uargs = {}
    for k,v in args.iteritems():
        try:
            x = unicode(v, 'utf-8')
        except UnicodeDecodeError:
            x = v.decod('cp1252')
        uargs[unicode(k, 'utf-8')] = unicode(x.encode('ascii', 'xmlcharrefreplace'), 'utf-8')

    start_response(status, response_headers)
    return [bytes(template.render(uargs))]

                       
def make_app():
    return app
