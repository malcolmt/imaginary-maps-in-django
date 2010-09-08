from django.contrib.gis.db import models

class Track(models.Model):
    """
    Some kind of track on a land feature. For example, a walking track, or an
    animal migration route. Tracks are represented as lines and, as such, have
    no width.
    """
    name = models.CharField(unique=True, max_length=50)
    path = models.LineStringField(geography=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name


class FeatureType(models.Model):
    """
    A type of location that might be a point of interest.
    """
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class PointOfInterest(models.Model):
    """
    A notable location. Could be a shipwreck, a camping place... anything that
    is a single location.
    """
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(FeatureType)
    location = models.PointField()

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = "points of interest"

    def __unicode__(self):
        return self.name


class Note(models.Model):
    """
    A note about a PointOfInterest.
    """
    poi = models.ForeignKey(PointOfInterest)
    date = models.DateField()
    note = models.TextField()

    # Required for GIS queries on related model.
    objects = models.GeoManager()

    def __unicode__(self):
        # XXX: Work around fact that strftime() cannot usually handle years
        # prior to 1900.
        tmp_date = self.date.replace(year=1900)
        date_str = u"%s, %s" % (tmp_date.strftime("%d %b"), self.date.year)
        return u"Note about %s: %s" % (self.poi, date_str)

track_layermap = {
    "name": "Name",
    "path": "LINESTRING",
}

