from django.contrib.gis import admin

from adventure import models
from utils.admin_helper import AdminBase

admin.site.register([models.Track, models.PointOfInterest], AdminBase)
admin.site.register([models.Note, models.FeatureType])

