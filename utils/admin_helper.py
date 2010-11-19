from django.contrib.gis import admin

class AdminBase(admin.GeoModelAdmin):
    openlayers_url = "/static_data/openlayers/OpenLayers.js"
    wms_url = "http://localhost:8001"
    wms_layer = "base"
    wms_name = "Imaginary island"
    default_lat = -0.0434097180624
    default_lon = 150.057492178
