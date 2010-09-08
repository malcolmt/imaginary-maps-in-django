from django.contrib.gis.db import models

class Land(models.Model):
    """
    Land boundaries that are used on the map.
    """
    name = models.CharField(max_length=50)
    region = models.PolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


# Used when importing shape data into this model.
land_layermap = {
    "name": "name",
    "region": "POLYGON",
}

