"""
The interface that sets up our WMS server with the maps and layers we're able
to serve.

Based on http://trac.mapnik.org/browser/trunk/docs/ogcserver/readme.txt
"""

import os

from mapnik2.ogcserver import WMS


MAPFILE_XML = os.path.join(os.path.dirname(__file__), "island.xml")

class WMSFactory(WMS.BaseWMSFactory):
    def __init__(self):
        WMS.BaseWMSFactory.__init__(self)   # Old style class. :-(
        self.loadXML(MAPFILE_XML)
        self.finalize()

