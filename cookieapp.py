def wsgi_app(env, start_response):
    path = env['PATH_INFO']

    if path == '/':
        cookie_info = env.get('HTTP_COOKIE', "")
        cookie_info = "The cookie sez: %s<p>" % cookie_info
        start_response('200 OK', [('Content-type', 'text/html')])
        return [cookie_info,
                "<a href='/set'>Set cookie</a> | ",
                "<a href='/del'>Clear cookie</a>"]
    elif path == '/set':
        start_response('302 Redirect', [('Content-type', 'text/html'),
            ('Location', '/'),
            ('Set-Cookie', 'favorite_color=red')
            ])
        return ["You should have been redirected"]
    elif path == '/del':
        start_response('302 Redirect', [('Content-type', 'text/html'),
            ('Location', '/'),
            ('Set-Cookie', 'favorite_color=NONE; Expires=Thu, 01-Jan-1970 00:00:01 GMT')
            ])

        return ["You should have been redirected"]
    start_response('404 Not Found', [('Content-type', \
                                      'text/html;   \
                                      charset="UTF-8"')])
    return []

def get_wsgi_app():
    return wsgi_app
