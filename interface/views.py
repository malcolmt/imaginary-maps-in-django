from django.contrib.gis import geos
from django.contrib.gis.shortcuts import render_to_kml

import adventure.models

def tracks(request):
    bbox = request.GET.get("BBOX", request.GET.get("bbox"))
    minx, miny, maxx, maxy = [float(elt) for elt in bbox.split(",")]
    geom = geos.Polygon.from_bbox((minx, miny, maxx, maxy))
    result = adventure.models.Track.objects.filter(path__intersects=geom).kml()
    return render_to_kml("gis/kml/placemarks.kml", {"geomdata": result,
        "places": result})

def places(request):
    bbox = request.GET.get("BBOX", request.GET.get("bbox"))
    minx, miny, maxx, maxy = [float(elt) for elt in bbox.split(",")]
    geom = geos.Polygon.from_bbox((minx, miny, maxx, maxy))
    result = adventure.models.PointOfInterest.objects. \
            filter(location__bboverlaps=geom).kml()
    return render_to_kml("gis/kml/placemarks.kml", {"geomdata": result,
        "places": result})

