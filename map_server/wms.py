#!/usr/bin/env python
"""
Run a WMS (web mapping service) server via the WSGI API. Based on
http://trac.mapnik.org/wiki/OgcServer .
"""

import os
import sys

from mapnik.ogcserver.wsgi import WSGIApp


PORT = 8001
CONF_FILE = os.path.join(os.path.dirname(__file__), "ogcserver.conf")

sys.path.insert(0, os.path.dirname(__file__))
application = WSGIApp(CONF_FILE)

if __name__ == "__main__":
    # Run in standalone mode. Useful for development
    from wsgiref.simple_server import make_server

    httpd = make_server("localhost", PORT, application)
    print "Listening on port %d..." % PORT
    httpd.serve_forever()

