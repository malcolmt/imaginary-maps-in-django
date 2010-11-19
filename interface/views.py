from django.contrib.gis import geos
from django.contrib.gis.shortcuts import render_to_kml

import adventure.models

KML_TEMPLATE = "gis/kml/placemarks.kml"

def _get_request_box(request):
    """
    Returns a geos.Polygon that describes the OpenLayers bounding box for the
    request.
    """
    bbox = request.GET.get("BBOX", request.GET.get("bbox"))
    minx, miny, maxx, maxy = [float(elt) for elt in bbox.split(",")]
    return geos.Polygon.from_bbox((minx, miny, maxx, maxy))

def tracks(request):
    geom = _get_request_box(request)
    result = adventure.models.Track.objects.filter(path__intersects=geom).kml()
    return render_to_kml(KML_TEMPLATE, {"geomdata": result, "places": result})

def places(request):
    geom = _get_request_box(request)
    result = adventure.models.PointOfInterest.objects. \
            filter(location__bboverlaps=geom).kml()
    return render_to_kml(KML_TEMPLATE, {"geomdata": result, "places": result})

