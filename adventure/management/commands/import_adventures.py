#!/usr/bin/env python
"""
Loads tracks and point of interest into the adventure models.
"""

import datetime
import os

from django.contrib.gis import utils, gdal
from django.core.management import base

from adventure import models


TRACK_FILE = "../../data/tracks.shp"
POI_FILE = "../../data/notables.shp"

class Command(base.NoArgsCommand):
    def handle_noargs(self, **options):
        verbosity = bool(int(options.get("verbosity", 1)))

        # 1. Use layer mapping to load the track data.
        basedir = os.path.dirname(__file__)
        filename = os.path.join(basedir, TRACK_FILE)
        layermapping = utils.LayerMapping(models.Track, filename,
                models.track_layermap)
        layermapping.save(strict=True, verbose=verbosity)

        # 2. Import the points of interest data manually, since we have to
        # parse date strings.
        datasource = gdal.DataSource(os.path.join(basedir, POI_FILE))
        layer = datasource[0]
        
        # Populate the FeatureType values first, for efficiency.
        existing = set(models.FeatureType.objects.values_list("name",
                flat=True))
        for feature_type in layer.get_fields("type"):
            if feature_type not in existing:
                models.FeatureType(name=feature_type).save()
                existing.add(feature_type)
        features = dict(models.FeatureType.objects.values_list("name", "id"))

        # Now create the PointOfInterest and "initial observation" Note for
        # each item in the layer.
        existing_pois = dict(models.PointOfInterest.objects.values_list("name",
                "id"))
        existing_notes = set(models.Note.objects.values_list("poi_id",
                flat=True))
        for item in layer:
            name = item.get("name")
            poi_id = existing_pois.get(name)
            if not poi_id:
                poi = models.PointOfInterest.objects.create(
                        name = name,
                        type_id = features[item.get("type")],
                        location = item.geom.wkt
                        )
                poi_id = poi.id
            if poi_id in existing_notes:
                continue
            date = datetime.datetime.strptime(item.get("date"),
                    "%d-%b-%Y").date()
            models.Note(poi=poi, date=date, note="Initial observation").save()

