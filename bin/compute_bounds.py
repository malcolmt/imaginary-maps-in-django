#!/usr/bin/env python
"""
Given a bounding box dimensions, in metres, and a longitude, latitude pair for
the upper left corner, roughly computes the long/lat pair for the lower right
corner in the WGS84 spatial reference system. This is useful for placing a fake
map on a sphere that resembles the earth. We often know the map dimensions in
metres, but WGS84 deals in degrees.

It is assumed that the dimensions are small enough that the particular
reference system won't play a big role in the bounds (and that the placement
is around the equator regions, where stretching is relatively minimal). The
computations are all done in the EPSG:3785 (a.k.a. "900913") frame and then
reprojected to EPSG:4326 (WGS84). Doing all computations in EGS84 would reveal
fractionally different values, but so small as to make no pratical difference
on regions of the order of 10 - 100 km square.

Although this program uses some modules from django.contrib.gis, they do not
depend upon Django's environment being set up.

Called as:
        compute_bounds.py <ul_long> <ul_lat> <width> <height>
"""

import sys

from django.contrib.gis import geos


def main(argv=None):
    if argv is None:
        argv = sys.argv
    ul_long, ul_lat = float(argv[1]), float(argv[2])
    width, height = float(argv[3]), float(argv[4])
    
    # First, convert upper left coordinate to a metre-based representation.
    up_left = geos.Point(ul_long, ul_lat, srid=4326)
    up_left.transform(3785)

    # Second, construct a polygon (rectangle) of the required dimensions.
    ulx, uly = up_left.coords
    lrx, lry = ulx + width, uly - height
    polygon = geos.Polygon(((ulx, uly), (lrx, uly), (lrx, lry), (ulx, lry),
            (ulx, uly)), srid=3785)

    # Finally, convert back to WGS84 and display the bounds.
    polygon.transform(4326)
    print "Region bounding box is:\n\t", polygon.extent

if __name__ == "__main__":
    sys.exit(main())
 
